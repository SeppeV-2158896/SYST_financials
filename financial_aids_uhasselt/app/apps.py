from django.apps import AppConfig
from django.db.utils import IntegrityError


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'  # Ensure this is your actual app name

    def ready(self):
        from app.models import Question  # Import inside the method to avoid premature import issues

        initial_questions = [
            "What is your name?",
            "How old are you?",
            "Where are you from?",
            "What is your favorite color?",
        ]

        for question_text in initial_questions:
            try:
                Question.objects.get_or_create(question_text=question_text)  # Use the correct field name
            except IntegrityError:
                pass  # Skip if the question already exists
