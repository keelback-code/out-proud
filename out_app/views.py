from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
# from django.views.generic import TemplateView, ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .models import Page, User, ViewerAccess
from .forms import WritePageForm, AllowViewerForm

# from django.http import HttpResponse
# from cloudinary.forms import cl_init_js_callbacks  


def nav_view(request):

    user_logged_in = request.user.email
    # viewer_logged_in = ViewerAccess.objects.get(id=viewer_email)
    viewer_db = ViewerAccess.objects.filter(viewer_email=user_logged_in)
    print(user_logged_in)
    print(viewer_db[0])
    
    # print(viewer_logged_in)

    # for viewer in viewer_db:
    if user_logged_in == viewer_db[0]:
        viewer_nav_access = True
        print("reached true")
    else:
        viewer_nav_access = False
        print("reached false")

        return render(
            request,
            "viewer_profile.html",
            {
                # "viewer_logged_in": viewer_logged_in,
                # "user_logged_in": user_logged_in,
                "viewer_nav_access": viewer_nav_access
            }
        )
        


# view for creator's profile
class CreatorProfile(generic.ListView):

    queryset = Page.objects.all()
    template_name = "creator_profile.html"
    paginate_by = 3
    ordering = ['title']


# class ViewerProfile(generic.ListView):

#     queryset = ViewerAccess.objects.all()
#     # ViewerAccess.objects.filter(pk='id').exists()
#     template_name = "viewer_profile.html"
#     # paginate_by = 3
#     # ordering = ['title']


class WritePage(generic.CreateView):
    
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
            # send_mail(
            #     request.POST['first_name'],
            #     request.POST['email'],
            #     request.POST['shown_name']
            # )
        else:
            viewer_form = AllowViewerForm()
        
        return redirect(
            "creator_profile",
            )


class EditPage(View):

    def get(self, request, slug):
        page_to_edit = Page.objects.get(slug=slug)
        edit_page_form = WritePageForm(instance=page_to_edit)
        return render(
            request,
            "edit_page.html",
            {
                "edit_page_form": edit_page_form
            }
        )  

    def post(self, request, slug):
        if request.method == "POST":
            page_to_edit = Page.objects.get(slug=slug)
            edit_page_form = WritePageForm(request.POST, request.FILES, instance=page_to_edit)
            if edit_page_form.is_valid():
                edit_page_form.save()
                return redirect('creator_profile')
            else:
                return redirect('creator_profile')

class DeletePage(View):

    def get(self, request, slug):
        page_to_delete = Page.objects.get(slug=slug)
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
            page_to_delete = Page.objects.get(slug=slug)
            delete_form = WritePageForm(request.POST, request.FILES, instance=page_to_delete)
            page_to_delete.delete()
            return redirect('creator_profile')
        else:
            return redirect('creator_profile')


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

