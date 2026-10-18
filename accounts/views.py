from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import (
    UserRegistrationForm, TeacherCreationForm, TeacherEditForm,
    AdminResetPasswordForm, TeacherChangePasswordForm
)
from .models import User, Role
from .permissions import admin_required


@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully.')
            return redirect('dashboard-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_user.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@admin_required
def manage_teachers(request):
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'all')

    teachers = User.objects.filter(Q(is_teacher=True) | Q(role__name__icontains='teacher')).order_by('-date_joined')

    if query:
        teachers = teachers.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(employee_id__icontains=query) |
            Q(department_name__icontains=query)
        )

    if status_filter == 'active':
        teachers = teachers.filter(is_active=True)
    elif status_filter == 'inactive':
        teachers = teachers.filter(is_active=False)
    elif status_filter == 'must_change_pwd':
        teachers = teachers.filter(must_change_password=True)

    total_count = User.objects.filter(is_teacher=True).count()
    active_count = User.objects.filter(is_teacher=True, is_active=True).count()
    must_change_count = User.objects.filter(is_teacher=True, must_change_password=True).count()

    return render(request, 'accounts/manage_teachers.html', {
        'teachers': teachers,
        'query': query,
        'status_filter': status_filter,
        'total_count': total_count,
        'active_count': active_count,
        'must_change_count': must_change_count,
    })


@admin_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            default_pwd = form.cleaned_data.get('default_password') or 'Teacher@2026'
            teacher.set_password(default_pwd)
            teacher.is_teacher = True
            teacher.is_staff = True
            teacher.must_change_password = True

            teacher_role, _ = Role.objects.get_or_create(name='Teacher')
            teacher.role = teacher_role
            teacher.save()

            messages.success(
                request,
                f'Teacher account for {teacher.get_full_name() or teacher.username} created successfully! '
                f'Default password is "{default_pwd}" (real-time sync active, teacher prompted to change on login).'
            )
            return redirect('manage-teachers')
    else:
        form = TeacherCreationForm()

    return render(request, 'accounts/add_teacher.html', {'form': form})


@admin_required
def edit_teacher(request, user_id):
    teacher = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = TeacherEditForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Details for {teacher.get_full_name() or teacher.username} updated successfully in real time.')
            return redirect('manage-teachers')
    else:
        form = TeacherEditForm(instance=teacher)

    return render(request, 'accounts/edit_teacher.html', {'form': form, 'teacher': teacher})


@admin_required
def reset_teacher_password(request, user_id):
    teacher = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminResetPasswordForm(request.POST)
        if form.is_valid():
            new_pwd = form.cleaned_data['new_password']
            force_change = form.cleaned_data.get('force_change', True)

            teacher.set_password(new_pwd)
            teacher.must_change_password = force_change
            teacher.save()

            messages.success(
                request,
                f'Password for teacher "{teacher.username}" has been reset and synced in real time! '
                f'New temporary password: {new_pwd}'
            )
            return redirect('manage-teachers')
    else:
        form = AdminResetPasswordForm(initial={'new_password': 'Teacher@2026', 'force_change': True})

    return render(request, 'accounts/reset_teacher_password.html', {'form': form, 'teacher': teacher})


@admin_required
def toggle_teacher_status(request, user_id):
    if request.method == 'POST':
        teacher = get_object_or_404(User, id=user_id)
        teacher.is_active = not teacher.is_active
        teacher.save()
        status_label = 'Activated' if teacher.is_active else 'Deactivated'
        messages.success(request, f'Teacher {teacher.username} account has been {status_label} in real time.')
    return redirect('manage-teachers')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = TeacherChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.must_change_password = False
            user.save()
            # Keep user session active after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed and synced in real time across the portal!')
            return redirect('dashboard-home')
    else:
        form = TeacherChangePasswordForm(request.user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'must_change': request.user.must_change_password
    })
