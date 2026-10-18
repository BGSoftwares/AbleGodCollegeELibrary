from django.urls import path
from .views import (
    attendance_dashboard, take_attendance, attendance_session_detail,
    manage_classes, manage_students
)

urlpatterns = [
    path('', attendance_dashboard, name='attendance-dashboard'),
    path('take/<int:classroom_id>/', take_attendance, name='take-attendance'),
    path('session/<int:session_id>/', attendance_session_detail, name='attendance-session-detail'),
    path('classes/', manage_classes, name='manage-classes'),
    path('classes/<int:classroom_id>/students/', manage_students, name='manage-students'),
]
