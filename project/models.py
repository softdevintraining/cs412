# File: project/models.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 11/20/2025
# Description: File to define data models for my final project application

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User # for auth

# Create your models here.
class Profile(models.Model):
    '''Encapsulate idea of a Profile. Provides some necessary attributes.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='final_project_user')
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.display_name}'s Profile'''
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={"pk": self.pk})

    def get_songs(self):
        return Song.objects.filter(profile=self)
    def get_followers(self):
        followers = []

        for follow in Follow.objects.filter(followed=self):
            followers.append(follow.followed_by)

        return followers
    def get_following(self):
        return Follow.objects.filter(followed_by=self)
    
    def get_num_songs(self):
        return len(self.get_num_songs)
    def get_num_followers(self):
        return len(self.get_followers())
    def get_num_following(self):
        return len(self.get_following())
    
    def get_song_feed(self):
        '''Returns the posts that should appear in this Profile's feed.'''
        profiles = []
        for follow in self.get_following():
            profiles.append(follow.followed)

        # profiles = Profile.objects.filter(username__in=usernames)
        song_feed = Song.objects.filter(profile__in=profiles)
        print(f'get_following: {self.get_following()}')
        print(f'users: {profiles}')
        print(f'profiles: {profiles}')
        return song_feed
    
    def get_profile_feed(self):
        '''Returns the profiles that should appear in this Profile's feed.'''
        pass

    def is_follower(self, profile):
        if profile in self.get_followers():
            return True
    
class Song(models.Model):
    '''Encapsulate idea of a Song.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    length = models.DurationField(blank=True, null=True)
    audio_file = models.FileField(blank=True, null=True)
    audio_url = models.URLField(blank=True, max_length=1000)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.name} by {self.profile.display_name}'''
    
    def get_absolute_url(self):
        return reverse('show_song', kwargs={"pk": self.pk})
    
    def get_comments(self):
        return Comment.objects.filter(song=self)
    
    def get_likes(self):
        '''Return a QuerySet of Likes related to this Post.'''
        likes = Like.objects.filter(song=self).order_by('timestamp')
        return likes
    
    def liked_by(self, profile):
        '''Returns whether a profile likes a post.'''
        likes = self.get_likes()
        profiles = []
        for like in likes:
            profiles.append(like.profile)

        return (profile in profiles)
    
class Like(models.Model):
    '''Encapsulate idea of a Like on a Song.'''
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.profile.display_name} likes {self.song.name}'''

class Follow(models.Model):
    '''Encapsulate idea of a Follow on a Profile.'''
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='final_project_followed')
    followed_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.followed_by.display_name} follows {self.followed.display_name}'''

class Comment(models.Model):
    '''Encapsulate idea of a Comment on a Song.'''
    text = models.TextField()
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.profile.display_name} comments on {self.song.name}'''