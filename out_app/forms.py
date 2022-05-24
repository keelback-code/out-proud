from django import forms
from .models import Page, ViewerAccess


class WritePageForm(forms.ModelForm):
    """
    Model form for the Creator to create, edit and delete Pages.
    """
    class Meta:
        model = Page
        fields = ('title', 'text_content', 'image', 'link', 'link_title',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)


class AllowViewerForm(forms.ModelForm):
    """
    Model form for the Creator to allow a Viewer to see their Page.
    """
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['allowed_page'].queryset = Page.objects.filter(
                                               creator=request.user)

    class Meta:
        model = ViewerAccess
        fields = ('allowed_page', 'first_name', 'viewer_email', 'shown_name',)

        def form_valid(self, form):
            form.instance.created_by = self.request.user
            return super().form_valid(form)
