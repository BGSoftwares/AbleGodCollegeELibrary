from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from books.models import Book
from borrowing.models import Borrowing
from categories.models import Category
from .models import GalleryItem
from .forms import GalleryItemForm
from accounts.permissions import admin_required, teacher_or_librarian_required


@login_required
def dashboard(request):
    books = Book.objects.select_related('publisher', 'uploaded_by').prefetch_related('authors', 'categories').all().order_by('-created_at')
    borrowings = Borrowing.objects.select_related('borrower', 'book').all().order_by('-borrowed_at')[:10]
    
    # Gallery items for the dashboard (photos and videos)
    gallery_items = GalleryItem.objects.filter(is_featured=True).order_by('-created_at')[:12]
    
    # Learning materials uploaded from device
    learning_videos = Book.objects.filter(
        Q(content_type='learning_video') | 
        Q(file__iendswith='.mp4') | 
        Q(file__iendswith='.webm')
    ).order_by('-created_at')[:8]

    study_notes = Book.objects.filter(
        Q(content_type='study_notes') |
        Q(content_type='learning_material')
    ).order_by('-created_at')[:8]

    return render(request, 'dashboard/dashboard.html', {
        'books': books,
        'borrowings': borrowings,
        'gallery_items': gallery_items,
        'learning_videos': learning_videos,
        'study_notes': study_notes,
    })


def home(request):
    featured_books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories')[:6]
    gallery_preview = GalleryItem.objects.filter(is_featured=True).order_by('-created_at')[:6]
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
        'gallery_preview': gallery_preview,
    })


def search_books(request):
    query = request.GET.get('q', '').strip()
    content_filter = request.GET.get('type', '')
    books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories').all()
    
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(isbn__icontains=query) |
            Q(description__icontains=query) |
            Q(authors__full_name__icontains=query)
        ).distinct()
    
    if content_filter:
        books = books.filter(content_type=content_filter)

    return render(request, 'dashboard/search_results.html', {'books': books, 'query': query, 'content_filter': content_filter})


@teacher_or_librarian_required
def manage_gallery(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            if request.user.is_authenticated:
                item.uploaded_by = request.user
            item.save()
            messages.success(request, f'"{item.title}" successfully added to the dashboard gallery from your device!')
            return redirect('manage-gallery')
    else:
        form = GalleryItemForm()

    gallery_items = GalleryItem.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_gallery.html', {
        'form': form,
        'gallery_items': gallery_items
    })


@teacher_or_librarian_required
def delete_gallery_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(GalleryItem, id=item_id)
        title = item.title
        item.delete()
        messages.success(request, f'Gallery media "{title}" removed.')
    return redirect('manage-gallery')
