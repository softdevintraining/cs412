# blog/urls.py
from django.urls import path, include
from .views import *
from rest_framework import routers, serializers, viewsets
from rest_framework import generics

# API serializers to define the API representation
class JokeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Joke
        fields = ['text', 'name']

class PictureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Picture
        fields = ['image_url']

# APIViews to define the view behavior
class RandomAPIView(generics.ListAPIView):
    jokes = Joke.objects.all()
    joke = jokes.filter(pk=random.randint(0, len(jokes) -1))

    queryset = joke
    serializer_class = JokeSerializer

class AllJokesAPIView(generics.ListCreateAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class JokeAPIView(generics.RetrieveAPIView):
    jokes = Joke.objects.all()
    serializer_class = JokeSerializer
    def get_queryset(self):
        return self.jokes.filter(pk=self.kwargs['pk'])

class PictureAPIView(generics.RetrieveAPIView):
    pictures = Picture.objects.all()
    serializer_class = PictureSerializer
    def get_queryset(self):
        return self.pictures.filter(pk=self.kwargs['pk'])

class AllPicturesAPIView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

urlpatterns = [
    path('', RandomJokeView.as_view(), name="random"),
    path('random', RandomJokeView.as_view(), name="random"),
    path('jokes', ShowAllJokes.as_view(), name="jokes"),
    path('joke/<int:pk>', JokeView.as_view(), name="joke"),
    path('pictures', ShowAllPictures.as_view(), name="pictures"),
    path('picture/<int:pk>', PictureView.as_view(), name="picture"),
    path('api/', RandomAPIView.as_view()),
    path('api/random', RandomAPIView.as_view()),
    path('api/jokes', AllJokesAPIView.as_view()),
    path('api/pictures', AllPicturesAPIView.as_view()),
    path('api/joke/<int:pk>', JokeAPIView.as_view()),
    path('api/picture/<int:pk>', PictureAPIView.as_view())
]