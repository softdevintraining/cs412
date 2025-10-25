# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/24/2025
# Description: File which houses forms associated with the mini_insta app

from django import forms
from .models import Post, Profile, Follow

class CreateProfileForm(forms.ModelForm):
    '''A form to add a new Profile to the database.'''
    
    class Meta():
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''

    class Meta():
        '''Associate this form with the Post model.'''
        model = Post
        fields = ['caption']

class CreateFollowForm(forms.ModelForm):
    '''A form to add a Follow to the database.'''

    class Meta():
        '''Associate this form with the Follow model.'''
        model = Follow
        fields = [] # fields are empty because view is handling everything

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''
    
    class Meta():
        '''Associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdatePostForm(forms.ModelForm):
    '''A form to update a Post in the database.'''

    class Meta():
        '''Associate this form with the Post model.'''
        model = Post
        fields = ['caption']