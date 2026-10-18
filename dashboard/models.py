from django.db import models
from django.conf import settings


class GalleryItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Photo / Picture'),
        ('video', 'Video Clip'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'Campus Life & General'),
        ('academics', 'Academics & Science Labs'),
        ('sports', 'Sports & Physical Education'),
        ('events', 'Prize Giving & School Events'),
        ('library', 'Library & Reading Clubs'),
    ]

    title = models.CharField(max_length=200)
    caption = models.TextField(blank=True, help_text='Brief description or caption for the media')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image_file = models.ImageField(upload_to='gallery/images/', blank=True, null=True)
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_uploads')
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gallery Item'
        verbose_name_plural = 'Gallery Items'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.get_media_type_display()})'
