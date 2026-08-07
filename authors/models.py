from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    biography = models.TextField(blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.full_name
