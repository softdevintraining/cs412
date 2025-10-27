# File: voter_analytics/urls.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/31/2025
# Description: File which pattern matches HTML responses to valid requests to 
# voter_analytics/

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ShowVotersView.as_view(), name="show_all_voters"),
    path(r'voters', views.ShowVotersView.as_view(), name="voter_list"),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name="voter"),
    path(r'graphs', views.ShowGraphsView.as_view(), name="graphs"),
]