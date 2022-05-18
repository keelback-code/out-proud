from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  # UserPassesTestMixin
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

        queryset = Page.objects.all()
        template_name = "creator_profile.html"
        paginate_by = 3
        ordering = ['title']

        # add viewer_access context

        # return render(
        #     request,
        #     "creator_profile.html",
        #     {
        #         "viewer_access": viewer_access
        #     }
        # )


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
        # editor = Page.objects.filter(creator=request.user.username).count() > 0
        if Page.creator == request.user:  # not working yet
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
        
        if Page.creator == request.user:  # not working yet
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


class AllowViewer(LoginRequiredMixin, generic.CreateView):
    """
    Class to allow Viewers; contains get and post functions, as well
    as a function to allow only Pages for the logged in user to be seen in the dropdown.
    """

    def get(self, request, *args, **kwargs):
       # only ready to send should show eg status=1
        # preferred_dropdown = Page.objects.filter(creator=request.user)

        # viewer_form = AllowViewerForm(initial=Page.objects.filter(creator=request.user))

        # related_page = Page.objects.filter(creator=request.user)

     
        # print(related_page)
        # # for x in related_creator:
        # if related_page in related_creator:
        #     print("here")
        # else:
        #     print("not here")
            # print(x)
            # print(related_creator)
            # st_x = str(x)
            # if related_page == st_x:
            #     print("yup")
            # else:
            #     print("nope")
            

        return render(
            request,
            "allow_viewer.html",
            {
                "viewer_form": AllowViewerForm()
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

    user_logged_in = str(request.user.email)
    viewers = ViewerAccess.objects.all()
    for viewer in viewers:
        viewer_logged_in = str(viewer)  # change str to be around == line?
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

