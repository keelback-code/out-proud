from .models import Page, Viewer
from django import forms



class WritePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'text_content', 'photo_content', 'video_content', 'link', 'link_title', 'status',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)

class AllowViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = ('viewer_name', 'viewer_email', 'shown_name',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
