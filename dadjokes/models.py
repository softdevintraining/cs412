from django.db import models

# Create your models here.
class Joke(models.Model):
    '''Encapsulate the idea of a Joke.'''

    text = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text} by {self.name} '

class Picture(models.Model):
    '''Store urls of an image.'''

    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now=True)