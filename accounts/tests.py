from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin = User.objects.create_superuser(username="adminuser", password="AdminPassword123!", email="admin@example.com")
        self.teacher = User.objects.create_user(
            username="teacher1",
            password="Teacher@2026",
            email="teacher1@example.com",
            is_teacher=True,
            is_staff=True,
            must_change_password=True
        )

    def test_logout_redirects_to_home(self):
        self.client.login(username="testuser", password="password123")
        self.assertIn('_auth_user_id', self.client.session)
        url = reverse('logout')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('home'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_redirects_to_dashboard(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_admin_can_access_teacher_management(self):
        self.client.login(username="adminuser", password="AdminPassword123!")
        response = self.client.get(reverse('manage-teachers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "teacher1")

    def test_admin_reset_teacher_password_realtime(self):
        self.client.login(username="adminuser", password="AdminPassword123!")
        url = reverse('reset-teacher-password', kwargs={'user_id': self.teacher.id})
        response = self.client.post(url, {
            'new_password': 'NewTemporaryPass2026!',
            'force_change': True
        })
        self.assertRedirects(response, reverse('manage-teachers'))

        # Verify password synced immediately in real time
        self.teacher.refresh_from_db()
        self.assertTrue(self.teacher.check_password('NewTemporaryPass2026!'))
        self.assertTrue(self.teacher.must_change_password)

    def test_teacher_can_change_password_and_clear_flag(self):
        self.client.login(username="teacher1", password="Teacher@2026")
        url = reverse('change-password')
        response = self.client.post(url, {
            'old_password': 'Teacher@2026',
            'new_password': 'MyStrongPersonalPass123!',
            'confirm_password': 'MyStrongPersonalPass123!',
        })
        self.assertRedirects(response, reverse('dashboard-home'))

        self.teacher.refresh_from_db()
        self.assertTrue(self.teacher.check_password('MyStrongPersonalPass123!'))
        self.assertFalse(self.teacher.must_change_password)
