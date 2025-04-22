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

    user = None
    if user_email:
        try:
            user = UserProfile.objects.get(email=user_email)
        except UserProfile.DoesNotExist:
            user = None

    context = {
        'username': username,
        'header': header,
        'basic_questions': Question.objects.filter(text__in=[
            "Email address", "Faculty of student", "Amount of ECTS this year", "Domicile"
        ]),
        'yes_no_questions': Question.objects.filter(text__in=[
            "Are you staying in a student room?", "Have you bought your laptop through the university?"
        ]),
        'income_questions': Question.objects.exclude(text__in=[
            "Email address", "Faculty of student", "Amount of ECTS this year",
            "Domicile", "Are you staying in a student room?", "Have you bought your laptop through the university?"
        ]),
        # Prefill user data
        'email': user.email if user else '',
        'faculty': user.faculty if user else '',
        'ects_amount': user.ects_amount if user else '',
        'domicile': user.domicile if user else '',
        'living_unit_points': user.living_unit_points if user else '',
        'annual_family_income': user.annual_family_income if user else '',
        'cadastral_income_rental': user.cadastral_income_rental if user else '',
        'cadastral_income_business': user.cadastral_income_business if user else '',
        'separable_taxable_incomes': user.separable_taxable_incomes if user else '',
        'alimentation_money': user.alimentation_money if user else '',
        'living_wages': user.living_wages if user else '',
        'income_replacement_allowance': user.income_replacement_allowance if user else '',
        'foreign_incomes': user.foreign_incomes if user else '',
        'study_income': user.study_income if user else '',
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


