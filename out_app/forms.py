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

        # Code for lines 21-25, for use in assessing if viewer exists in db, from https://stackoverflow.com/questions/41374782/django-check-if-object-exists
        
        def clean_viewer_email(self):
            viewer_email = self.cleaned_data['viewer_email']
            if AllowViewerForm.objects.filter(viewer_email=viewer_email).exists():
                raise forms.ValidationError('The email [%s] already exists' % viewer_email)    
            return viewer_email


        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
