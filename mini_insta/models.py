# File: mini_insta/models.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/3/2025
# Description: File to define data models for the mini_insta application

from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a mini_insta Profile.'''

    # data attributes for Profile model
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk}) 

    def get_all_posts(self):
        '''Return a QuerySet of Posts about this Profile.'''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_followers(self):
        followers = []

        for follow in Follow.objects.filter(profile=self):
            followers.append(follow.follower_profile)

        return followers

    def get_num_followers(self):
        return len(self.get_followers())
    
    def get_following(self):
        return list(Follow.objects.filter(follower_profile=self))
    
    def get_num_following(self):
        return len(Follow.objects.filter(follower_profile=self))
    
    def get_post_feed(self):
        usernames = []
        for follow in self.get_following():
            usernames.append(follow.profile.username)

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
        return reverse('show_post', kwargs={'pk': self.pk}) 
    
    def get_all_photos(self):
        '''Return a QuerySet of comments about this article.'''
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos
    
    def get_all_comments(self):
        comments = Comment.objects.filter(post=self).order_by('timestamp')
        return comments

    def get_likes(self):
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
        if (self.image_file):
            print(self.image_file.url)
            return (self.image_file.url)
        else:
            return (self.image_url)
        
class Follow(models.Model):
    '''Encapsulate the idea of a Follow on a Profile.'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'@{self.follower_profile.username} follows @{self.profile.username}.'
    
class Comment(models.Model):
    '''Encapsulate the idea of a Comment on a Post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f'{self.profile.username} comments: \'{self.text}\' on {self.post.profile}\'s post.'
    

class Like(models.Model):
    '''Encapsulate the idea of a Like on a Post.'''
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile.username} Likes {self.post.profile}\'s post.'