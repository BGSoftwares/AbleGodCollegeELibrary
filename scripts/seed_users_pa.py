import os
import sys
import django

# Setup Django environment
project_home = "/home/BGDevopps/AbleGodCollegeELibrary-master"
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User, Role

def create_users():
    print("Creating Roles...")
    admin_role, _ = Role.objects.get_or_create(name='Administrator')
    librarian_role, _ = Role.objects.get_or_create(name='Librarian')
    teacher_role, _ = Role.objects.get_or_create(name='Teacher')

    print("Creating Administrator...")
    admin, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@ablegod.edu'})
    admin.set_password('AdminPass123!')
    admin.role = admin_role
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()

    print("Creating Librarian...")
    librarian, created = User.objects.get_or_create(username='librarian', defaults={'email': 'librarian@ablegod.edu'})
    librarian.set_password('LibrarianPass123!')
    librarian.role = librarian_role
    librarian.is_staff_member = True
    librarian.save()

    print("Creating Teacher...")
    teacher, created = User.objects.get_or_create(username='teacher', defaults={'email': 'teacher@ablegod.edu'})
    teacher.set_password('TeacherPass123!')
    teacher.role = teacher_role
    teacher.is_teacher = True
    teacher.save()

    print("\nSuccess! Accounts created/updated:")
    print("1. admin / AdminPass123!")
    print("2. librarian / LibrarianPass123!")
    print("3. teacher / TeacherPass123!")

if __name__ == '__main__':
    create_users()
