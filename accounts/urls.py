from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    register_user, logout_user, manage_teachers, add_teacher,
    edit_teacher, reset_teacher_password, toggle_teacher_status,
    change_password_view
)
from .forms import BeautifulLoginForm

urlpatterns = [
    path('register/', register_user, name='register-user'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=BeautifulLoginForm
    ), name='login'),
    path('logout/', logout_user, name='logout'),

    # Teacher Management (Admin only)
    path('teachers/', manage_teachers, name='manage-teachers'),
    path('teachers/add/', add_teacher, name='add-teacher'),
    path('teachers/<int:user_id>/edit/', edit_teacher, name='edit-teacher'),
    path('teachers/<int:user_id>/reset-password/', reset_teacher_password, name='reset-teacher-password'),
    path('teachers/<int:user_id>/toggle-status/', toggle_teacher_status, name='toggle-teacher-status'),

    # Real-time Password Change (Teachers & Users)
    path('change-password/', change_password_view, name='change-password'),
]
