# File: mini_insta/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/3/2025
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
    path(r'profile/<int:pk>/create_post', views.CreatePostView.as_view(), name="create_post"),
    path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path(r'post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post"),
    path(r'profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path(r'profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name="show_following"),
]