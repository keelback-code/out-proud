from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin
from django.views import generic, View
from django import forms
from .models import Page, ViewerAccess
from .forms import WritePageForm, AllowViewerForm 


# def check_viewers(request):
#     """
#     Global function to check if viewer exists in database.
#     """
#     viewer_requested = str(request.user.email)
#     viewers = ViewerAccess.objects.all()

#     for viewer in viewers:
#         viewer_logged_in = str(viewer)
#         if user_logged_in == viewer_logged_in:
#             viewer_access = True
#         else:
#             viewer_access = False

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
            queryset = ViewerAccess.objects.all()

            # Code for lines 81-88, for use in assessing if viewer exists in db, from https://stackoverflow.com/questions/41374782/django-check-if-object-exists

            if viewer_form.is_valid():
                viewer_email = viewer_form.cleaned_data['viewer_email']
                if ViewerAccess.objects.filter(viewer_email=viewer_email).exists():
                    messages.error(request, 'already exists')
                else:
                    instance = viewer_form.save()
                    return redirect('creator_profile')
            
        return render(
             request,
             "allow_viewer.html",
             {
                 "viewer_form": viewer_form
            }
        )


class EditPage(LoginRequiredMixin, View):

    def get(self, request, slug):
        # editor = Page.objects.filter(creator=request.user.username).count() > 0
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

    # user_logged_in = str(request.user.email)
    # viewer_logged_in = ViewerAccess.objects.filter(viewer_email=user_logged_in).count() > 0
    # viewer_access = str(viewer_logged_in)

    user_logged_in = str(request.user.email)
    viewers = ViewerAccess.objects.all()

    for viewer in viewers:
        viewer_logged_in = str(viewer)
        if user_logged_in == viewer_logged_in:
            viewer_access = True
        else:
            viewer_access = False

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

