from django.contrib import admin
from .models import Page, ViewerAccess


@admin.register(Page)
class SuperuserPageAdmin(admin.ModelAdmin):
    """
    Class to see pages in the backend.
    """
    list_display = ('title', 'creator',)


@admin.register(ViewerAccess)
class SuperuserViewerAccessAdmin(admin.ModelAdmin):
    """
    Class to see viewers in the backend.
    """
    list_display = ('first_name', 'viewer_email',)
