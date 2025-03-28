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

        for question_text in initial_questions:
            try:
                Question.objects.get_or_create(question_text=question_text)  # Use the correct field name
            except IntegrityError:
                pass  # Skip if the question already exists
