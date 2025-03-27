from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from app.models import Question

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def simulate(request):
    # authenticated = request.user.is_authenticated
    authenticated = True  # For testing purposes, assume user is authenticated
    
    # If user is not authenticated and they are not a guest
    if not authenticated:
        if 'guest' in request.GET:
            # Treat the user as a guest
            username = None
        else:
            # If they are not logged in and not a guest, redirect them to login page
            return index(request)
    else:
        # If the user is authenticated, use their username
        username = request.user.username
    
    # Get all questions from the database
    questions = Question.objects.all()
    
    # Pass the user status and questions to the template
    context = {
        'questions': questions,
        'username': username or 'Guest',  # If username is None, display 'Guest'
        'is_authenticated': True,
    }

    return render(request, 'account_info.html', context)