from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'is_student', 'is_teacher', 'is_staff_member')


class BeautifulLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg login-input',
            'placeholder': 'Username or Email',
            'autocomplete': 'username',
        }),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg login-input',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        }),
        label='Password'
    )
