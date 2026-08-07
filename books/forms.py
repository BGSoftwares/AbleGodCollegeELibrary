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
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mathematics Form 4 Past Paper 2024'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 978-3-16-148410-0 or N/A'}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief description of the resource...'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 4}),
            'departments': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 3}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2024'}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1st Edition / Revised'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 45'}),
            'language': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'English'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'uploaded_by': forms.Select(attrs={'class': 'form-select'}),
        }


