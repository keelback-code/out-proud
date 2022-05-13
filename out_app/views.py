from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin
from django.views import generic, View
from django import forms
from .models import Page, User, ViewerAccess
from .forms import WritePageForm, AllowViewerForm 


class CreatorProfile(LoginRequiredMixin, generic.ListView):

    queryset = Page.objects.all()
    template_name = "creator_profile.html"
    paginate_by = 3
    ordering = ['title']


class WritePage(LoginRequiredMixin, generic.CreateView):
    
    def get(self, request, *args, **kwargs):

        return render(
            request,
            "write_page.html",
            {
                "page_form": WritePageForm
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
                # "images": image
            }
        )


class AllowViewer(LoginRequiredMixin, generic.CreateView):

    def get(self, request, *args, **kwargs):
        return render(
            request,
            "allow_viewer.html",
            {
                "viewer_form": AllowViewerForm()
            }
        )

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            viewer_form = AllowViewerForm(request.POST)
            if viewer_form.is_valid():
                form = viewer_form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('creator_profile')
            else:
                viewer_form = AllowViewerForm()
                print("else reached")
                return redirect('allow_viewer')
            
        return render(
             request,
             "allow_viewer.html",
             {
                 "viewer_form": viewer_form
            }
        )


class EditPage(LoginRequiredMixin, View):

    def get(self, request, slug):
        editor = Page.objects.filter(creator=request.user.username).count() > 0
        if editor is True:
            page_to_edit = get_object_or_404(Page, slug=slug)
            edit_page_form = WritePageForm(instance=page_to_edit)
            return render(
                request,
                "edit_page.html",
                {
                    "edit_page_form": edit_page_form
                }
            )
        else:
            return redirect('creator_profile')

    def post(self, request, slug):
        
        if Page.creator == request.user:
            if request.method == "POST":
                page_to_edit = get_object_or_404(Page, slug=slug)
                edit_page_form = WritePageForm(request.POST, request.FILES, instance=page_to_edit)
                if edit_page_form.is_valid():
                    edit_page_form.save()
                    return redirect('creator_profile')
                else:
                    return redirect('creator_profile')
        else:
            return redirect('creator_profile')


class DeletePage(LoginRequiredMixin, View):

    def get(self, request, slug):
        page_to_delete = get_object_or_404(Page, slug=slug)
        delete_form = WritePageForm(instance=page_to_delete)

        return render(
            request,
            "delete_page.html",
            {
                "delete_form": delete_form
            }
        ) 

    def post(self, request, slug):

        if request.method == "POST":
            page_to_delete = get_object_or_404(Page, slug=slug)
            delete_form = WritePageForm(request.POST, request.FILES, instance=page_to_delete)
            page_to_delete.delete()
            return redirect('creator_profile')
        else:
            return redirect('creator_profile')


@login_required
def creator_page(request, slug):
    page = get_object_or_404(Page, slug=slug)

    return render(
        request,
        "creator_page.html",
        {
            "page": page
        }
    )


@login_required
def viewer_profile_access(request):

    viewer_access = ViewerAccess.objects.filter(viewer_email=request.user.email).count() > 0

    return render(
        request,
        "viewer_profile.html",
        {
            "viewer_access": viewer_access
        }
    )


def resources(request):
    return render(request, "resources.html")


def landing_page(request):
    return render(request, "index.html")

