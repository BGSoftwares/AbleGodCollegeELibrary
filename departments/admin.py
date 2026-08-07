from django.contrib import admin
from .models import Department, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'created_at')
    list_filter = ('school',)
    search_fields = ('name', 'school__name')
