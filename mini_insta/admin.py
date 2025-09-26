# File: mini_insta/admin.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/26/2025
# Description: File to handle the mini_insta application admin

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)