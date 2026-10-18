from django.urls import path
from .views import dashboard, search_books, manage_gallery, delete_gallery_item

urlpatterns = [
    path('', dashboard, name='dashboard-home'),
    path('view/', dashboard, name='dashboard'),
    path('search/', search_books, name='dashboard-search'),
    path('search-books/', search_books, name='search-books'),
    path('gallery/', manage_gallery, name='manage-gallery'),
    path('gallery/<int:item_id>/delete/', delete_gallery_item, name='delete-gallery-item'),
]
