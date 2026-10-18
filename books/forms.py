import time
from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        optional_fields = ['uploaded_by', 'authors', 'categories', 'publisher', 'departments', 'language', 'isbn', 'publication_year', 'edition', 'page_count']
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False

    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'content_type', 'description', 
            'authors', 'publisher', 'categories', 'departments',
            'publication_year', 'edition', 'page_count', 'language', 
            'cover_image', 'file', 'is_available', 'uploaded_by'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics Form 3 Lab Demonstration or Biology Notes'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional (leave blank to auto-generate code)'}),
            'content_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_content_type'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description of the video, notes, or learning material...'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'departments': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 3}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2026'}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2026 Revision / Lesson 4'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 15'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'video/mp4,video/webm,video/ogg,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/zip,audio/mpeg'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uploaded_by': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '').strip()
        if not isbn:
            # Auto generate unique code for uploaded device materials
            isbn = f"AGC-{int(time.time()*1000)%100000000:08d}"
        return isbn
