import os
import sys
import django

# Setup django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from accounts.models import User, Role
from attendance.models import ClassRoom, Student
from dashboard.models import GalleryItem
from books.models import Book


def seed_data():
    print("[*] Seeding AbleGod College school management features...")

    # 1. Ensure Roles
    teacher_role, _ = Role.objects.get_or_create(name='Teacher', defaults={'description': 'Faculty Member'})
    admin_role, _ = Role.objects.get_or_create(name='Admin', defaults={'description': 'Administrator'})

    # 2. Create sample teachers
    teachers_data = [
        {
            'username': 'm.moyo',
            'first_name': 'Munashe',
            'last_name': 'Moyo',
            'email': 'm.moyo@ablegodcollege.ac.zw',
            'phone': '+263771122334',
            'employee_id': 'TCH-001',
            'department_name': 'Physical Sciences',
        },
        {
            'username': 'c.sibanda',
            'first_name': 'Chipo',
            'last_name': 'Sibanda',
            'email': 'c.sibanda@ablegodcollege.ac.zw',
            'phone': '+263772233445',
            'employee_id': 'TCH-002',
            'department_name': 'Humanities & Arts',
        },
        {
            'username': 't.dube',
            'first_name': 'Tinashe',
            'last_name': 'Dube',
            'email': 't.dube@ablegodcollege.ac.zw',
            'phone': '+263773344556',
            'employee_id': 'TCH-003',
            'department_name': 'Commercials & Accounting',
        },
    ]

    created_teachers = []
    for td in teachers_data:
        teacher, created = User.objects.get_or_create(
            username=td['username'],
            defaults={
                'first_name': td['first_name'],
                'last_name': td['last_name'],
                'email': td['email'],
                'phone': td['phone'],
                'employee_id': td['employee_id'],
                'department_name': td['department_name'],
                'is_teacher': True,
                'is_staff': True,
                'must_change_password': True,
                'role': teacher_role,
            }
        )
        if created:
            teacher.set_password('Teacher@2026')
            teacher.save()
            print(f"  ✅ Created teacher: {teacher.get_full_name()} (username: {teacher.username}, default pwd: Teacher@2026)")
        else:
            teacher.is_teacher = True
            teacher.employee_id = td['employee_id']
            teacher.department_name = td['department_name']
            teacher.save()
        created_teachers.append(teacher)

    # 3. Create Classrooms
    classrooms_data = [
        {'name': 'Form 1 Sciences', 'grade_level': 'Form 1', 'stream': 'Sciences', 'teacher': created_teachers[0]},
        {'name': 'Form 2 Arts', 'grade_level': 'Form 2', 'stream': 'Arts', 'teacher': created_teachers[1]},
        {'name': 'Form 3 Commercials', 'grade_level': 'Form 3', 'stream': 'Commercials', 'teacher': created_teachers[2]},
        {'name': 'Form 4 Sciences', 'grade_level': 'Form 4', 'stream': 'Sciences', 'teacher': created_teachers[0]},
    ]

    created_classes = []
    for cd in classrooms_data:
        c, created = ClassRoom.objects.get_or_create(
            name=cd['name'],
            defaults={
                'grade_level': cd['grade_level'],
                'stream': cd['stream'],
                'class_teacher': cd['teacher']
            }
        )
        if created:
            print(f"  ✅ Created classroom: {c.name}")
        created_classes.append(c)

    # 4. Create Students for Form 1 Sciences & Form 2 Arts
    students_f1 = [
        ('Tatenda', 'Chiwenga', 'AGC-2026-001', 'Male', 'Mr. Chiwenga', '+263771000001'),
        ('Blessed', 'Ncube', 'AGC-2026-002', 'Male', 'Mrs. Ncube', '+263771000002'),
        ('Rutendo', 'Moyo', 'AGC-2026-003', 'Female', 'Dr. Moyo', '+263771000003'),
        ('Kudakwashe', 'Ndlovu', 'AGC-2026-004', 'Male', 'Mrs. Ndlovu', '+263771000004'),
        ('Tariro', 'Gumbo', 'AGC-2026-005', 'Female', 'Mr. Gumbo', '+263771000005'),
        ('Nyasha', 'Mhlanga', 'AGC-2026-006', 'Female', 'Mrs. Mhlanga', '+263771000006'),
        ('Farai', 'Mutasa', 'AGC-2026-007', 'Male', 'Mr. Mutasa', '+263771000007'),
        ('Ruvimbo', 'Chikore', 'AGC-2026-008', 'Female', 'Mrs. Chikore', '+263771000008'),
    ]

    for first, last, adm, gender, parent, phone in students_f1:
        s, created = Student.objects.get_or_create(
            admission_number=adm,
            defaults={
                'first_name': first,
                'last_name': last,
                'classroom': created_classes[0],
                'gender': gender,
                'parent_name': parent,
                'parent_phone': phone,
                'is_active': True,
            }
        )
        if created:
            print(f"  ✅ Enrolled student: {s.full_name} in {created_classes[0].name}")

    # 5. Check sample gallery items
    if not GalleryItem.objects.exists():
        g1 = GalleryItem.objects.create(
            title='AbleGod College Science Fair 2026',
            caption='Students demonstrating robotics and physics experiments in the main laboratory.',
            category='academics',
            media_type='image',
            is_featured=True
        )
        g2 = GalleryItem.objects.create(
            title='Annual Athletics & Sports Day Highlights',
            caption='Track and field championships held at the college sports grounds.',
            category='sports',
            media_type='image',
            is_featured=True
        )
        print("  ✅ Created sample gallery items")

    print("\n🎉 Seed completed successfully!")


if __name__ == '__main__':
    seed_data()
