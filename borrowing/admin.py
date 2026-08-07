from django.contrib import admin
from .models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book', 'borrowed_at', 'due_date', 'is_returned')
    list_filter = ('is_returned', 'borrowed_at')
    search_fields = ('borrower__username', 'book__title')
