# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/3/2025
# Description: File which houses forms associated with the mini_insta app

from django import forms
from .models import Post, Profile

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''

    class Meta():
        '''Associate this form with the Post model.'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''
    class Meta():
        '''Associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']