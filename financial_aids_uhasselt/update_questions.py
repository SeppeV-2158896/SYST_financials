import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_aids_uhasselt.settings')
django.setup()

from app.models import Question

# List of questions to add with their tags
questions = [
    {"text": "Email address", "tag": "email"},
    {"text": "Faculty of student", "tag": "faculty"},
    {"text": "Amount of ECTS this year", "tag": "ects_amount"},
    {"text": "Domicile", "tag": "domicile"},
    {"text": "Living unit points", "tag": "living_unit_points"},
    {"text": "Annual family income", "tag": "annual_family_income"},
    {"text": "Cadastral income (rental)", "tag": "cadastral_income_rental"},
    {"text": "Cadastral income (business)", "tag": "cadastral_income_business"},
    {"text": "Separable taxable incomes", "tag": "separable_taxable_incomes"},
    {"text": "Alimentation money", "tag": "alimentation_money"},
    {"text": "Living wages", "tag": "living_wages"},
    {"text": "Income replacement allowance", "tag": "income_replacement_allowance"},
    {"text": "Foreign incomes", "tag": "foreign_incomes"},
    {"text": "Study income", "tag": "study_income"},
]

def reset_questions():
    """
    Clears the Question table and populates it with predefined questions.
    """
    # Clear the table
    Question.objects.all().delete()
    print("Cleared all existing questions.")

    # Add new questions with tags
    for question in questions:
        Question.objects.create(text=question["text"], tag=question["tag"])
        print(f"Added question: {question['text']} with tag: {question['tag']}")

if __name__ == "__main__":
    reset_questions()

