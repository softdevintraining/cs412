# File: project/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 11/20/2025
# Description: File which pattern matches HTML responses to valid requests to 
# project/

# imports
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

# URL patterns for this app:
urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('songs', views.SongsListView.as_view(), name='all_songs'),
    path('song/<int:pk>', views.SongDetailView.as_view(), name='show_song'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='show_profile'),
    path('profile/feed', views.ShowFeedView.as_view(), name='show_feed'),
    path('profile/upload', views.CreateSongView.as_view(), name='create_song'),
    path('sign_up', views.CreateProfileView.as_view(), name='create_profile'),
    path('song/<int:pk>/update', views.UpdateSongView.as_view(), name='update_song'),
    path('song/<int:pk>/comment', views.CreateCommentView.as_view(), name='comment'),
    path('comment/<int:pk>/delete', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('song/<int:pk>/delete', views.DeleteSongView.as_view(), name='delete_song'),
    path('song/<int:pk>/like', views.SongDetailView.as_view(), name='create_like'),
    path('song/<int:pk>/delete_like', views.SongDetailView.as_view(), name='delete_like'),
    path('search', views.SearchView.as_view(), name='search'),
    path('login/', auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name="logout"),
]