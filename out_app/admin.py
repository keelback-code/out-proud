from django.contrib import admin
from .models import Page
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):

    summernote_fields = ('text_content')
