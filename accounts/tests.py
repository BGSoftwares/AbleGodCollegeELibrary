from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_logout_redirects_to_home(self):
        # Log in first
        self.client.login(username="testuser", password="password123")
        
        # Verify user is logged in
        self.assertIn('_auth_user_id', self.client.session)
        
        # Perform logout request (GET)
        url = reverse('logout')
        response = self.client.get(url)
        
        # Verify redirect to home
        self.assertRedirects(response, reverse('home'))
        
        # Verify user is logged out (session auth keys removed)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_redirects_to_dashboard(self):
        url = reverse('login')
        response = self.client.post(url, {
            'username': 'testuser',
            'password': 'password123'
        })
        # Verify redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))
