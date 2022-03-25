from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Page


# view for creator's profile?
class CreatorView(generic.ListView):
    model = Page
    queryset = Page.objects.order_by('-date')  # show draft and pub to creator
    template_name = 'creator_profile.html'
    paginate_by = 3

# view for creator's page
class CreatorPage(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Page.objects.filter(status=1)  # this only shows pub posts, appropriate? test and see
        post = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "creator_page.html",
        )
