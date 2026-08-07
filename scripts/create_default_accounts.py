import os
import sys
import django


def main():
    # Ensure project root is on path so settings can be imported
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from accounts.models import Role, User

    roles = [
        ('Administrator', 'Full access admin role'),
        ('Librarian', 'Manages library resources and borrowing'),
        ('Teacher', 'Academic staff member'),
        ('Student', 'Learner/student account'),
    ]

    created_roles = {}
    for name, desc in roles:
        role, _ = Role.objects.get_or_create(name=name, defaults={'description': desc})
        created_roles[name] = role

    users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'AdminPass123!',
            'role': created_roles['Administrator'],
            'is_superuser': True,
            'is_staff': True,
            'is_staff_member': True,
        },
        {
            'username': 'librarian',
            'email': 'librarian@example.com',
            'password': 'LibrarianPass123!',
            'role': created_roles['Librarian'],
            'is_superuser': False,
            'is_staff': False,
            'is_staff_member': True,
        },
        {
            'username': 'teacher',
            'email': 'teacher@example.com',
            'password': 'TeacherPass123!',
            'role': created_roles['Teacher'],
            'is_superuser': False,
            'is_staff': False,
            'is_teacher': True,
        },
        {
            'username': 'student',
            'email': 'student@example.com',
            'password': 'StudentPass123!',
            'role': created_roles['Student'],
            'is_superuser': False,
            'is_staff': False,
            'is_student': True,
        },
    ]

    results = []
    for u in users:
        username = u['username']
        try:
            user = User.objects.get(username=username)
            updated = False
            # Update role and flags if needed
            if user.role != u['role']:
                user.role = u['role']
                updated = True
            for flag in ('is_superuser', 'is_staff', 'is_staff_member', 'is_teacher', 'is_student'):
                if flag in u and getattr(user, flag, False) != u.get(flag, False):
                    setattr(user, flag, u.get(flag, False))
                    updated = True
            if updated:
                user.save()
            results.append((username, False))
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, email=u['email'], password=u['password'])
            # set additional flags
            if u.get('is_superuser'):
                user.is_superuser = True
            if u.get('is_staff'):
                user.is_staff = True
            if u.get('is_staff_member'):
                user.is_staff_member = True
            if u.get('is_teacher'):
                user.is_teacher = True
            if u.get('is_student'):
                user.is_student = True
            user.role = u['role']
            user.save()
            results.append((username, True))

    print('Created/updated users:')
    for username, created in results:
        print(f'- {username} (created={created})')

    print('\nCredentials:')
    for u in users:
        print(f"{u['username']} -> email: {u['email']}, password: {u['password']}")


if __name__ == '__main__':
    main()
