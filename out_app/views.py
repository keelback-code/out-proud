from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django import forms
from .models import Page, ViewerAccess, User
from .forms import WritePageForm, AllowViewerForm 


# def check_creator_exists(request):  # what do I need this for?
#     """
#     Global function to check if creator exists in database.
#     """
#     creator_requested = request.user
#     creators = Page.objects.filter(creator=request.user)

#     for creator in creators:
#         if str(creator_requested) == str(creator):
#             creator_access = True
#         else:
#             creator_access = False
    
#         return creator_access 


def check_viewer_exists(request):  # do I need this???? if it's only for viewer profile and login is sorted by mixins...
    """
    Global function to check if viewer exists in database.
    """
    viewer_requested = request.user.email
    viewers = ViewerAccess.objects.filter(viewer_email=request.user.email)

    for viewer in viewers:
        if str(viewer_requested) == str(viewer):
            viewer_access = True
        else:
            viewer_access = False
    
        return viewer_access


class CreatorProfile(LoginRequiredMixin, View):
    """
    Class to display pages belonging to logged in creator.
    """
    def get(self, request):
        creator_pages = Page.objects.filter(creator=request.user).values_list('title', flat=True)
        creator_page_list = Page.objects.filter(title__in=creator_pages)

        return render(
            request,
            "creator_profile.html",
            {
                "creator_page_list": creator_page_list
            }
        )
            

class ViewerProfile(LoginRequiredMixin, View):
    """
    Class to display pages assigned to logged in viewer.
    """
    def get(self, request):
        viewer_pages = ViewerAccess.objects.filter(viewer_email=request.user.email).values_list('allowed_page', flat=True)
        viewer_page_list = Page.objects.filter(slug__in=viewer_pages) 

        return render(
            request,
            "viewer_profile.html",
            {
                "viewer_page_list": viewer_page_list,
                "viewer_access": check_viewer_exists(request)
            }
        )


class WritePage(LoginRequiredMixin, generic.CreateView):
    """
    Class to allow users to create a page and commit it to the db.
    """
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
            write_page.creator = request.user
            write_page.save()
            return redirect('landing_page')
        else:
            page_form = WritePageForm()
        
        return render(
            request,
            "write_page.html",
            {
                "page_form": page_form
            }
        )


class EditPage(LoginRequiredMixin, View):
    """
    Class to allow users to update a page.
    """
    def get(self, request, slug):
        page_to_edit = get_object_or_404(Page, slug=slug)
        edit_page_form = WritePageForm(instance=page_to_edit)
        if page_to_edit.creator == request.user:
            return render(
                request,
                "edit_page.html",
                {
                    "edit_page_form": edit_page_form
                }
            )
        else:
            return redirect('landing_page')

    def post(self, request, slug):
        page_to_edit = get_object_or_404(Page, slug=slug)
        print(page_to_edit.slug)
        edit_page_form = WritePageForm(request.POST, request.FILES, instance=page_to_edit)
        if page_to_edit.creator == request.user:  
            if request.method == "POST":
                if edit_page_form.is_valid():
                    final_save = edit_page_form.save(commit=False)
                    final_save.slug = page_to_edit.slug
                    print(page_to_edit.slug)
                    # print(edit_page_form.slug)
                    print(final_save.slug)
                    final_save.save()
                    return redirect('landing_page')
                else:
                    return redirect('landing_page')


class DeletePage(LoginRequiredMixin, View):
    """
    Class to allow users to delete a page.
    """
    def get(self, request, slug):
        page_to_delete = get_object_or_404(Page, slug=slug)
        delete_form = WritePageForm(instance=page_to_delete)
        if page_to_delete.creator == request.user:
            return render(
                request,
                "delete_page.html",
                {
                    "delete_form": delete_form
                }
            ) 
        else:
            return redirect('landing_page')

    def post(self, request, slug):
        if request.method == "POST":
            page_to_delete = get_object_or_404(Page, slug=slug)
            delete_form = WritePageForm(request.POST, request.FILES, instance=page_to_delete)
            if page_to_delete.creator == request.user: 
                page_to_delete.delete()
                return redirect('landing_page')
            else:
                return redirect('landing_page')


class AllowViewer(LoginRequiredMixin, generic.CreateView):
    """
    Class to give a Viewer access to a creator's page; also contains
    a function to check for existing emails in the Viewer db.
    """
    def get(self, request, *args, **kwargs):      
        viewer_form = AllowViewerForm(request)

        return render(
            request,
            "allow_viewer.html",
            {
                "viewer_form": viewer_form
            }
        )

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            viewer_form = AllowViewerForm(request, request.POST)

            # Code for lines 180-186, for use in assessing if viewer exists in db, from:
            # https://stackoverflow.com/questions/41374782/django-check-if-object-exists

            if viewer_form.is_valid():
                viewer_email = viewer_form.cleaned_data['viewer_email']
                if ViewerAccess.objects.filter(viewer_email=viewer_email).exists():
                    messages.error(request, 'already exists')
                else:
                    instance = viewer_form.save()
                    return redirect('landing_page')
            
        return render(
             request,
             "allow_viewer.html",
             {
                 "viewer_form": viewer_form
            }
        )


@login_required
def creator_page(request, slug):
    """
    Function to retrieve a creator's page dynamically.
    """
    page = get_object_or_404(Page, slug=slug)

    return render(
        request,
        "creator_page.html",
        {
            "page": page
        }
    )

def resources(request):
    """
    Function to retrieve the Resources page.
    """
    return render(request, "resources.html")


def landing_page(request):
    """
    Function to retrieve the Resources page.
    """
    return render(request, "index.html")

