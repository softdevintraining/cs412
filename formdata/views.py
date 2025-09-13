# formdata/views.py
# view functions to handle URL requests

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def show_form(request):
    '''Show the form to the user.'''

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Process the form submission, and generate a result.'''

    template_name = "formdata/confirmation.html"
    print(request)

    if request.POST:

        # extract form fields into variables:
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color': favorite_color,
        }


    # delegate work to a template
    return render(request, template_name, context)

    