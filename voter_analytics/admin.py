# File: voter_analytics/admin.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 10/31/2025
# Description: File to handle the voter_analytics application admin
from django.contrib import admin

# Register your models here.
from .models import Voter

admin.site.register(Voter)