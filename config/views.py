from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render


def permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)


def health_check(request):
    """Lightweight health endpoint for hosting-platform monitoring."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except Exception:
        return JsonResponse({'status': 'unhealthy'}, status=503)

    return JsonResponse({'status': 'ok'}, status=200)
