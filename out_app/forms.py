from .models import Page, Viewer
from django import forms


class CreatorPageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'text_content', 'photo_content', 'video_content', 'link', 'link_title', 'status',)

class ViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = ('viewer_name', 'viewer_email',)
