from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from cloudinary.forms import cl_init_js_callbacks
from cloudinary.forms import CloudinaryFileField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms
from .models import Page, User
from .forms import WritePageForm, AllowViewerForm


# view for creator's profile
class CreatorView(generic.ListView):

    model = Page
    template_name = "creator_profile.html"
    paginate_by = 3


class AllowViewer(View):

    form_class = AllowViewerForm
    initial = { "viewer_form": AllowViewerForm }
    template_name = "allow_viewer.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, { "viewer_form": AllowViewerForm })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # if form.is_valid():
        #     # <process form cleaned data>
            

        return render(
            request, 
            self.template_name, 
            {
                "viewer_form": AllowViewerForm 
            },
            # return HttpResponseRedirect('/creator_profile/')
        )


# class WritePage(View):

#     form_class = WritePageForm
#     initial = { "page_form": WritePageForm }
#     template_name = "write_page.html"

#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
        
#         return render(
#             request,
#             self.template_name,
#             {
#                 "page_form": WritePageForm()
#             },
#         )

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             page = WritePageForm.save(self)  # commit=False ?
#             # page.user = request.user
#             # page.save()           
#         else:
#             page = WritePageForm()

#         return render(
#             request, 
#             self.template_name, 
#             {
#                 "page": page
#             },
#             HttpResponseRedirect('/creator_profile/')
#         )


class WritePage(View):

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
        else:
            page_form = WritePageForm()
        
        return render(
            request,
            "creator_profile.html",
            {
                "page_form": page_form
            }
        )


class EditPage(UpdateView):
    model = Page
    fields = ['title', 'text_content', 'image', 'link', 'link_title', 'status']
    template_name = "edit_page.html"
    success_url="/creator_profile"

        
class Resources(TemplateView):

    template_name = "resources.html"

    # def resources(request):
    #     return render(request, "resources.html")


class LandingPage(TemplateView):

    template_name = "index.html"


class CreatorPage(TemplateView):

    template_name = "creator_page.html"

