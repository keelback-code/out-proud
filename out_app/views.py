from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Page, Viewer
from .forms import CreatorPageForm, ViewerForm


# view for creator's profile
class CreatorView(generic.ListView):
    model = Page
    queryset = Page.objects.order_by('-date')  # show draft and pub to creator
    template_name = "creator_profile.html"
    paginate_by = 3

# view for creator's page
class CreatorPage(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Page.objects.all  # this only shows unpub posts, change
        page_view = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "creator_page.html",
            {
                "page_view": page_view,
                "page_form": CreatorPageForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Page.objects.filter(status=0)  # this only shows unpub posts, change
        page_view = get_object_or_404(queryset, slug=slug)

        page_form = CreatorPageForm(data=request.POST)

        return render(
            request,
            "creator_page.html",
            {
                "page_view": page_view,
                "page_form": CreatorPageForm()
            },
        )

# WIP class for form on own page for allowing viewers, maybe try diff variables for class
class AllowViewer(View):

    form_class = ViewerForm
    initial = { "viewer_form": ViewerForm }
    template_name = "allow_viewer.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, { "viewer_form": ViewerForm })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(
            request, 
            self.template_name, 
            { 
                "viewer_form": ViewerForm 
            }
        )



    # def get(self, request, *args, **kwargs):
    #     viewer_obj = get_object_or_404(Viewer)

    #     return render(
    #             request,
    #             "allow_viewer.html",
    #             {
    #                 "viewer_obj": viewer_obj,
    #                 "viewer_form": ViewerForm()
    #             },
    #         )
    
    # def post(self, request, *args, **kwargs):
    #     viewer_obj = get_object_or_404(Viewer)

    #     viewer_form = ViewerForm(data=request.POST)

    #     return render(
    #             request,
    #             "allow_viewer.html",
    #             {
    #                 "viewer_obj": viewer_obj,
    #                 "viewer_form": ViewerForm()
    #             },
    #         )

class Resources(TemplateView):

    template_name = "resources.html"

    # def resources(request):
    #     return render(request, "resources.html")

class LandingPage(TemplateView):

    template_name = "index.html"
