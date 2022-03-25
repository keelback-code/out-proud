from . import views
from django.urls import path
# from out_app.views import PageList


urlpatterns = [
    path('creator_profile/', views.CreatorView.as_view(), name='creator_profile'),
    path('<slug:slug>/', views.CreatorPage.as_view(), name='creator_page'),
]
