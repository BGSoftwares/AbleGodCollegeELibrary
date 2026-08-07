from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from books.models import Book
from borrowing.models import Borrowing
from categories.models import Category


@login_required
def dashboard(request):
    books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories').all()
    borrowings = Borrowing.objects.select_related('borrower', 'book').all()
    return render(request, 'dashboard/dashboard.html', {'books': books, 'borrowings': borrowings})


def home(request):
    featured_books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories')[:6]
    categories = []
    color_classes = ['subject-icon-color-1', 'subject-icon-color-2', 'subject-icon-color-3', 'subject-icon-color-4', 'subject-icon-color-5', 'subject-icon-color-6']
    for index, category in enumerate(Category.objects.all()):
        categories.append({
            'pk': category.pk,
            'name': category.name,
            'description': category.description,
            'color_class': color_classes[index % len(color_classes)],
        })

    return render(request, 'home.html', {
        'title': 'AbleGod College E-Library',
        'featured_books': featured_books,
        'categories': categories,
    })


def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.none()
    if query:
        books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories').filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__full_name__icontains=query)
        ).distinct()
    else:
        books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories').all()
    return render(request, 'dashboard/search_results.html', {'books': books, 'query': query})
