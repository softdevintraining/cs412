# File: project/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 11/20/2025
# Description: Views file which handles requests to project/

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Song, Like, Follow, Comment

# from .forms import CreateProfileForm, CreatePostForm, CreateFollowForm, UpdateProfileForm, UpdatePostForm
# from django.urls import reverse
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import login
# from django.contrib.auth.mixins import LoginRequiredMixin ## for auth
# from django.contrib.auth.forms import UserCreationForm # for creating a new user

# Create your views here.
class SongsListView(ListView):
    '''Define a view class to display all the songs as a list.'''
    model = Song
    template_name = "project/show_all_songs.html"
    context_object_name = "songs"