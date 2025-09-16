# File: restaurant/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/13/2025
# Description: The views file which handles responses to requests to restaurant/

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

food_prices = {
    'Wings': [8.0, 14.0],
    'Chicken Sandwich': [10.0],
    'Waffle Fries': [6.0],
    'Texas Toast': [3.0],
    'Special': [10.0],
}

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

# def confirmation(request):
#     '''Respond to the URL: '/confirmation\''''
    
#     template_name = 'restaurant/confirmation.html'
    
#     context = {
#         "time": time.ctime(),
#     }
#     return render(request, template_name, context)

def confirmation(request):
    '''Process form submission, return HTML result.'''
    
    template_name = "restaurant/order.html"
    print(request)

    if request.POST:
        template_name = "restaurant/confirmation.html"

        # extract submitted form fields into variables:
        items = request.POST.getlist("items")
        name = request.POST["user_name"]
        phone = request.POST["user_phone"]
        email = request.POST["user_email"]
        special_instructions = request.POST["special_instructions"]
        
        print(items)
        print(name)
        print(phone)
        print(email)
        print(special_instructions)

        # add variables to context
        context = {
            'time': time.ctime(),
            'items': items,
            'name': name,
            'phone': phone,
            'email': email,
            'special_instructions': special_instructions or "No instructions provided.",
        }

    return render(request, template_name, context)
