# File: restaurant/views.py
# Author: Oluwatimilehin Akibu (akilu@bu.edu), 9/19/2025
# Description: Views file which handles responses to requests to restaurant/

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

days_of_week = [ # list of weekdays, used to grab current day of order
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"]

months = [ # list of months, used to grab current month of order
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"]

food_prices = { # dict of food prices, used to calculate total price of order
    '8 Pc. Wings': [12.0, 14.0],
    'Chicken Sandwich': 10.0,
    'Waffle Fries': 6.0,
    'Texas Toast': 3.0,
    'Slice of Apple Pie': 7.0,
    'Loaded Fries': 10.0,
    'K-BBQ Tenders': 15.0,
    'Impossible Chicken Wings': 12.0,
}

daily_specials = [ # list of daily specials, one is displayed at random
    'Apple Pie',
    'Loaded Fries',
    'K-BBQ Tenders',
    'Impossible Chicken Wings',
]

special = None 

# Create your views here.
def main(request):
    '''Respond to the URL: '/main\''''
    
    template_name = 'restaurant/main.html'

    context = {
        "time": time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    '''Respond to the URL: '/order\''''

    template_name = 'restaurant/order.html'
    
    # pick a random special from the list
    special = daily_specials[random.randint(0, len(daily_specials) - 1)]

    context = {
        "time": time.ctime(),
        "special": special,
    }
    return render(request, template_name, context)

def confirmation(request):
    '''Process form submission, return HTML result.'''

    template_name = "restaurant/confirmation.html"

    # extract submitted form fields into variables:
    items = request.POST.getlist("items")
    name = request.POST["user_name"]
    phone = request.POST["user_phone"]
    email = request.POST["user_email"]
    special_instructions = request.POST["special_instructions"]

    # calculate total price of the order
    price = 0.0
    for item in items:
        if item == "8 Pc. Wings":
            if request.POST.get("wings_type") == "boneless":
                price += food_prices[item][0]
            else:
                price += food_prices[item][1]
        else:
            price += food_prices[item]

    # estimate order readytime based on current time
    timestamp = time.time() + random.randint(0, 3600)
    struct = time.localtime(timestamp)
    current_day = struct.tm_wday
    current_month = struct.tm_mon
    string = time.strftime(f"{days_of_week[current_day]} {months[current_month]} %d %H:%M:%S %Y", struct)

    # add variables to context
    context = {
        'time': time.ctime(),
        'items': items,
        'name': name,
        'phone': phone,
        'email': email,
        'price': price,
        'order_time': string,
        'special_instructions': special_instructions or "No instructions provided.",
    }

    return render(request, template_name, context)
