from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.name
