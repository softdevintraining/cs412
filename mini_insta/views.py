# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/17/2025
# Description: Views file which handles requests to mini_insta/

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin ## for auth

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

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to handle the creation of a new Post.'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''

        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']

        # call reverse to generate the URL for this Article
        return reverse('show_post', kwargs={'pk': Post.objects.last().pk})

    def get_context_data(self):
        '''Return the dictionary of context variabels for use in the template.'''
        context = super().get_context_data()

        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)
        profile = self.get_object()

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Overwrite form_valid method.'''
        # pk = self.kwargs['pk']
        user = self.request.user
        # profile = Profile.objects.get(pk=pk)
        profile = self.get_object()

        form.instance.profile = profile
        form.instance.user = user

        if (self.request.POST):
            # create Photo objects and relate to them to created post
            files = self.request.FILES.getlist('files')
            form.instance.save()

            for file in files:
                photo = Photo()
                photo.post = form.instance
                photo.image_file = file
                photo.save()
        
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        # queryset = Profile.objects.get(user=user, )
        return profile
    
    def get_login_url(self):
        return reverse('login')

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to handle the update of a Profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        # queryset = Profile.objects.get(user=user, )
        return profile
    
    def get_login_url(self):
        return reverse('login')

class DeletePostView(LoginRequiredMixin, DeleteView):
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
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
            
class UpdatePostView(LoginRequiredMixin, UpdateView):
    '''A view to handle updating a Post.'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

class ShowFollowersDetailView(DetailView):
    '''Define a view class to show followers of a Profile.'''
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingDetailView(DetailView):
    '''Define a view class to show following of a Profile.'''
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(LoginRequiredMixin, ListView):
    '''Define a view class to show the post feed of a Profile.'''
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        '''Provides context data needed for this view.'''
        context = super().get_context_data()

        # pk = self.kwargs['pk']
        # profile = Profile.objects.get(pk=pk)
        profile = self.get_object()
        
        context['profile'] = profile
        return context

    def get_success_url(self):
        '''Generates a URL to redirect to.'''
        return self.get_context_data()['profile'].get_absolute_url()
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        # queryset = Profile.objects.get(user=user, )
        return profile
    
    def get_login_url(self):
        return reverse('login')

class SearchView(LoginRequiredMixin, ListView):
    '''Define a view class to handle searching from a Profile.'''
    template_name = "mini_insta/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        '''Overwrite dispatch method to handle template forwarding.'''
        if ('query' not in self.request.GET):
            self.template_name = "mini_insta/search.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Overwrite queryset method to grab relevant Posts.'''
        query = None
        if ('query' in self.request.GET):
            query = self.request.GET.get('query')
            return Post.objects.filter(caption__contains=query)
        else:
            return []
    
    def get_context_data(self):
        '''Overwrite get_context_data to define necessary context variables.'''
        context = super().get_context_data()
        # pk = self.kwargs['pk']
        profile = self.get_object()
        matching_posts = None
        matching_profiles = None

        if ('query' in self.request.GET):
            query = self.request.GET.get('query')
            context['query'] = query
            matching_posts = self.get_queryset()
            matching_profiles = list(Profile.objects.filter(username__contains=query))
            if matching_profiles != None:
                for item in Profile.objects.filter(display_name__contains=query):
                    if item in matching_profiles:
                        continue
                    else:
                        matching_profiles.append(item)
                for item in Profile.objects.filter(bio_text__contains=query):
                    if item in matching_profiles:
                        continue
                    else:
                        matching_profiles.append(item)

        context['profile'] = profile
        context['posts'] = matching_posts
        context['profiles'] = matching_profiles
        return context

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
    
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        # queryset = Profile.objects.get(user=user, )
        return profile
    
    def get_login_url(self):
        return reverse('login')
    
    
class LoggedOutView(TemplateView):
    '''A view to show the logout confirmation page.'''
    template_name="mini_insta/logged_out.html"