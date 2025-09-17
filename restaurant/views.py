# File: restaurant/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/13/2025
# Description: The views file which handles responses to requests to restaurant/

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

food_prices = {
    '8 Pc. Wings': [12.0, 14.0],
    'Chicken Sandwich': 10.0,
    'Waffle Fries': 6.0,
    'Texas Toast': 3.0,
    'Slice of Apple Pie': 7.0,
    'Loaded Fries': 10.0,
    'K-BBQ Tenders': 15.0,
    'Impossible Chicken Wings': 12.0,
}

daily_specials = [
    'Apple Pie',
    'Loaded Fries',
    'K-BBQ Tenders',
    'Impossible Chicken Wings',
]

special = None

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
    special = daily_specials[random.randint(0, len(daily_specials) - 1)]

    context = {
        "time": time.ctime(),
        "special": special,
    }
    return render(request, template_name, context)

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

        price = 0.0
        for item in items:
            if item == "8 Pc. Wings":
                if request.POST.get("wings_type") == "boneless":
                    price += food_prices[item][0]
                else:
                    price += food_prices[item][1]
            else:
                price += food_prices[item]

        print(items)
        print(name)
        print(phone)
        print(email)
        print(price)
        print(special_instructions)

        # add variables to context
        context = {
            'time': time.ctime(),
            'items': items,
            'name': name,
            'phone': phone,
            'email': email,
            'price': price,
            'special_instructions': special_instructions or "No instructions provided.",
        }

    return render(request, template_name, context)
