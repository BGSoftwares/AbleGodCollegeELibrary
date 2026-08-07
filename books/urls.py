from django.urls import path
from .views import (
    add_book, category_resources, delete_book, download_book, 
    edit_book, manage_resources, resource_list, save_note, view_book
)

urlpatterns = [
    path('add/', add_book, name='add-book'),
    path('manage/', manage_resources, name='manage-resources'),
    path('edit/<int:pk>/', edit_book, name='edit-book'),
    path('delete/<int:pk>/', delete_book, name='delete-book'),
    path('category/<int:pk>/', category_resources, name='category-resources'),
    path('past-exam-papers/', resource_list, {'category_type': 'past-exam-papers'}, name='past-exam-papers'),
    path('textbooks-notes/', resource_list, {'category_type': 'textbooks-notes'}, name='textbooks-notes'),
    path('learning-materials/', resource_list, {'category_type': 'learning-materials'}, name='learning-materials'),
    path('other-resources/', resource_list, {'category_type': 'other-resources'}, name='other-resources'),
    path('download/<int:pk>/', download_book, name='download-book'),
    path('save-note/', save_note, name='save-note'),
    path('view/<int:pk>/', view_book, name='view-book'),
]
