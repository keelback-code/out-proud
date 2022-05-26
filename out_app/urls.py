from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
# from django.conf import settings
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('creator_profile/', views.CreatorProfile.as_view(),
         name='creator_profile'),
    path('viewer_profile/', views.ViewerProfile.as_view(),
         name='viewer_profile'),
    path('write_page/', views.WritePage.as_view(), name='write_page'),
    path('creator_page/<slug:slug>/', views.creator_page, name='creator_page'),
    path('allow_viewer/', views.AllowViewer.as_view(), name='allow_viewer'),
    path('resources/', views.resources, name='resources'),
    path('creator_page/edit_page/<slug:slug>/', views.EditPage.as_view(),
         name='edit_page'),
    path('creator_page/delete_page/<slug:slug>/', views.DeletePage.as_view(),
         name='delete_page'),
    path('user_error/', views.error_page, name='user_error'),
    path('email_example/', views.email_example_page, name='email_example'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url(
         'favicon.ico')),),
]
