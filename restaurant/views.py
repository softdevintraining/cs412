# File: restaurant/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/13/2025
# Description: The views file which handles responses to requests to restaurant/

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.
def main(request):
    '''Respond to the URLs: '/main\''''
    
    template_name = 'restaurant/main.html'

    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)

def order(request):
    '''Respond to the URL: '/order\''''

    template_name = 'restaurant/order.html'

    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)

def confirmation(request):
    '''Respond to the URL: '/confirmation\''''
    
    template_name = 'restaurant/confirmation.html'
    
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)