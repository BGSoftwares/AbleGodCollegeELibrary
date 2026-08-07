from django.contrib.auth import views as auth_views
from django.urls import path
from .views import register_user, logout_user
from .forms import BeautifulLoginForm

urlpatterns = [
    path('register/', register_user, name='register-user'),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=BeautifulLoginForm
    ), name='login'),
    path('logout/', logout_user, name='logout'),
]
