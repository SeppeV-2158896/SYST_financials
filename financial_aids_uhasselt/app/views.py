from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from app.models import FinancialSupport, Question

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

    # Definieer de basic en income-related questions
    basic_question_texts = [
        "Email address",
        "Faculty of student",
        "Amount of ECTS this year",
        "Domicile"
    ]
    yes_no_questions_texts = [
    "Are you staying in a student room?",
    "Have you bought your laptop through the university?"
    ]

    yes_no_questions = Question.objects.filter(question_text__in=yes_no_questions_texts)
#voor debuggen
    print("Yes/No Questions gevonden:", yes_no_questions)

    
    # Filter de vragen op basis van deze teksten
    basic_questions = Question.objects.filter(question_text__in=basic_question_texts)
    income_questions = Question.objects.exclude(question_text__in=basic_question_texts + yes_no_questions_texts)
    yes_no_questions = Question.objects.filter(question_text__in=yes_no_questions_texts)
    # Pass de user status en gescheiden vragen naar de template
    context = {
        'basic_questions': basic_questions,
        'income_questions': income_questions,
        'yes_no_questions': yes_no_questions,
        'username': username,
        'header': header,
    }

    return render(request, 'account_info.html', context)

def financial_overview(request):
    return render(request, 'financial_overview.html')

def financial_support(request):
    supports = FinancialSupport.objects.all()
    return render(request, 'financial_support.html', {'supports': supports})


