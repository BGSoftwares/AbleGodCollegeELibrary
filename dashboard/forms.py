from django import forms
from .models import GalleryItem


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'caption', 'category', 'media_type', 'image_file', 'video_file', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Annual Speech & Prize Giving Day 2026'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description or caption...'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'media_type': forms.Select(attrs={'class': 'form-select', 'id': 'id_media_type'}),
            'image_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'video_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'video/mp4,video/webm,video/ogg'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        image_file = cleaned_data.get('image_file')
        video_file = cleaned_data.get('video_file')

        if media_type == 'image' and not image_file:
            raise forms.ValidationError('Please choose an image file from your device.')
        if media_type == 'video' and not video_file:
            raise forms.ValidationError('Please choose a video file (MP4/WebM) from your device.')

        return cleaned_data
