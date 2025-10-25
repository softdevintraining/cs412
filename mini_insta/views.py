# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/17/2025
# Description: Views file which handles requests to mini_insta/

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreateProfileForm, CreatePostForm, CreateFollowForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin ## for auth
from django.contrib.auth.forms import UserCreationForm # for creating a new user

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

    def get_context_data(self, **kwargs): 
        '''Grabbing context for this detail view'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # check if current user follows the profile being viewed
        if (self.request.user.is_authenticated): 
            # this if statement avoids errors for anonymous users
            user_profile = Profile.objects.get(user=self.request.user)
            context['followed_by'] = user_profile in profile.get_followers()
        
        return context
    
    # Remove a follow object from the database
    def remove_follow(self, followed, follower):
        follow = Follow.objects.get(profile=followed, follower_profile=follower)
        follow.delete()

    # Override post method to handle follow and unfollow functionality
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        user_profile = Profile.objects.get(user=self.request.user)
        self.object = profile

        if (self.get_context_data()['followed_by']):
            self.remove_follow(profile, user_profile)

        # redirect to current profile's page (consequence of post method)
        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk':pk}))

class UserProfileView(DetailView):
    '''Define a view class to display the Profile of current user.'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    # if a suer is logged in, set profile context object to the user's profile
    def get_object(self, queryset = ...):
        if self.request.user:
            return Profile.objects.get(user=self.request.user)
        return None

class PostDetailView(DetailView):
    '''Define a view class to display the details of a single Post.'''
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


    def get_context_data(self, **kwargs):
        '''Grabbing context for this detail view'''
        context = super().get_context_data()
        post = Post.objects.get(pk=self.kwargs['pk'])
        
        # check if current user likes the post being viewed
        if (self.request.user.is_authenticated): 
            # this if statement avoids errors for anonymous users
            user = Profile.objects.get(user=self.request.user)
            context['liked_by'] = post.liked_by(user)

        return context

    # Override post method to handle like and unlike functionality
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = Profile.objects.get(user=self.request.user)
        self.object = post
        
        if (self.get_context_data()['liked_by'] == True):
            self.remove_like(post, profile)
        else:
            self.add_like(post, profile)
    
        # redirect to current post's page (consequence of post method)
        return HttpResponseRedirect(reverse('show_post', kwargs={'pk':pk}))
    
    # Add a Like to the database
    def add_like(self, post, profile):
        like = Like()
        like.post = post
        like.profile = profile 
        like.save()

    # Remove a like from the database
    def remove_like(self, post, profile):
        print("removing like")
        like = Like.objects.get(post=post, profile=profile)
        like.delete()


class CreateProfileView(CreateView):
    '''A view to handle the creation of a new Profile.'''

    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        '''Grabbing context for the view'''
        context = super().get_context_data(**kwargs)

        user_creation_form = UserCreationForm()
        context['new_user_form'] = user_creation_form
    
        return context

    # Validate create profile form, create user, login, and then create profile
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        print(user)

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        form.instance.user = user

        return super().form_valid(form)

class CreatePostView(LoginRequiredMixin, CreateView):
    '''A view to handle the creation of a new Post.'''

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
        return reverse('show_post', kwargs={'pk': Post.objects.last().pk})

    def get_context_data(self):
        '''Return the dictionary of context variabels for use in the template.'''
        context = super().get_context_data()
        profile = self.get_object()

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Overwrite form_valid method.'''
        user = self.request.user
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
        return profile
    
    def get_login_url(self):
        return reverse('login')

class CreateFollowView(CreateView):
    model = Follow
    form_class = CreateFollowForm
    template_name = "mini_insta/create_follow_form.html"

    def get_context_data(self, **kwargs):
        '''Provides context data needed for this view.'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        follower_profile = Profile.objects.get(user=self.request.user)
        
        context['profile'] = profile
        context['follower'] = follower_profile
        return context
    
    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Follow.'''
        return self.get_context_data()['profile'].get_absolute_url()
    
    def form_valid(self, form):
        if (self.request.POST):
            profile = self.get_context_data()['profile']
            follower = self.get_context_data()['follower']
            new_follow = Follow()
            new_follow.follower_profile = follower
            new_follow.profile = profile
            new_follow.save()

        return HttpResponseRedirect(reverse('show_profile', kwargs={'pk': profile.pk}))

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
        return profile
    
    def get_login_url(self):
        return reverse('login')
    
    
class LoggedOutView(TemplateView):
    '''A view to show the logout confirmation page.'''
    template_name="mini_insta/logged_out.html"