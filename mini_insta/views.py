# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/3/2025
# Description: Views file which handles requests to mini_insta/

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.http import HttpResponse

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

class CreatePostView(CreateView):
    '''A view to handle the creation of a new Post.'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # create and return a URL
        # return reverse('show_all') # not ideal; we will return to this
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        # call reverse to generate the URL for this Article
        
        return reverse('show_post', kwargs={'pk': Post.objects.last().pk})

    def get_context_data(self):
        '''Return the dictionary of context variabels for use in the template.'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        form.instance.profile = profile

        if (self.request.POST):
            files = self.request.FILES.getlist('files')
            form.instance.save()
            for file in files:
                
                photo = Photo()
                photo.post = form.instance
                photo.image_file = file
                photo.save()
                print("photo would be saved here.")

            # form.instance.save()
            # photo = Photo()
            # photo.post = form.instance
            # photo.image_url = self.request.POST['image_url']
            # photo.save()
        
        return super().form_valid(form)

class UpdateProfileView(UpdateView):
    '''A view to handle the update of a Profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    '''A view to handle the deletion of a Post.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        '''Provides context data needed for this view.'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile
        
        context['profile'] = profile
        return context

    def get_success_url(self):
        return self.get_context_data()['profile'].get_absolute_url()
        
class UpdatePostView(UpdateView):
    '''A view to handle updating a Post.'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    # def get_context_data(self, **kwargs):
    #     '''Provides context data needed for this view.'''
    #     context = super().get_context_data()

    #     pk = self.kwargs['pk']
    #     post = Post.objects.get(pk=pk)
    #     profile = post.profile
        
    #     context['profile'] = profile
    #     return context

    # def get_success_url(self):
    #     return reverse('show_post', kwargs={'pk':self.pk})

class ShowFollowersDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(ListView):
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        '''Provides context data needed for this view.'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        
        context['profile'] = profile
        return context

    def get_success_url(self):
        return self.get_context_data()['profile'].get_absolute_url()