from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    is_student = models.BooleanField(default=False)
    is_staff_member = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False, help_text=_('User must change password on next login'))
    employee_id = models.CharField(max_length=50, blank=True)
    department_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_full_name() or self.username

    def save(self, *args, **kwargs):
        if (self.is_teacher or self.is_staff_member) and (not self.employee_id or not self.employee_id.strip()):
            self.employee_id = generate_next_employee_id()
        super().save(*args, **kwargs)


def generate_next_employee_id():
    import re
    from datetime import datetime
    year = datetime.now().year
    prefix = f"AGC-EMP-"
    existing = User.objects.filter(employee_id__startswith=prefix).values_list('employee_id', flat=True)
    max_num = 0
    for emp in existing:
        m = re.search(r'(\d+)$', emp or '')
        if m:
            try:
                max_num = max(max_num, int(m.group(1)))
            except ValueError:
                pass
    if max_num == 0:
        for emp in User.objects.values_list('employee_id', flat=True):
            m = re.search(r'(\d+)$', emp or '')
            if m:
                try:
                    max_num = max(max_num, int(m.group(1)))
                except ValueError:
                    pass
    return f"{prefix}{max_num + 1:03d}"


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity Logs'

    def __str__(self):
        return f'{self.user} - {self.action}'
