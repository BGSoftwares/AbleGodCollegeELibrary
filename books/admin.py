from django.contrib import admin
from .models import Book, Review, Download, Bookmark, SavedNote


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'content_type', 'publisher', 'is_available', 'created_at')
    list_filter = ('content_type', 'is_available', 'categories', 'publisher')
    search_fields = ('title', 'isbn')
    filter_horizontal = ('authors', 'categories')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'created_at')
    search_fields = ('book__title', 'reviewer__username')


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'downloaded_at')
    search_fields = ('book__title', 'user__username')


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at')
    search_fields = ('book__title', 'user__username')


@admin.register(SavedNote)
class SavedNoteAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at', 'updated_at')
    search_fields = ('book__title', 'user__username', 'content')
