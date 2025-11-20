from django.contrib import admin

# Register your models here.
from .models import Profile, Song, Like, Follow, Comment

admin.site.register(Profile)
admin.site.register(Song)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Comment)