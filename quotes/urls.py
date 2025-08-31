# file: quotes/urls.py

from django.urls import path
from django.conf import settings 
from . import views

# URL patterns for hw app
urlpatterns = [
    # path(r'', views.home, name="home")
    path(r'', views.main_page, name="main_page"),
    # path(r'about', views.about, name="about_page"),
]
