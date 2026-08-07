from django.contrib import admin
from .models import Role, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_student', 'is_teacher', 'is_staff_member', 'is_active')
    list_filter = ('role', 'is_student', 'is_teacher', 'is_staff_member', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')


from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'created_at')
    search_fields = ('user__username', 'action')
