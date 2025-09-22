# mini_insta/models.py
# define data models for the mini_insta application

from django.db import models

# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a mini_insta Profile.'''
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''return a string representation of this model instance.'''
        return f'{self.username}\'s Profile!'