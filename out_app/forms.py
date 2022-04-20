from .models import Page, User
from django import forms
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField
from django.utils.crypto import get_random_string




class WritePageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('slug', 'creator', 'title', 'text_content', 'image', 'link', 'link_title', 'status',)
        text_content = SummernoteTextField()
        # use | safe when templating summernote
        # summernote_fields = ('text_content',)
        # prepopulated_fields = {'slug': get_random_string}

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)

class AllowViewerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email',)
        # maybe not possible to give a shown name, will come back to this

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
