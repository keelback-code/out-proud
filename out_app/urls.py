from . import views
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('creator_profile/', views.CreatorView.as_view(), name='creator_profile'),
    path('creator_page/<slug:slug>/', views.CreatorPage.as_view(), name='creator_page'),
    path('allow_viewer/', views.AllowViewer.as_view(), name='allow_viewer'),
    path('resources/', TemplateView.as_view(template_name='resources.html')),
]
