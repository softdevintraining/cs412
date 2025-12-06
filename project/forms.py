# File: mini_insta/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/24/2025
# Description: File which houses forms associated with the mini_insta app

from django import forms
from .models import Song, Profile, Comment

class CreateProfileForm(forms.ModelForm):
    '''A form to add a new Profile to the database.'''
    
    class Meta():
        model = Profile
        fields = ['username', 'display_name', 'profile_image_url', 'bio_text']

class CreateSongForm(forms.ModelForm):
    '''A form to add a new Song to the DB.'''

    class Meta():
        model = Song
        fields = ['name', 'description', 'genre', 'audio_url', 'audio_url', 'image_url']
        
class CreateCommentForm(forms.ModelForm):
    '''A form to add a new Comment to the DB.'''

    class Meta():
        model = Comment
        fields = ['text']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile in the database.'''
    
    class Meta():
        '''Associate this form with the Profile model.'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class UpdateSongForm(forms.ModelForm):
    '''A form to add a new Song to the DB.'''

    class Meta():
        model = Song
        fields = ['name', 'description', 'genre', 'audio_file', 'audio_url', 'audio_url', 'image_url']

class DeleteSongForm(forms.ModelForm):
    '''A form to remove a Song from the DB.'''

    class Meta():
        model = Song
        fields = ['name', 'description', 'genre', 'audio_file', 'audio_url', 'audio_url', 'image_url']

class DeleteCommentForm(forms.ModelForm):
    '''A form to add a new Comment to the DB.'''

    class Meta():
        model = Comment
        fields = ['text']