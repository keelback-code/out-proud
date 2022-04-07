from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Page
from .forms import ViewerForm


# view for creator's profile?
class CreatorView(generic.ListView):
    model = Page
    queryset = Page.objects.order_by('-date')  # show draft and pub to creator
    template_name = 'creator_profile.html'
    paginate_by = 3

# view for creator's page
class CreatorPage(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Page.objects.filter(status=0)  # this only shows unpub posts, change
        # queryset = Page.objects.order_by('-date')
        page_view = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "creator_page.html",
            {
                "page_view": page_view,
                "viewer_form": ViewerForm()
            },
        )


# WIP class for form on own page for allowing viewers
# class AllowViewer(View):

#     def get(self, request, *args, **kwargs):
#         queryset = ViewerForm.objects()
#         viewer_form = get_object_or_404(queryset)

#         return render(
#                 request,
#                 "allow_viewer.html",
#                 {
#                     "viewer_form": ViewerForm()
#                 },
#             )
