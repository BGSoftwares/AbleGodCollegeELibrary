from django.urls import path
from .views import dashboard, home, search_books

urlpatterns = [
    path('', home, name='dashboard-home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('search/', search_books, name='search-books'),
]
