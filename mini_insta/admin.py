# File: mini_insta/admin.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/3/2025
# Description: File to handle the mini_insta application admin

from django.contrib import admin

# Register your models here.
from .models import Profile, Post, Photo, Follow, Comment, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)