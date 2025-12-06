# File: project/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 11/20/2025
# Description: Views file which handles requests to project/

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Song, Like, Follow, Comment
from .forms import CreateProfileForm, CreateSongForm, CreateCommentForm, UpdateProfileForm, UpdateSongForm, DeleteSongForm, DeleteCommentForm

# Needed for creating/deleting likes and follows
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin ## for auth
from django.contrib.auth.forms import UserCreationForm # for creating a new user

# from .forms import CreateProfileForm, CreatePostForm, CreateFollowForm, UpdateProfileForm, UpdatePostForm
# from django.urls import reverse
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import login
# from django.contrib.auth.mixins import LoginRequiredMixin ## for auth
# from django.contrib.auth.forms import UserCreationForm # for creating a new user

# Create your views here.
class RequireLogin():
    def get_login_url(self):
        return reverse('login')
    
    def get_object(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile

class LandingPageView(TemplateView):
    template_name = "project/landing_page.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profiles'] = Profile.objects.all()
        
        if (self.request.user.is_authenticated):
            context['user_profile'] = Profile.objects.get(user=self.request.user)

        return context

class SongsListView(ListView):
    '''Define a view class to display all the songs as a list.'''
    model = Song
    template_name = "project/show_all_songs.html"
    context_object_name = "songs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.is_authenticated)
        if (self.request.user.is_authenticated):
            context['user_profile'] = Profile.objects.get(user=self.request.user)

        return context

class SongDetailView(DetailView):
    '''Define a view class to display the information of one song.'''
    model = Song
    template_name = "project/show_song.html"
    context_object_name = "song"

    def get_context_data(self, **kwargs):
        '''Grabbing context for this detail view'''
        context = super().get_context_data()
        song = Song.objects.get(pk=self.kwargs['pk'])
        profile = song.profile
        form = CreateCommentForm()

        # check if current user likes the post being viewed
        if (self.request.user.is_authenticated): 
            # this if statement avoids errors for anonymous users
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
            if user_profile:
                context['show_buttons'] = True
                context['liked_by'] = song.liked_by(user_profile)
            else:
                context['show_buttons'] = False

        context['profile'] = profile
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        song = Song.objects.get(pk=pk)
        self.object = song

        if (self.request.user.is_authenticated):
            profile = Profile.objects.get(user=self.request.user)
            if (self.get_context_data()['liked_by'] == True):
                self.remove_like(song, profile)
            else:
                self.add_like(song, profile)
        else:
            print("No authenticated user")
    
        # redirect to current post's page (consequence of post method)
        return HttpResponseRedirect(reverse('show_song', kwargs={'pk':pk}))

    def add_like(self, song, profile):
        if profile:
            like = Like()
            like.song = song
            like.profile = profile 
            like.save()
            print('added like')
        else:
            print("could not add like, no profile")

    # Remove a like from the database
    def remove_like(self, song, profile):
        if profile:
            like = Like.objects.get(song=song, profile=profile)
            like.delete()
        else:
            print("could not remove like")

class ProfileDetailView(DetailView):
    '''Define a view class to the display a single profile.'''
    model = Profile
    template_name = "project/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        '''Grabbing context for this detail view.'''
        context = super().get_context_data()
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # self.object = profile

        if (self.request.user.is_authenticated):
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
            context['followed_by'] = profile.is_follower(user_profile)
            print(context['followed_by'])

        context['profile'] = profile
        return context
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        self.object = profile

        if (self.request.user.is_authenticated):
            user_profile = Profile.objects.get(user=self.request.user)
            if (self.get_context_data()['followed_by'] == True):
                self.remove_follow(profile, user_profile)
            else:
                self.add_follow(profile, user_profile)
        else:
            print("No authenticated user")
    
        # redirect to current post's page (consequence of post method)
        return HttpResponseRedirect(reverse('show_song', kwargs={'pk':pk}))

    def add_follow(self, followed, follower):
        follow = Follow()
        follow.followed = followed
        follow.followed_by = follower
        follow.save()
        
    
    def remove_follow(self, followed, followed_by): 
        follow = Follow.objects.get(followed=followed, followed_by=followed_by)
        follow.delete()

class ShowFeedView(RequireLogin, LoginRequiredMixin, ListView):
    '''Define a view class to show the feed of a Profile.'''
    model = Song
    template_name = "project/show_feed.html"
    context_object_name = "songs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user):
            profile = self.get_object()
            context["user_profile"] = profile

        return context
    
class SearchView(ListView):
    '''Define a view class to handle searching from a Profile.'''
    template_name = "project/search_results.html"

    def dispatch(self, request, *args, **kwargs):
        '''Overwrite dispatch method to handle template forwarding.'''
        # if ('query' not in self.request.GET):
            # self.template_name = "project/search.html"
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Overwrite queryset method to grab relevant Songs.'''
        query = None
        if ('query' in self.request.GET):
            query = self.request.GET.get('query')
            return Song.objects.filter(name__contains=query)
        else:
            return []
    
    def get_context_data(self):
        '''Overwrite get_context_data to define necessary context variables.'''
        context = super().get_context_data()
        if (self.request.user.is_authenticated):
            profile = self.get_object()
            context['user_profile'] = profile
        matching_songs = None
        matching_profiles = None

        if ('query' in self.request.GET):
            query = self.request.GET.get('query')
            context['query'] = query
            matching_songs = self.get_queryset()
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

        context['songs'] = matching_songs
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
        
class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "project/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = UserCreationForm()
        context['new_user_form'] = user_form

        if (self.request.user.is_authenticated):
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
            
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        user = user_form.save()
        print(user)

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        form.instance.user = user

        return super().form_valid(form)

class CreateSongView(RequireLogin, LoginRequiredMixin, CreateView):
    # model = Song
    form_class = CreateSongForm
    template_name = "project/create_song_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
        return reverse('show_song', kwargs={'pk': Song.objects.last().pk})

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        profile = self.get_object()

        context['user_profile'] = profile
        return context

    def form_valid(self, form):
        '''Overwrite form_valid method.'''
        user = self.request.user
        profile = self.get_object()

        form.instance.profile = profile
        form.instance.user = user

        if (self.request.POST):
            # create Photo objects and relate to them to created post
            file = self.request.FILES.get('file')
            if (file):
                form.instance.audio_file = file

            form.instance.save()
        
        return super().form_valid(form)
    
class CreateCommentView(RequireLogin, CreateView):
    model = Comment
    form_class = CreateCommentForm
    
    def get_success_url(self):
        return reverse('show_song', kwargs={'pk': Comment.objects.last().song.pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        song = Song.objects.get(pk=self.kwargs['pk'])
        profile = self.get_object()

        context['profile'] = profile
        context['song'] = song
        return context
    
    def form_valid(self, form):
        '''Overwrite form_valid method.'''
        user = self.request.user
        profile = self.get_object()

        form.instance.user = user
        form.instance.profile = profile
        form.instance.song = self.get_context_data()['song']
        
        return super().form_valid(form)

class DeleteCommentView(RequireLogin, TemplateView):
    model = Comment
    form_class = DeleteCommentForm
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data()
        # comment = Comment.objects.get(pk=self.kwargs['pk'])
        # self.object = comment
        song_name = self.request.POST['song_name']
        username = self.request.POST['song_profile_user']
        song_profile = Profile.objects.get(username=username)
        text = self.request.POST.get('form_text')
        profile = self.get_object()
        song = Song.objects.get(name=song_name, profile=song_profile)
        # comment = Comment.objects.get(text=text, profile=profile)
        
        # profile = self.get_object().profile
        
        context['song'] = song
        context['text'] = text
        context['song_profile'] = profile

        if (self.request.user.is_authenticated):
            user_profile = self.get_object()
            context['user_profile'] = user_profile
        # context['comment'] = comment
        return context
    
    def post(self, request, *args, **kwargs):
        # pk = self.kwargs['pk']
        # song = Song.objects.get(pk=pk)
        # self.object = song
        song = self.get_context_data()['song']
        text = self.get_context_data()['text']
        profile = self.get_context_data()['song_profile']


        if (self.request.user.is_authenticated):
            self.remove_comment(text, profile, song)
        else:
            print("No authenticated user")
        return HttpResponseRedirect(reverse('show_song', kwargs={'pk':self.get_context_data()['song'].pk}))
    
    def remove_comment(self, text, profile, song):

        comment = Comment.objects.get(text=text, profile=profile, song=song)
        comment.delete()
    
        # redirect to current post's page (consequence of post method)    
    
class UpdateProfileView(RequireLogin, LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "project/update_profile_form.html"

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user):
            profile = self.get_object()
            context["profile"] = profile

        return context

class UpdateSongView(RequireLogin, LoginRequiredMixin, UpdateView):
    model = Song
    form_class = UpdateSongForm
    template_name = "project/update_song_form.html"

    def get_object(self):
        return Song.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.user.is_authenticated):
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
        return context
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)

class DeleteSongView(LoginRequiredMixin, DeleteView):
    '''A view to handle the deletion of a Song.'''

    model = Song
    form_class = DeleteSongForm
    template_name = 'project/delete_song_form.html'

    def get_context_data(self, **kwargs):
        '''Provides context data needed for this view.'''
        context = super().get_context_data()

        pk = self.kwargs['pk']
        song = Song.objects.get(pk=pk)
        context['profile'] = song.profile
        if (self.request.user.is_authenticated):
            user_profile = Profile.objects.get(user=self.request.user)
            context['user_profile'] = user_profile
        return context

    def get_success_url(self):
        return self.get_context_data()['profile'].get_absolute_url()
    
    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)
