from django.db import models


class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        unique_together = ('name', 'school')

    def __str__(self):
        return f'{self.name} ({self.school.name})'
