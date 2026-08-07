from django.db import models
from django.conf import settings
from authors.models import Author
from publishers.models import Publisher
from categories.models import Category


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, default='English')
    CONTENT_TYPE_CHOICES = [
        ('textbook', 'Textbook / Book'),
        ('learning_material', 'Learning Material'),
        ('resource', 'Resource'),
        ('past_exam_paper', 'Past Examination Paper'),
    ]
    content_type = models.CharField(max_length=32, choices=CONTENT_TYPE_CHOICES, null=True, blank=True)
    file = models.FileField(upload_to='books/files/', blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    departments = models.ManyToManyField('departments.Department', related_name='books', blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_books')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f'{self.reviewer} - {self.book}'


class Download(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='downloads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='downloads')
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Download'
        verbose_name_plural = 'Downloads'

    def __str__(self):
        return f'{self.user} - {self.book}'


class Bookmark(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return f'{self.user} - {self.book}'


class SavedNote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='saved_notes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Saved Note'
        verbose_name_plural = 'Saved Notes'

    def __str__(self):
        return f'{self.user} note on {self.book}'
