from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from app.models import Question

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def simulate(request):
    questions = Question.objects.all()  # Fetch all questions from the database
    return render(request, 'account_info.html', {'questions': questions})