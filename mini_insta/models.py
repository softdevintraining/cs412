# File: mini_insta/models.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/17/2025
# Description: File to define data models for the mini_insta application

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User # for auth

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a mini_insta Profile.'''

    # Data attributes for Profile model
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        '''Returns a url that displays the detail page of this Profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk}) 

    def get_all_posts(self):
        '''Return a QuerySet of Posts about this Profile.'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_followers(self):
        '''Returns a QuerySet containing the followers of this Profile.'''
        followers = []

        for follow in Follow.objects.filter(profile=self):
            followers.append(follow.follower_profile)

        return followers

    def get_num_followers(self):
        '''Returns the number of this Profile's followers.'''
        return len(self.get_followers())
    
    def get_following(self):
        '''Returns a list containing the Profiles this Profile follows.'''
        following = []
        for follow in Follow.objects.filter(follower_profile=self):
            following.append(follow.profile)
        
        return following
    
    def get_num_following(self):
        '''Returns the number of Profiles this Profile follows.'''
        return len(Follow.objects.filter(follower_profile=self))
    
    def get_post_feed(self):
        '''Returns the posts that should appear in this Profile's feed.'''
        usernames = []
        for follow in self.get_following():
            usernames.append(follow.username)

        profiles = Profile.objects.filter(username__in=usernames)
        post_feed = Post.objects.filter(profile__in=profiles)

        return post_feed

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.username}\'s Profile!'
    
class Post(models.Model):
    '''Encapsulate the idea of a Post on a Profile.'''

    # data attributes for Post model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        '''Returns a url that displays the detail page of this Post.'''
        return reverse('show_post', kwargs={'pk': self.pk}) 
    
    def get_all_photos(self):
        '''Return a QuerySet of Photos related to this Post.'''
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos
    
    def get_all_comments(self):
        '''Return a QuerySet of Comments related to this Post.'''
        comments = Comment.objects.filter(post=self).order_by('timestamp')
        return comments

    def get_likes(self):
        '''Return a QuerySet of Likes related to this Post.'''
        likes = Like.objects.filter(post=self).order_by('timestamp')
        return likes 
    
    def __str__(self):
        '''Return a string representation of this Post.'''
        return f'{self.caption}'
    
class Photo(models.Model):
    '''Encapsulate the idea of the Photo on a Post.'''

    # data attributes for Photo model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Photo.'''
        if (self.image_file):
            return f'Photo file for: \'{self.post.caption}\''
        elif (self.image_url):
            return f'Photo url for: \'{self.post.caption}\''
        else:
            return f'Photo for: \'{self.post.caption}\''
    
    def get_image_url(self):
        '''Return the url representation of this Photo.'''
        if (self.image_file):
            print(self.image_file.url)
            return (self.image_file.url)
        else:
            return (self.image_url)
        
class Follow(models.Model):
    '''Encapsulate the idea of a Follow on a Profile.'''

    # data attributes for Follow model
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, 
                                related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                         related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'@{self.follower_profile.username} follows @{self.profile.username}.'
    
class Comment(models.Model):
    '''Encapsulate the idea of a Comment on a Post.'''

    # data attributes for Post model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Comment.'''
        return f'{self.profile.username} comments: \'{self.text}\' on {self.post.profile.username}\'s post.'
    

class Like(models.Model):
    '''Encapsulate the idea of a Like on a Post.'''

    # data attributes for Like model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Like.'''
        return f'{self.profile.username} likes {self.post.profile.username}\'s post.'