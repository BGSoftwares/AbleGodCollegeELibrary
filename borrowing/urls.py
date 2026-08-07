from django.urls import path
from .views import add_borrowing

urlpatterns = [
    path('add/', add_borrowing, name='add-borrowing'),
]
