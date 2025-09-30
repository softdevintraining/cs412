from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a Post to the database.'''

    class Meta():
        '''Associate this form with the Post model.'''
        model = Post
        fields = ['caption']