# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/26/2025
# Description: Views file which handles responses to requests to mini_insta/

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile, Post

# Create your views here.
class ProfileListView(ListView):
    '''Define a view class to display all the profiles as a list.'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''Define a view class to display details of a single profile.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''Define a view class to display the details of a single Post.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"