from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    """
    Class to model Summernote attributes.
    """
    # prepopulated_fields = {'creator': ('User',)} logged in user? should be editable tho
    # prepopulated_fields = {'page_code': (get_random_string,)} does this work this way?
    summernote_fields = ('text_content')
    list_display = ('title', 'status', 'date')
    list_filter = ('status', 'date')
