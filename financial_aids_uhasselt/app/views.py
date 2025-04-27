from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from app.models import FinancialSupport, Question, SupportSystem
from .calculations import calculate_reference_income, determine_category
from django.contrib.auth.hashers import check_password
from app.models import UserProfile
from urllib.parse import urlencode
from decimal import Decimal

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
    # Check if the user is continuing as a guest
    if 'guest' in request.GET:
        # Clear the email session variable for guest users
        if 'email' in request.session:
            del request.session['email']

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
        'user_email': user_email,  # Pass user_email to the template
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
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('index')

    user = UserProfile.objects.get(pk=user_id)
    historical_data = user.historical_data.all().order_by('school_year')

    # Calculate totals for each year
    graph_data = {}
    for data in historical_data:
        year = data.school_year
        if year not in graph_data:
            graph_data[year] = {"income": Decimal(0), "expenses": Decimal(0)}
        graph_data[year]["income"] += Decimal(data.income)
        graph_data[year]["expenses"] += Decimal(
            data.study_expenses_tuition +
            data.study_expenses_books +
            data.study_expenses_housing
        )

    # Prepare data for the graph
    graph_labels = list(graph_data.keys())
    graph_income = [float(graph_data[year]["income"]) for year in graph_labels]
    graph_expenses = [float(graph_data[year]["expenses"]) for year in graph_labels]

    return render(request, 'financial_overview.html', {
        'historical_data': historical_data,
        'graph_labels': graph_labels,
        'graph_income': graph_income,
        'graph_expenses': graph_expenses,
    })

def financial_support(request):
    supports = json.loads(request.GET.get('supports', '[]'))
    error = request.GET.get('error', None)
    return render(request, 'financial_support.html', {'supports': supports, 'error': error})

@csrf_exempt
def calculate_income_view(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            
            # Perform the calculation
            result = calculate_reference_income(data)
            
            if "reference_income" in result:
                # Determine the category
                living_unit_points = float(data.get("living_unit_points", 0) or 0.0)
                reference_income = result["reference_income"]
                category = determine_category(living_unit_points, reference_income)
                result["category"] = category

                # Fetch all support systems
                all_supports = SupportSystem.objects.all()
                supports = [
                    {
                        "name": support.name,
                        "description": support.description,
                        "eligible": support.min_category <= category <= support.max_category,
                        "link": support.link,
                    }
                    for support in all_supports
                ]

                # Redirect to financial_support with supports as query parameters
                query_params = urlencode({'supports': json.dumps(supports)})
                return redirect(f'/financial-support/?{query_params}')
        except Exception as e:
            # Redirect with an error message
            query_params = urlencode({'error': str(e)})
            return redirect(f'/financial-support/?{query_params}')
    # Redirect for invalid request method
    query_params = urlencode({'error': "Invalid request method"})
    return redirect(f'/financial-support/?{query_params}')

def save_user_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON payload

            # Extract the email address from the basic_questions
            email = next(
                (item["answer"] for item in data.get("basic_questions", []) if item["question"] == "Email address"),
                None
            )

            if not email:
                return JsonResponse({"success": False, "error": "Email address is required."})

            # Get or create the UserProfile for the logged-in user
            user_profile, created = UserProfile.objects.get_or_create(email=email)

            # Update basic questions
            user_profile.faculty = next(
                (item["answer"] for item in data.get("basic_questions", []) if item["question"] == "Faculty of student"), 
                user_profile.faculty
            )
            user_profile.ects_amount = next(
                (int(item["answer"]) for item in data.get("basic_questions", []) if item["question"] == "Amount of ECTS this year"), 
                user_profile.ects_amount
            )
            user_profile.domicile = next(
                (item["answer"] for item in data.get("basic_questions", []) if item["question"] == "Domicile"), 
                user_profile.domicile
            )

            # Update income questions
            user_profile.annual_family_income = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Annual family income"), 
                user_profile.annual_family_income
            )
            user_profile.cadastral_income_rental = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Cadastral income (rental)"), 
                user_profile.cadastral_income_rental
            )
            user_profile.cadastral_income_business = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Cadastral income (business)"), 
                user_profile.cadastral_income_business
            )
            user_profile.separable_taxable_incomes = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Separable taxable incomes"), 
                user_profile.separable_taxable_incomes
            )
            user_profile.alimentation_money = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Alimentation money"), 
                user_profile.alimentation_money
            )
            user_profile.living_wages = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Living wages"), 
                user_profile.living_wages
            )
            user_profile.income_replacement_allowance = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Income replacement allowance"), 
                user_profile.income_replacement_allowance
            )
            user_profile.foreign_incomes = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Foreign incomes"), 
                user_profile.foreign_incomes
            )
            user_profile.study_income = next(
                (float(item["answer"]) for item in data.get("income_questions", []) if item["question"] == "Study income"), 
                user_profile.study_income
            )

            # Save the updated profile
            user_profile.save()

            return JsonResponse({"success": True, "message": "Data saved successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request method."})



