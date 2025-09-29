# File: mini_insta/models.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/26/2025
# Description: File to define data models for the mini_insta application

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a mini_insta Profile.'''

    # data attribute for Profile
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def get_all_posts(self):
        '''Return a QuerySet of Posts about this Profile.'''
        posts = Post.objects.filter(profile=self)
        return posts

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.username}\'s Profile!'
    
class Post(models.Model):
    '''Encapsulate the idea of a Post on a Profile.'''

    # data attributes for Post
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_all_photos(self):
        '''Return a QuerySet of comments about this article.'''
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos

    def __str__(self):
        '''Return a string representation of this Post.'''
        return f'{self.caption}'
    
class Photo(models.Model):
    '''Encapsulate the idea of the Photo on a Post.'''

    # data attributes for Photo
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Photo.'''
        return f'Photo for: \'{self.post.caption}\''