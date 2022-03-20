from . import views
from django.urls import path


urlpatterns = [
    path('creator_profile', views.PageList.as_view(), name='creator_profile')
]