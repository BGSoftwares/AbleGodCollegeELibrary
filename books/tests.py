from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from books.models import Book
from categories.models import Category

User = get_user_model()

class ResourceListTests(TestCase):
    def setUp(self):
        # Create a test category
        self.category = Category.objects.create(name="Math")
        
        # Create user
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")
        
        # Create books with different content types
        self.past_paper = Book.objects.create(
            title="Algebra Past Paper 2025",
            isbn="111-222-333",
            content_type="past_exam_paper",
            is_available=True
        )
        self.past_paper.categories.add(self.category)
        
        self.textbook = Book.objects.create(
            title="Calculus Vol 1",
            isbn="444-555-666",
            content_type="textbook",
            is_available=True
        )
        self.textbook.categories.add(self.category)

    def test_past_exam_papers_list(self):
        url = reverse('past-exam-papers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verify it lists the past exam paper
        self.assertContains(response, "Algebra Past Paper 2025")
        # Verify it does NOT list the textbook
        self.assertNotContains(response, "Calculus Vol 1")

    def test_textbooks_notes_list(self):
        url = reverse('textbooks-notes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Verify it lists the textbook
        self.assertContains(response, "Calculus Vol 1")
        # Verify it does NOT list the past exam paper
        self.assertNotContains(response, "Algebra Past Paper 2025")

    def test_management_portal_access(self):
        url = reverse('manage-resources')
        # Anonymous should redirect to login
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Teacher user should have access
        teacher = User.objects.create_user(username="teacher1", email="teacher1@example.com", password="password123", is_teacher=True)
        self.client.login(username="teacher1", password="password123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Resource Management Center")
        self.assertContains(response, "Algebra Past Paper 2025")

    def test_edit_book_view(self):
        teacher = User.objects.create_user(username="teacher2", email="teacher2@example.com", password="password123", is_teacher=True)
        self.client.login(username="teacher2", password="password123")
        url = reverse('edit-book', kwargs={'pk': self.past_paper.pk})
        
        response = self.client.post(url, {
            'title': 'Updated Algebra Past Paper 2025',
            'isbn': self.past_paper.isbn,
            'content_type': 'past_exam_paper',
            'is_available': True,
        })
        self.assertEqual(response.status_code, 302)
        self.past_paper.refresh_from_db()
        self.assertEqual(self.past_paper.title, 'Updated Algebra Past Paper 2025')




    def test_delete_book_view(self):
        teacher = User.objects.create_user(username="teacher3", email="teacher3@example.com", password="password123", is_teacher=True)
        self.client.login(username="teacher3", password="password123")
        url = reverse('delete-book', kwargs={'pk': self.textbook.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=self.textbook.pk).exists())

    def test_login_page_branding(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BG Devops')
        self.assertContains(response, '0784654328')


