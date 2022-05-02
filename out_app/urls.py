from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('creator_profile/', views.CreatorProfile.as_view(), name='creator_profile'),
    path('viewer_profile/', views.ViewerProfile.as_view(), name='viewer_profile'),
    path('write_page/', views.WritePage.as_view(), name='write_page'),
    path('creator_page/<slug:slug>/', views.creator_page, name='creator_page'),
    path('allow_viewer/', views.AllowViewer.as_view(), name='allow_viewer'),
    path('resources/', views.resources, name='resources'),
    path('creator_page/edit_page/<slug:slug>/', views.EditPage.as_view(), name='edit_page'),
    path('creator_page/delete_page/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
]
