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


class CreatorProfile(LoginRequiredMixin, generic.ListView):

        # queryset = Page.objects.all()
        model = Page
        template_name = "creator_profile.html"
        paginate_by = 3
        ordering = ['title']

        # def get_context_data(self, **kwargs):
        #     context = super().get_context_data(**kwargs)
        #     context["viewer_access"] = check_viewer_exists
        #     return context


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
        edit_page_form = WritePageForm(request.POST, request.FILES, instance=page_to_edit)  # in here somewhere?
        if page_to_edit.creator == request.user:  
            if request.method == "POST":
                if edit_page_form.is_valid():
                    edit_page_form.save()  # duplicate pages?
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


class AllowViewer(LoginRequiredMixin, generic.CreateView):
    """
    Class to allow Viewers; contains get and post functions, as well
    as a function to allow only Pages for the logged in user to be seen in the dropdown.
    """

    def get(self, request, *args, **kwargs):

        # viewer_form = AllowViewerForm(initial=Page.objects.filter(creator=request.user))
       
        viewer_form = AllowViewerForm()

        
        # related_page = viewer_form['allowed_page'](initial=Page.objects.filter(creator=request.user))

        # viewer_form = AllowViewerForm(instance=related_page)

        page_options = viewer_form['allowed_page']
        print(page_options)
        creator_pages = Page.objects.filter(creator=request.user)
        print(creator_pages)
        
        for options in creator_pages:
            if str(page_options) == str(options):
                print("true")
            else:
                print("false")
        
            # return viewer_access


        return render(
            request,
            "allow_viewer.html",
            {
                "viewer_form": viewer_form
                # "page_dropdown": page_dropdown
            }
        )

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            viewer_form = AllowViewerForm(request.POST)

            # Code for lines 139-145, for use in assessing if viewer exists in db, from:
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

    return render(
        request,
        "viewer_profile.html",
        {
            "viewer_access": check_viewer_exists
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

