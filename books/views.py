from django.db.models import Q
from django.http import FileResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from .forms import BookForm
from .models import Book, SavedNote
from categories.models import Category
from accounts.permissions import teacher_or_librarian_required, student_required
import mimetypes


@teacher_or_librarian_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            if not book.uploaded_by_id:
                book.uploaded_by = request.user
            book.save()
            form.save_m2m()
            return redirect('manage-resources')
    else:
        form = BookForm(initial={'uploaded_by': request.user})
    return render(request, 'books/add_book.html', {'form': form})


@teacher_or_librarian_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manage-resources')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'book': book})


@teacher_or_librarian_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('manage-resources')
    return render(request, 'books/delete_confirm.html', {'book': book})


@teacher_or_librarian_required
def manage_resources(request):
    filter_type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '').strip()

    books_qs = Book.objects.select_related('publisher', 'uploaded_by').prefetch_related('authors', 'categories').order_by('-created_at')

    if filter_type != 'all':
        books_qs = books_qs.filter(content_type=filter_type)

    if search_query:
        books_qs = books_qs.filter(
            Q(title__icontains=search_query) |
            Q(isbn__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(authors__full_name__icontains=search_query)
        ).distinct()

    total_count = Book.objects.count()
    textbook_count = Book.objects.filter(content_type='textbook').count()
    past_exam_count = Book.objects.filter(content_type='past_exam_paper').count()
    learning_material_count = Book.objects.filter(content_type='learning_material').count()
    resource_count = Book.objects.filter(content_type='resource').count()

    context = {
        'books': books_qs,
        'filter_type': filter_type,
        'search_query': search_query,
        'total_count': total_count,
        'textbook_count': textbook_count,
        'past_exam_count': past_exam_count,
        'learning_material_count': learning_material_count,
        'resource_count': resource_count,
    }
    return render(request, 'books/manage_resources.html', context)



def category_resources(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories').filter(categories=category)
    return render(request, 'books/resources_list.html', {
        'books': books,
        'title': category.name,
        'category': category,
    })


def resource_list(request, category_type):
    content_type_map = {
        'past-exam-papers': 'past_exam_paper',
        'textbooks-notes': 'textbook',
        'learning-materials': 'learning_material',
        'other-resources': 'resource',
    }
    page_metadata = {
        'past-exam-papers': {
            'title': 'Past Exam Papers',
            'description': 'Download past exam papers and study materials grouped by subject, year, and exam type.',
            'hero_title': 'Exam-ready study materials',
            'hero_excerpt': 'Access authentic past papers, marking guides, and revision resources to support every learner.',
            'cta_label': 'Upload Past Exam Paper',
            'hero_class': 'past-exam',
        },
        'textbooks-notes': {
            'title': 'Textbooks and Notes',
            'description': 'Browse textbooks, class notes, and academic supplements for every level and subject.',
            'hero_title': 'Textbooks and teacher notes',
            'hero_excerpt': 'Find textbooks and well-organized notes for classroom learning, homework, and revision.',
            'cta_label': 'Upload Textbook or Notes',
            'hero_class': 'textbooks',
        },
        'learning-materials': {
            'title': 'Learning Materials',
            'description': 'Browse teacher notes, revision materials, lesson plans, and worksheets designed to support learning.',
            'hero_title': 'Teacher-led learning resources',
            'hero_excerpt': 'Find high-quality lecture notes, revision guides, and lesson materials for the classroom and home study.',
            'cta_label': 'Upload Learning Material',
            'hero_class': 'learning-materials',
        },
        'other-resources': {
            'title': 'Other Resources',
            'description': 'Discover supplementary files, worksheets, and multimedia study aids for learners and teachers.',
            'hero_title': 'Other classroom resources',
            'hero_excerpt': 'Explore worksheets, guides, and additional learning resources to support active studying.',
            'cta_label': 'Upload Other Resource',
            'hero_class': 'other-resources',
        },
    }
    metadata = page_metadata.get(category_type, page_metadata['other-resources'])
    content_type_key = content_type_map.get(category_type)
    books = Book.objects.select_related('publisher').prefetch_related('authors', 'categories')
    if content_type_key:
        books = books.filter(content_type=content_type_key)
    else:
        books = Book.objects.none()

    content_type_label = None
    if content_type_key:
        content_type_label = content_type_key.replace('_', ' ').title()

    return render(request, 'books/resources_list.html', {
        'books': books,
        'title': metadata['title'],
        'page_description': metadata['description'],
        'hero_title': metadata['hero_title'],
        'hero_excerpt': metadata['hero_excerpt'],
        'cta_label': metadata['cta_label'],
        'page_type': category_type,
        'content_type': content_type_key,
        'content_type_label': content_type_label,
    })


def download_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.file:
        raise Http404('Resource file not found.')
    return FileResponse(book.file.open('rb'), as_attachment=True, filename=book.file.name.split('/')[-1])


def view_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.file:
        raise Http404('Resource file not found.')
    file_path = getattr(book.file, 'path', book.file.name)
    mime_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(book.file.open('rb'), as_attachment=False, content_type=mime_type or 'application/octet-stream')


@student_required
def save_note(request):
    if request.method != 'POST':
        return HttpResponseForbidden('Invalid request method.')

    book_id = request.POST.get('book_id')
    content = request.POST.get('content', '').strip()
    if not book_id or not content:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    book = get_object_or_404(Book, pk=book_id)
    SavedNote.objects.create(book=book, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER', '/'))
