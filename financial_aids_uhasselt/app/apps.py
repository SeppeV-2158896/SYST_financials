from django.apps import AppConfig
from django.db.utils import IntegrityError


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Ensure this is your actual app name

    def ready(self):
        from app.models import Question  # Import inside the method to avoid premature import issues

        initial_questions = [
            "Annual family income (in euros)",
            "Cadastral income (rental properties)",
            "Cadastral income (business properties)",
            "Separable taxable incomes(such as bonuses, early vacation bonus)",
            "Alimentation money(if applicable)",
            "Living wages",
            "Income replacement allowance",
            "Foreign incomes",
        ]
        
        #---gebruik deze line om vragen die nog in db waren te verwijderen---
        Question.objects.all().delete()
        basic_questions = [
            "Email address",
            "Faculty of student",
            "Amount of ECTS this year",
            "Domicile",
        ]
        
        yes_no_questions = [
            "Are you staying in a student room?",
            "Have you bought your laptop through the university?",
        ]
        
        for question_text in initial_questions:
            try:
                Question.objects.get_or_create(question_text=question_text)  # Use the correct field name
            except IntegrityError:
                pass  # Skip if the question already exists

        for question_text in basic_questions:
            try:
                Question.objects.get_or_create(question_text = question_text)
            except IntegrityError:
                pass
        for question_text in yes_no_questions:
            try:
                Question.objects.get_or_create(question_text=question_text)  # Use the correct field name
            except IntegrityError:
                pass  # Skip if the question already exists