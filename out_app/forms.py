from .models import Page, ViewerAccess
from django import forms


class WritePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('creator', 'title', 'text_content', 'image', 'link', 'link_title', 'status',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)


class AllowViewerForm(forms.ModelForm):
    class Meta:
        model = ViewerAccess
        fields = ('allowed_page', 'first_name', 'viewer_email', 'shown_name',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
