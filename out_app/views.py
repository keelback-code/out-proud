from django.shortcuts import render
from django.views import generic
from .models import Page


# view for creator's profile?
class PageList(generic.ListView):
    model = Page
    queryset = Page.objects.order_by('-date')  # show draft and pub to creator
    template_name = 'creator_profile.html'
    paginate_by = 3
