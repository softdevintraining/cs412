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

class Song(models.Model):
    '''Encapsulate idea of a Song.'''
    uploader = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    description = models.TextField(blank=True)
    genre = models.TextField(blank=True)
    length = models.DurationField(blank=True, null=True)
    audio_file = models.FileField(blank=True)
    audio_url = models.URLField(blank=True, max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.name} by {self.uploader.display_name}'''
    
class Like(models.Model):
    '''Encapsulate idea of a Like on a Song.'''
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    liked_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.liked_by.display_name} likes {self.song.name}'''

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
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'''{self.commenter.display_name} comments on {self.song.name}'''