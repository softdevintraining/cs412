from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

import random
# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to display all the profiles as a list.'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"