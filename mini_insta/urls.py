# mini_insta/urls.py
# url patterns for the 'mini_insta' app.

from django.urls import path
from django.conf import settings
from . import views

# URL patterns for this app:
urlpatterns = [
    path(r'', views.ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ProfileDetailView.as_view(), name="show_profile"),
]