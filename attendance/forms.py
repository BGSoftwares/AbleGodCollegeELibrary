from django import forms
from .models import ClassRoom, Student, AttendanceSession


class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'grade_level', 'stream', 'class_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Form 1 Sciences'}),
            'grade_level': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Form 1'}),
            'stream': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sciences'}),
            'class_teacher': forms.Select(attrs={'class': 'form-select'}),
        }


class StudentForm(forms.ModelForm):
    admission_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Auto-generated next ID if blank (e.g. AGC-2026-001)'
        })
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'admission_number', 'classroom', 'gender', 'parent_name', 'parent_phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent / Guardian Name'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +263 77 123 4567'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and not self.initial.get('admission_number'):
            from .models import generate_next_admission_number
            self.initial['admission_number'] = generate_next_admission_number()
