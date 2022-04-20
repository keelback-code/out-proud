from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.crypto import get_random_string
from .models import Page, User


@admin.register(Page)
class SuperuserAdmin(admin.ModelAdmin):
    """
    Class to see pages in the backend.
    """
    list_display = ('title', 'status',)
    list_filter = ('status',)
    # prepopulated_fields = {'creator': ('User',)}  # logged in user? should be editable tho
    
    

#@admin.register(Viewer)



# class PageAdmin(admin.ModelAdmin):
#     """
#     Admin Class for pre-filling slugs.
#     """
#     model = Page
    # prepopulated_fields = {'creator': ('User',)}  # logged in user? should be editable tho
    # prepopulated_fields = {'slug': (get_random_string)}


# class SummernotePageAdmin(SummernoteModelAdmin):
#     """
#     Admin Class for specifying summernote fields.
#     """
#     model = Page
#     summernote_fields = ('text_content')
