# File: project/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 11/20/2025
# Description: File which pattern matches HTML responses to valid requests to 
# project/

from django.urls import path
from . import views

# URL patterns for this app:
urlpatterns = [
    path('songs', views.SongsListView.as_view(), name='songs'),
]