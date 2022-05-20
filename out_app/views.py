from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic, View
from django import forms
from .models import Page, ViewerAccess, User
from .forms import WritePageForm, AllowViewerForm 


def check_creator_exists(request):
    """
    Global function to check if creator exists in database.
    """
    creator_requested = request.user
    creators = Page.objects.filter(creator=request.user)

    for creator in creators:
        if str(creator_requested) == str(creator):
            creator_access = True
        else:
            creator_access = False
    
        return creator_access


def check_viewer_exists(request):
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

# def get_user_pages(Klass, request):
#     """
#     Global function for retrieving pages belonging to a creator.
#     """
#     user = request.user
#     page_list = Klass.objects.filter(user=user).values_list('title', flat=True)
#     return Klass.objects.filter(title__in=page_list)

    # viewer_page_list = ViewerAccess.objects.filter(viewer_email=request.user.email).values_list('allowed_page', flat=True) # gets viewer pages assocuated with logged in viewer
    # # viewer_pages = ViewerAccess.objects.filter(allowed_page__in=viewer_page_list) # just gets emails
    # # print(viewer_pages)
    # print(viewer_page_list)


class CreatorProfile(LoginRequiredMixin, View):

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


class EditPage(LoginRequiredMixin, View):

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
            return redirect('creator_profile')

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
                    return redirect('creator_profile')
                else:
                    return redirect('creator_profile')


class DeletePage(LoginRequiredMixin, View):
    # needs to check for ownership
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
            return redirect('creator_profile')

    def post(self, request, slug):
        if request.method == "POST":
            page_to_delete = get_object_or_404(Page, slug=slug)
            delete_form = WritePageForm(request.POST, request.FILES, instance=page_to_delete)
            if page_to_delete.creator == request.user: 
                page_to_delete.delete()
                return redirect('creator_profile')
            else:
                return redirect('creator_profile')


class AllowViewer(LoginRequiredMixin, generic.CreateView):
    """
    Class to allow Viewers; contains get and post functions, as well
    as a function to check for existing emails in the Viewer db.
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
                    return redirect('creator_profile')
            
        return render(
             request,
             "allow_viewer.html",
             {
                 "viewer_form": viewer_form
            }
        )


@login_required
def viewer_profile_access(request):

    creator_page_list = Page.objects.filter(creator=request.user).values_list('title', flat=True)
    creator_pages = Page.objects.filter(title__in=creator_page_list)
    print(creator_pages)

   
    viewer_page_list = ViewerAccess.objects.filter(viewer_email=request.user.email).values_list('allowed_page', flat=True) # gets viewer pages assocuated with logged in viewer
    # viewer_pages = ViewerAccess.objects.filter(allowed_page__in=viewer_page_list) # just gets emails
    # print(viewer_pages)
    print(viewer_page_list)



    return render(
        request,
        "viewer_profile.html",
        {
            "viewer_access": check_viewer_exists(request)
        }
    )

@login_required
def creator_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    # viewer_profile_access(request)
    # check_viewer_exists(request)

    return render(
        request,
        "creator_page.html",
        {
            "page": page,
            "viewer_access": check_viewer_exists(request)
        }
    )

def resources(request):
    return render(request, "resources.html")


def landing_page(request):
    return render(request, "index.html")

