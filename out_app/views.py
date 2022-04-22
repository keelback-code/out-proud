from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
from .models import Page, User, ViewerAccess
from .forms import WritePageForm, AllowViewerForm


# view for creator's profile
class CreatorView(generic.ListView):

    # model = Page
    queryset = Page.objects.all()
    template_name = "creator_profile.html"
    paginate_by = 3   


class WritePage(View):

    # def get_form(request):
    #     form = WritePageForm()
    #     return render(request, 'write_page.html', {'form': form})

    # def post_new(request):
    #     if request.method == "POST":
    #         form = WritePageForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             page = form.save()
    #             # page.creator = request.user
    #             # page.save()
    #             return redirect('creator_page', slug=slug)
    #     else:
    #         form = WritePageForm()

    #     return render(request, 'write_page.html', {'form': form})
    
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "write_page.html",
            {
                "page_form": WritePageForm()
            }
        )

    def post(self, request, *args, **kwargs):
        
        page_form = WritePageForm(request.POST, request.FILES)

        if page_form.is_valid():
            write_page = page_form.save(commit=False)
            write_page.user = request.user
            write_page.save()
            return redirect('creator_profile')
        else:
            page_form = WritePageForm()
        
        return render(
            request,
            "write_page.html",
            {
                "page_form": page_form
            }
        )


class AllowViewer(View):

    def get(self, request):
        return render(
            request,
            "allow_viewer.html",
            {
                "viewer_form": AllowViewerForm()
            }
        )

    def post(self, request):
        
        viewer_form = AllowViewerForm(request.POST)

        if viewer_form.is_valid():
            form = viewer_form.save(commit=False)
            form.creator = request.user
            form.save()
        else:
            viewer_form = AllowViewerForm()
        
        return redirect(
            "creator_profile",
            )


class EditPage(UpdateView):
    # model = Page
    fields = ['title', 'text_content', 'image', 'link', 'link_title', 'status']
    template_name = "edit_page.html"
    success_url="/creator_profile"


# class CreatorPage(View):

#     def get(self, request, slug, *args, **kwargs):
#         queryset = Page.objects.all()
#         page = get_object_or_404(queryset, slug=slug)

#         return render(
#             request,
#             "creator_page.html",
#             {
#                 "page": page
#             }
#         )

def creator_page(request, slug):
    page = get_object_or_404(Page, slug=slug)

    return render(
        request,
        "creator_page.html",
        {
            "page": page
        }
    )


def resources(request):
    return render(request, "resources.html")


def landing_page(request):
    return render(request, "index.html")




