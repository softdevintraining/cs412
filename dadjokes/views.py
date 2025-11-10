from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from .models import *
from rest_framework import serializers, viewsets
from rest_framework.response import Response


import random

# Create your views here.
class RandomJokeView(TemplateView):
    '''Define a view class to show a random joke and picture.'''

    template_name = "dadjokes/random.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jokes = Joke.objects.all()
        joke = jokes[random.randint(0, len(jokes) -1)]

        pictures = Picture.objects.all()
        picture = pictures[random.randint(0, len(jokes) -1)]

        context['joke'] = joke
        context['picture'] = picture
        
        return context

class ShowAllJokes(ListView):
    '''Define a view class to show all jokes.'''

    model = Joke
    template_name = "dadjokes/show_all_jokes.html"
    context_object_name = "jokes"

class ShowAllPictures(ListView):
    '''Define a view class to show all jokes.'''

    model = Picture
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = "pictures"

class JokeView(DetailView):
    '''Display a single joke.'''

    model = Joke
    template_name = "dadjokes/show_joke.html"
    context_object_name ="joke" # note the singular variable name

class PictureView(DetailView):
    '''Display a single picture.'''

    model = Picture
    template_name = "dadjokes/show_picture.html"
    context_object_name = "picture" # note the singular variable name
