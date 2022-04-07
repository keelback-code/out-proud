from .models import Viewer
from django import forms


class ViewerForm(forms.ModelForm):
    class Meta:
        model = Viewer
        fields = ('viewer_name', 'viewer_email',)
