from .models import Page, ViewerAccess
from django import forms
# from django.utils.crypto import get_random_string


class WritePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('slug', 'creator', 'title', 'text_content', 'image', 'link', 'link_title', 'status',)
        # prepopulated_fields = {'slug': get_random_string}

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
