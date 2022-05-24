from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic, View
from .models import Page, ViewerAccess
from .forms import WritePageForm, AllowViewerForm


def check_viewer_exists(request):
    """
    Global function to check if viewer exists in database.
    """
    if request.user.is_active:
        viewer_requested = request.user.email
        viewers = ViewerAccess.objects.filter(viewer_email=request.user.email)
        for viewer in viewers:
            if str(viewer_requested) == str(viewer):
                viewer_access = True
            else:
                viewer_access = False

            return viewer_access
    else:
        return redirect('accounts/signup/')


class CreatorProfile(LoginRequiredMixin, View):
    """
    Class to display pages belonging to logged in creator.
    """
    def get(self, request):
        creator_pages = Page.objects.filter(creator=request.user) \
                        .values_list('title', flat=True)
        creator_page_list = Page.objects.filter(title__in=creator_pages)

        return render(
            request,
            "creator_profile.html",
            {
                "creator_page_list": creator_page_list,
                "viewer_access": check_viewer_exists(request)
            }
        )


class ViewerProfile(LoginRequiredMixin, View):
    """
    Class to display pages assigned to logged in viewer.
    """
    def get(self, request):
        v_pages = ViewerAccess.objects.filter(viewer_email=request.user.email)\
                  .values_list('allowed_page', flat=True)
        viewer_page_list = Page.objects.filter(slug__in=v_pages)

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
                "page_form": WritePageForm,
                "viewer_access": check_viewer_exists(request)
            }
        )

    def post(self, request, *args, **kwargs):
        page_form = WritePageForm(request.POST, request.FILES)
        if page_form.is_valid():
            write_page = page_form.save(commit=False)
            write_page.creator = request.user
            write_page.save()
            messages.success(request, 'Page created successfully.')
            return redirect('landing_page')
        else:
            messages.error(request, 'Page not saved, please try again.')
            page_form = WritePageForm()

        return render(
            request,
            "write_page.html",
            {
                "page_form": page_form,
                "viewer_access": check_viewer_exists(request)
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
                    "edit_page_form": edit_page_form,
                    "viewer_access": check_viewer_exists(request)
                }
            )
        else:
            return redirect('user_error')

    def post(self, request, slug):
        page_to_edit = get_object_or_404(Page, slug=slug)
        print(page_to_edit.slug)
        edit_page_form = WritePageForm(
                         request.POST, request.FILES, instance=page_to_edit)
        # edit_page_form.slug = page_to_edit.slug
        # print(edit_page_form.slug)
        if page_to_edit.creator == request.user:
            if edit_page_form.is_valid():
                edit_page_form.save()
                # final_save = edit_page_form.save(commit=False)
                # final_save.slug = page_to_edit.slug
                # print(page_to_edit.slug)
                # print(final_save.slug)
                # final_save.save()
                messages.success(request, 'Page updated successfully.')
                return redirect('landing_page')
            else:
                messages.error(request,
                               'Update unsuccessful, please try again.')
                return redirect('user_error')


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
                    "delete_form": delete_form,
                    "viewer_access": check_viewer_exists(request)
                }
            )
        else:
            return redirect('user_error')

    def post(self, request, slug):
        page_to_delete = get_object_or_404(Page, slug=slug)
        delete_form = WritePageForm(request.POST,
                                    request.FILES, instance=page_to_delete)
        if page_to_delete.creator == request.user:
            page_to_delete.delete()
            messages.success(request, 'Page deleted successfully.')
            return redirect('landing_page')
        else:
            messages.error(request, 'Delete unsuccessful, please try again.')
            return redirect('user_error')


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
                "viewer_form": viewer_form,
                "viewer_access": check_viewer_exists(request)
            }
        )

    def post(self, request, *args, **kwargs):
        viewer_form = AllowViewerForm(request, request.POST)

        # Code for lines 199-207, to see if viewer exists in db, from:
        # https://stackoverflow.com/questions/41374782/django-check-if-object-exists

        if viewer_form.is_valid():
            viewer_email = viewer_form.cleaned_data['viewer_email']
            if ViewerAccess.objects.filter(
                    viewer_email=viewer_email).exists():
                messages.error(request, 'already exists')
            else:
                viewer_form.save()
                messages.success(request, 'Viewer emailed successfully.')
                return redirect('landing_page')

        return render(
             request,
             "allow_viewer.html",
             {
                 "viewer_form": viewer_form,
                 "viewer_access": check_viewer_exists(request)
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
            "page": page,
            "viewer_access": check_viewer_exists(request)
        }
    )


def resources(request):
    """
    Function to retrieve the Resources page.
    """
    return render(
        request,
        "resources.html",
        {
            "viewer_access": check_viewer_exists(request)
        }
    )


def landing_page(request):
    """
    Function to retrieve the Landing page.
    """
    return render(
        request,
        "index.html",
        {
            "viewer_access": check_viewer_exists(request)
        }
    )


def error_page(request):
    """
    Function to retrieve the error page.
    """
    return render(
        request,
        "user_error.html",
        {
            "viewer_access": check_viewer_exists(request)
        }
    )
