# File: mini_insta/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/26/2025
# Description: File which pattern matches HTML responses to valid requests to 
# mini_insta/

from django.urls import path
from django.conf import settings
from . import views

# URL patterns for this app:
urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
    path(r'post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
]