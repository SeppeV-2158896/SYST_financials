from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from app.models import Question

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def simulate(request):
    authenticated = request.POST.get('is_authenticated')
    
    # Check if the user is authenticated or accessing as a guest
    if not authenticated and 'guest' not in request.GET:
        return redirect('index')  # Redirect to the login page if unauthorized

    # Determine user type and set header
    if authenticated and 'guest' not in request.GET:
        username = request.POST.get('username')
        header = f"Welcome {username}"  # Header for authenticated users
    else:
        username = "Guest"
        header = "Financial Simulation"  # Header for guest users

    # Get all questions from the database
    questions = Question.objects.all()
    
    print(username)

    # Pass the user status and questions to the template
    context = {
        'questions': questions,
        'username': username,
        'header': header,
    }

    return render(request, 'account_info.html', context)