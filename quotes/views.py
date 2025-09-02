from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

ali_quotes = [
    "Float like a butterfly, sting like a bee.", 
    "I figured that if I said it enough, I would convince the world that I really was the greatest.",
    "Service to others is the rent you pay for your room here on Earth.",
    "Suffer now and live the rest of your life as a champion.",
    "I’ve wrestled with alligators,  I’ve tussled with a whale. I done handcuffed lightning and thrown thunder in jail.  You know I’m bad. Just last week, I murdered a rock, injured a stone, hospitalized a brick. I’m so mean, I make medicine sick!"
]

image_names = [
    'ali_dinner.jpg',
    'ali_knockdown.jpg',
    'ali_speech.jpg',
    'ali_suit.jpg',
    'ali_weave.jpg',
]

# formatted_ali_quotes = """
#     Float like a butterfly, sting like a bee. \n
#     I figured that if I said it enough, I would convince the world that I really was the greatest. \n
#     Service to others is the rent you pay for your room here on Earth. \n
#     Suffer now and live the rest of your life as a champion. \n
#     I’ve wrestled with alligators,  I’ve tussled with a whale. I done handcuffed lightning and thrown thunder in jail.  You know I’m bad. Just last week, I murdered a rock, injured a stone, hospitalized a brick. I’m so mean, I make medicine sick! \n
#     """

# Create your views here.
def main_page(request):
    '''Respond to the URLs '' and '/quote', delegate work to template'''

    template_name = 'quotes/quote.html'

    quote_num = random.randint(0, len(ali_quotes) - 1)
    image_num = random.randint(0, len(image_names) - 1)

    context = {
        "time": time.ctime(),
        "quote": ali_quotes[quote_num], 
        "image": image_names[image_num],
    }
    return render(request, template_name, context)

def show_all(request):
    '''Respond to the URL 'show_all', delegate work to template'''

    template_name = 'quotes/show_all.html'

    context = {
        "time": time.ctime(),
        "all_quotes": ali_quotes,
        "all_images": image_names,
    }
    return render(request, template_name, context)

def about(request):
    '''Respond to the URL 'about', delegate work to template'''

    template_name = 'quotes/about.html'

    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)

