from django import forms
from .models import Borrowing


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['borrower', 'book', 'due_date', 'is_returned']
