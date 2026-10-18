import urllib.parse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import ClassRoom, Student, AttendanceSession, AttendanceRecord
from .forms import ClassRoomForm, StudentForm
from accounts.permissions import teacher_or_librarian_required


@teacher_or_librarian_required
def attendance_dashboard(request):
    classes = ClassRoom.objects.all().prefetch_related('students')
    recent_sessions = AttendanceSession.objects.select_related('classroom', 'teacher').prefetch_related('records').all()[:10]
    total_classes = classes.count()
    total_students = Student.objects.filter(is_active=True).count()
    today_sessions = AttendanceSession.objects.filter(date=timezone.now().date()).count()

    return render(request, 'attendance/dashboard.html', {
        'classes': classes,
        'recent_sessions': recent_sessions,
        'total_classes': total_classes,
        'total_students': total_students,
        'today_sessions': today_sessions,
    })


@teacher_or_librarian_required
def take_attendance(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, id=classroom_id)
    students = classroom.students.filter(is_active=True).order_by('last_name', 'first_name')

    date_str = request.GET.get('date', timezone.now().date().isoformat())
    session_type = request.GET.get('type', 'Morning')

    # Check if a session already exists for this date and type
    existing_session = AttendanceSession.objects.filter(
        classroom=classroom,
        date=date_str,
        session_type=session_type
    ).first()

    existing_records_map = {}
    if existing_session:
        for r in existing_session.records.all():
            existing_records_map[r.student_id] = r.status

    if request.method == 'POST':
        date_val = request.POST.get('date', date_str)
        session_type_val = request.POST.get('session_type', session_type)
        notes_val = request.POST.get('notes', '').strip()

        with transaction.atomic():
            session, created = AttendanceSession.objects.get_or_create(
                classroom=classroom,
                date=date_val,
                session_type=session_type_val,
                defaults={
                    'teacher': request.user,
                    'notes': notes_val
                }
            )
            if not created:
                session.notes = notes_val
                session.teacher = request.user
                session.save()

            for student in students:
                status_key = f'status_{student.id}'
                status_val = request.POST.get(status_key, 'present')
                remarks_key = f'remarks_{student.id}'
                remarks_val = request.POST.get(remarks_key, '').strip()

                AttendanceRecord.objects.update_or_create(
                    session=session,
                    student=student,
                    defaults={
                        'status': status_val,
                        'remarks': remarks_val
                    }
                )

        messages.success(request, f'Attendance for {classroom.name} on {date_val} successfully recorded!')
        return redirect('attendance-session-detail', session_id=session.id)

    return render(request, 'attendance/take_attendance.html', {
        'classroom': classroom,
        'students': students,
        'selected_date': date_str,
        'selected_type': session_type,
        'existing_session': existing_session,
        'existing_records_map': existing_records_map,
    })


@teacher_or_librarian_required
def attendance_session_detail(request, session_id):
    session = get_object_or_404(
        AttendanceSession.objects.select_related('classroom', 'teacher').prefetch_related('records__student'),
        id=session_id
    )
    records = session.records.select_related('student').order_by('student__last_name', 'student__first_name')
    absent_records = records.filter(status='absent')
    late_records = records.filter(status='late')

    # Build WhatsApp Share text
    teacher_name = session.teacher.get_full_name() if session.teacher else 'Class Teacher'
    lines = [
        "📋 *ABLEGOD COLLEGE - CLASS ATTENDANCE REPORT*",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"🏫 *Class:* {session.classroom.name}",
        f"📅 *Date:* {session.date.strftime('%A, %d %B %Y')}",
        f"⏰ *Session:* {session.session_type}",
        f"👨‍🏫 *Marked by:* {teacher_name}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━",
        "📊 *ATTENDANCE SUMMARY:*",
        f"• Total Roster: {session.total_records}",
        f"• Present: {session.present_count} ({session.attendance_percentage}%)",
        f"• Absent: {session.absent_count}",
        f"• Late: {session.late_count}",
        f"• Excused: {session.excused_count}",
    ]

    if absent_records.exists():
        lines.append("\n❌ *ABSENT STUDENTS:*")
        for idx, rec in enumerate(absent_records, 1):
            phone_info = f" (Parent: {rec.student.parent_phone})" if rec.student.parent_phone else ""
            lines.append(f"{idx}. {rec.student.full_name}{phone_info}")

    if late_records.exists():
        lines.append("\n⚠️ *LATE STUDENTS:*")
        for idx, rec in enumerate(late_records, 1):
            lines.append(f"{idx}. {rec.student.full_name}")

    if session.notes:
        lines.append(f"\n📝 *Teacher's Note:*\n_{session.notes}_")

    lines.append("\n━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("_Generated via AbleGod College E-Library & School Portal_")

    whatsapp_message_raw = "\n".join(lines)
    whatsapp_url = f"https://api.whatsapp.com/send?text={urllib.parse.quote(whatsapp_message_raw)}"

    return render(request, 'attendance/session_detail.html', {
        'session': session,
        'records': records,
        'absent_records': absent_records,
        'late_records': late_records,
        'whatsapp_message': whatsapp_message_raw,
        'whatsapp_url': whatsapp_url,
    })


@teacher_or_librarian_required
def manage_classes(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            classroom = form.save()
            messages.success(request, f'Class "{classroom.name}" created successfully!')
            return redirect('manage-classes')
    else:
        form = ClassRoomForm()

    classes = ClassRoom.objects.all().prefetch_related('students').order_by('name')
    return render(request, 'attendance/manage_classes.html', {
        'form': form,
        'classes': classes,
    })


@teacher_or_librarian_required
def manage_students(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, id=classroom_id)
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.full_name} added to {classroom.name}!')
            return redirect('manage-students', classroom_id=classroom.id)
    else:
        form = StudentForm(initial={'classroom': classroom})

    students = classroom.students.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'attendance/manage_students.html', {
        'classroom': classroom,
        'students': students,
        'form': form,
    })
