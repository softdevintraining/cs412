# File: quotes/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/9/2025
# Description: File which pattern matches HTML responses to valid requests to 
# quotes/

from django.urls import path
from django.conf import settings 
from . import views

urlpatterns = [ # URL patterns for quotes app
    path(r'', views.main_page, name="main_page"),
    path(r'quote', views.main_page, name="main_page"),
    path(r'show_all', views.show_all, name="show_all"),
    path(r'about', views.about, name="about"),
]
