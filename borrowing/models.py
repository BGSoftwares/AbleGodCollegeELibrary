from django.db import models
from django.conf import settings
from books.models import Book


class Borrowing(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowings')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Borrowing'
        verbose_name_plural = 'Borrowings'

    def __str__(self):
        return f'{self.borrower} - {self.book}'
