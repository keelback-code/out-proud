from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
# from django.views.generic import TemplateView, ListView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from .models import Page, User, ViewerAccess
from .forms import WritePageForm, AllowViewerForm


# view for creator's profile
class CreatorView(generic.ListView):

    # model = Page
    queryset = Page.objects.all()
    template_name = "creator_profile.html"
    paginate_by = 3   


# class CreatorPage(generic.DetailView):
#     model = Page
#     template_name = "creator_page.html"


# class WritePage(LoginRequiredMixin, generic.CreateView):
#     model = Page
#     fields = ['title', 'text_content', 'image', 'link', 'link_title', 'status']
#     form_class = WritePageForm
#     template_name = "write_page.html"

#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super().form_valid(form)


# class EditPage(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
#     model = Page
#     fields = ['title', 'text_content', 'image', 'link', 'link_title', 'status']
#     form_class = WritePageForm
#     template_name = "edit_page.html"
#     success_url ="/"

#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super().form_valid(form)
    
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.creator:
#             return True
#         return False

class WritePage(generic.CreateView):
    
    def get(self, request, *args, **kwargs):

        return render(
            request,
            "write_page.html",
            {"page_form": WritePageForm}
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


# class EditPage(generic.UpdateView):
#     model = Page
#     fields = ['title', 'text_content', 'image', 'link', 'link_title', 'status']
#     template_name = "edit_page.html"
#     success_url ="/"

#     def form_valid(self, form):
#         form.instance.creator = self.request.user
#         return super().form_valid(form)

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
        return render(
            request,
            "edit_page.html",
            {
                "edit_page_form": edit_page_form
            }
        ) 


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

