from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ClassRoom, Student, AttendanceSession, AttendanceRecord

User = get_user_model()


class AttendanceTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher_att",
            password="TeacherPass123!",
            is_teacher=True,
            is_staff=True
        )
        self.classroom = ClassRoom.objects.create(
            name="Form 1 Test Sciences",
            grade_level="Form 1",
            stream="Sciences",
            class_teacher=self.teacher
        )
        self.student1 = Student.objects.create(
            first_name="Tatenda",
            last_name="Chiwenga",
            admission_number="AGC-TEST-001",
            classroom=self.classroom,
            parent_phone="+263771000001"
        )
        self.student2 = Student.objects.create(
            first_name="Blessed",
            last_name="Ncube",
            admission_number="AGC-TEST-002",
            classroom=self.classroom,
            parent_phone="+263771000002"
        )

    def test_attendance_dashboard_access(self):
        self.client.login(username="teacher_att", password="TeacherPass123!")
        response = self.client.get(reverse('attendance-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Form 1 Test Sciences")

    def test_take_attendance_and_record_saved(self):
        self.client.login(username="teacher_att", password="TeacherPass123!")
        url = reverse('take-attendance', kwargs={'classroom_id': self.classroom.id})
        response = self.client.post(url, {
            'date': '2026-10-18',
            'session_type': 'Morning',
            'notes': 'Test laboratory attendance',
            f'status_{self.student1.id}': 'present',
            f'remarks_{self.student1.id}': '',
            f'status_{self.student2.id}': 'absent',
            f'remarks_{self.student2.id}': 'Flu symptoms',
        })
        self.assertEqual(response.status_code, 302)

        session = AttendanceSession.objects.filter(classroom=self.classroom, date='2026-10-18').first()
        self.assertIsNotNone(session)
        self.assertEqual(session.present_count, 1)
        self.assertEqual(session.absent_count, 1)
        self.assertEqual(session.total_records, 2)

    def test_attendance_detail_contains_whatsapp_link(self):
        self.client.login(username="teacher_att", password="TeacherPass123!")
        session = AttendanceSession.objects.create(
            classroom=self.classroom,
            teacher=self.teacher,
            date='2026-10-18',
            session_type='Morning',
            notes='All present completed practicals.'
        )
        AttendanceRecord.objects.create(session=session, student=self.student1, status='present')
        AttendanceRecord.objects.create(session=session, student=self.student2, status='absent', remarks='Doctor appointment')

        url = reverse('attendance-session-detail', kwargs={'session_id': session.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Share Attendance to WhatsApp")
        self.assertContains(response, "https://api.whatsapp.com/send?text=")
        self.assertContains(response, "Blessed%20Ncube")
