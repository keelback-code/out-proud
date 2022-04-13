from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    """
    Class to model Summernote attributes.
    """
    # prepopulated_fields = {'creator': ('User',)}
    # prepopulated_fields = {'slug': (get_random_string,)}
    summernote_fields = ('text_content')
    # list_display = ('title', 'status', 'date')
    # list_filter = ('status', 'date')


# class PageAdmin(admin.ModelAdmin):
#     """
#     Admin Class for pre-filling slugs.
#     """
#     prepopulated_fields = {"slug": ("title",)}
#     prepopulated_fields = {'creator': ('User',)}  # logged in user? should be editable tho
#     # prepopulated_fields = {'slug': (get_random_string,)}   does this work this way?
