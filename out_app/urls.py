from . import views
from django.urls import path


urlpatterns = [
    path('creator_profile/', views.CreatorView.as_view(), name='creator_profile'),
    path('creator_page/<slug:slug>/', views.CreatorPage.as_view(), name='creator_page'),
    path('allow_viewer/', views.AllowViewer.as_view(), name='allow_viewer'),
]
