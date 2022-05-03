from django.contrib import admin
# from django_summernote.admin import SummernoteModelAdmin
# from django.utils.crypto import get_random_string
from .models import Page, User, ViewerAccess


@admin.register(Page)
class SuperuserPageAdmin(admin.ModelAdmin):
    """
    Class to see pages in the backend.
    """
    list_display = ('title', 'status',)
    list_filter = ('status',)


@admin.register(ViewerAccess)
class SuperuserViewerAccessAdmin(admin.ModelAdmin):
    """
    Class to see viewers in the backend.
    """
    list_display = ('first_name', 'viewer_email',)





# class PageAdmin(admin.ModelAdmin):
#     """
#     Admin Class for pre-filling slugs.
#     """
#     model = Page
    # prepopulated_fields = {'creator': ('User',)}  # logged in user? should be editable tho
    # prepopulated_fields = {'slug': (get_random_string)}


