# File: restaurant/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/19/2025
# Description: File which pattern matches HTML responses to valid requests to 
# restaurant/

from django.urls import path
from django.conf import settings 
from . import views

urlpatterns = [ # URL patterns for restaurant app
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order"),
    path(r'confirmation', views.confirmation, name="confirmation"),
]