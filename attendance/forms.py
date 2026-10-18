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
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'admission_number', 'classroom', 'gender', 'parent_name', 'parent_phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'admission_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AGC-2026-001'}),
            'classroom': forms.Select(attrs={'class': 'form-select'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Parent / Guardian Name'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +263 77 123 4567'}),
        }
