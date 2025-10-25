# File: mini_insta/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/17/2025
# Description: File which pattern matches HTML responses to valid requests to 
# mini_insta/

from django.urls import path
from django.conf import settings
from . import views

from django.contrib.auth import views as auth_views

# URL patterns for this app:
urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
    path(r'post/<int:pk>', views.PostDetailView.as_view(), name="show_post"),
    path(r'profile/create_post', views.CreatePostView.as_view(), name="create_post"),
    path(r'profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'post/<int:pk>/delete', views.DeletePostView.as_view(), name="delete_post"),
    path(r'post/<int:pk>/update', views.UpdatePostView.as_view(), name="update_post"),
    path(r'profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name="show_followers"),
    path(r'profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name="show_following"),
    path(r'profile/feed', views.PostFeedListView.as_view(), name="show_feed"),
    path(r'profile/search_results', views.SearchView.as_view(), name="search"),
    path(r'login/', auth_views.LoginView.as_view(template_name="mini_insta/login.html"), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path(r'logout_confirmation', views.LoggedOutView.as_view(), name="logout_confirmation"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/follow', views.CreateFollowView.as_view(), name="create_follow"),
    path(r'post/<int:pk>/like', views.PostDetailView.as_view(), name='create_like'),
    path(r'profile/<int:pk>/delete_follow', views.ProfileDetailView.as_view(), name="delete_follow"),
    path(r'post/<int:pk>/delete_like', views.PostDetailView.as_view(), name='delete_like'),
    path(r'profile', views.UserProfileView.as_view(), name="profile"),
]