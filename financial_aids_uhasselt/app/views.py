from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from app.models import FinancialSupport, Question
from .calculations import calculate_reference_income

from django.contrib.auth.hashers import check_password
from app.models import UserProfile

def index(request):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(email=email)
            # if check_password(password, user.password):
            if check_password(password, user.password):
                # ✅ Login succesvol
                request.session['user_id'] = user.user_id
                request.session['email'] = user.email
                return redirect('simulate')
            else:
                context['error'] = 'Incorrect password.'
        except UserProfile.DoesNotExist:
            context['error'] = 'User not found.'

    return render(request, 'index.html', context)

def simulate(request):
    user_email = request.session.get('email')

    if not user_email and 'guest' not in request.GET:
        return redirect('index')

    header = f"Welcome {user_email}" if user_email else "Financial Simulation"
    username = user_email if user_email else "Guest"
    
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
    basic_questions = Question.objects.filter(question_text__in=basic_question_texts)
    income_questions = Question.objects.exclude(question_text__in=basic_question_texts + yes_no_questions_texts)

    # 👉 Load user data
    user_data = {}
    if user_email:
        try:
            user = UserProfile.objects.get(email=user_email)
            user_data = {
                'email': user.email,
                'faculty': user.faculty,
                'ects_amount': user.ects_amount,
                'domicile': user.domicile,
                'annual_family_income': user.annual_family_income,
                'cadastral_income_rental': user.cadastral_income_rental,
                'cadastral_income_business': user.cadastral_income_business,
                'separable_taxable_incomes': user.separable_taxable_incomes,
                'alimentation_money': user.alimentation_money,
                'living_wages': user.living_wages,
                'income_replacement_allowance': user.income_replacement_allowance,
                'foreign_incomes': user.foreign_incomes,
                'study_income': user.study_income,
                'living_unit_points': user.living_unit_points,
            }
        except UserProfile.DoesNotExist:
            pass  # fallback op lege form

    context = {
        'basic_questions': basic_questions,
        'income_questions': income_questions,
        'yes_no_questions': yes_no_questions,
        'username': username,
        'header': header,
        'user_data': user_data,
    }

    return render(request, 'account_info.html', context)

def financial_overview(request):
    return render(request, 'financial_overview.html')

def financial_support(request):
    supports = FinancialSupport.objects.all()
    return render(request, 'financial_support.html', {'supports': supports})

@csrf_exempt  # Disable CSRF for this endpoint (ensure security in production)
def calculate_income_view(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            
            # Perform the calculation
            result = calculate_reference_income(data)
            
            # Return the result as JSON
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)


