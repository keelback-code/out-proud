from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Page, Viewer
from .forms import WritePageForm, AllowViewerForm
from .admin import PageAdmin



# view for creator's profile
class CreatorView(generic.ListView):
    model = Page
    template_name = "creator_profile.html"
    paginate_by = 3

# view for creator's page/view of form
# class WritePage(View):

#     def get(self, request, *args, **kwargs):
#         queryset = Page.objects.all()  # this only shows unpub posts, change
#         page_view = get_object_or_404(queryset)

#     def post(self, request, *args, **kwargs):
#         queryset = Page.objects.all()  # this only shows unpub posts, change
#         page_view = get_object_or_404(queryset)

#         page_form = CreatorPageForm(data=request.POST)

#         if page_form.is_valid():
#             # page_form.instance.email = request.user.email
#             # page_form.instance.name = request.user.username
#             # page = page_form.save(commit=False)
#             page = page_form.save()
#             # page.post = post
#             # page.save()
#         else:
#             page_form = CreatorPageForm()
        

#         return render(
#             request,
#             "write_page.html",
#             {
#                 "page_view": page_view,
#                 "page_form": page_form
#             },
#             HttpResponseRedirect('/creator_profile/')
#         )


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



    # def get(self, request, *args, **kwargs):
    #     viewer_obj = get_object_or_404(Viewer)

    #     return render(
    #             request,
    #             "allow_viewer.html",
    #             {
    #                 "viewer_obj": viewer_obj,
    #                 "viewer_form": ViewerForm()
    #             },
    #         )
    
    # def post(self, request, *args, **kwargs):
    #     viewer_obj = get_object_or_404(Viewer)

    #     viewer_form = ViewerForm(data=request.POST)

    #     return render(
    #             request,
    #             "allow_viewer.html",
    #             {
    #                 "viewer_obj": viewer_obj,
    #                 "viewer_form": ViewerForm()
    #             },
    #         )

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
#                 "page": page,
#                 "page_form": WritePageForm 
#             },
#         )

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             page = WritePageForm.save(self)  # commit=False ?
#             # page.save()
            
#         else:
#             page = WritePageForm

#         return render(
#             request, 
#             self.template_name, 
#             {
#                 "page": page,
#                 "page_form": WritePageForm
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
            },
        )

    def post(self, request, *args, **kwargs):

        page_form = WritePageForm(data=request.POST)
        if page_form.is_valid():
            write_page = page_form.save()
        else:
            page_form = WritePageForm()
        
        return render(
            request,
            "creator_profile.html",
            {
                "write_page": write_page
            },
        )


        
class Resources(TemplateView):

    template_name = "resources.html"

    # def resources(request):
    #     return render(request, "resources.html")

class LandingPage(TemplateView):

    template_name = "index.html"


class CreatorPage(TemplateView):

    template_name = "creator_page.html"
