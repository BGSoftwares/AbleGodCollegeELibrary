from django.db import models
from django.conf import settings
from django.utils import timezone


class ClassRoom(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text='e.g. Form 1 Sciences, Form 2 Arts, Form 4 Commercials')
    grade_level = models.CharField(max_length=50, default='Form 1')
    stream = models.CharField(max_length=50, blank=True, help_text='e.g. Sciences, Arts, Commercials')
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_classes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Class Room'
        verbose_name_plural = 'Class Rooms'
        ordering = ['grade_level', 'name']

    def __str__(self):
        return self.name

    @property
    def total_students(self):
        return self.students.filter(is_active=True).count()


class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=50, unique=True, help_text='e.g. AGC-2026-001')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='students')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    parent_name = models.CharField(max_length=150, blank=True)
    parent_phone = models.CharField(max_length=30, blank=True, help_text='Phone number for WhatsApp attendance sharing')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.admission_number})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class AttendanceSession(models.Model):
    SESSION_TYPE_CHOICES = [
        ('Morning', 'Morning Roll Call'),
        ('Afternoon', 'Afternoon Session'),
        ('Subject', 'Subject Period'),
    ]

    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='attendance_sessions')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendances')
    date = models.DateField(default=timezone.now)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPE_CHOICES, default='Morning')
    notes = models.TextField(blank=True, help_text='Teacher remarks or comments about the class attendance')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'
        ordering = ['-date', '-created_at']
        unique_together = ('classroom', 'date', 'session_type')

    def __str__(self):
        return f'{self.classroom.name} - {self.date} ({self.session_type})'

    @property
    def total_records(self):
        return self.records.count()

    @property
    def present_count(self):
        return self.records.filter(status='present').count()

    @property
    def absent_count(self):
        return self.records.filter(status='absent').count()

    @property
    def late_count(self):
        return self.records.filter(status='late').count()

    @property
    def excused_count(self):
        return self.records.filter(status='excused').count()

    @property
    def attendance_percentage(self):
        total = self.total_records
        if total == 0:
            return 0
        return round((self.present_count / total) * 100, 1)


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='present')
    remarks = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('session', 'student')

    def __str__(self):
        return f'{self.student} - {self.status}'
