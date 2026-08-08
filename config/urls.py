from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home
from config.views import health_check

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('books/', include('books.urls')),
    path('borrowings/', include('borrowing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'config.views.permission_denied_view'
