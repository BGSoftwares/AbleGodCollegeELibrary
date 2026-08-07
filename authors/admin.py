from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'website', 'created_at')
    search_fields = ('full_name',)
