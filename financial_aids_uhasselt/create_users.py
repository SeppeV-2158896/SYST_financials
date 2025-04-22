from django.contrib.auth.hashers import make_password
from app.models import UserProfile
from decimal import Decimal

# Pseudo users data
fake_users = [
    {
        "email": "alice@example.com",
        "password": "alice123",
        "faculty": "Engineering",
        "ects_amount": 60,
        "domicile": "Brussels",
        "annual_family_income": 24000.00,
        "cadastral_income_rental": 1500.00,
        "cadastral_income_business": 2000.00,
        "separable_taxable_incomes": 500.00,
        "alimentation_money": 0.00,
        "living_wages": 8000.00,
        "income_replacement_allowance": 1200.00,
        "foreign_incomes": 300.00,
    },
    {
        "email": "bob@example.com",
        "password": "bob123",
        "faculty": "Law",
        "ects_amount": 45,
        "domicile": "Antwerp",
        "annual_family_income": 32000.00,
        "cadastral_income_rental": 0.00,
        "cadastral_income_business": 500.00,
        "separable_taxable_incomes": 1500.00,
        "alimentation_money": 100.00,
        "living_wages": 9000.00,
        "income_replacement_allowance": 500.00,
        "foreign_incomes": 0.00,
    },
    {
        "email": "carol@example.com",
        "password": "carol123",
        "faculty": "Medicine",
        "ects_amount": 60,
        "domicile": "Ghent",
        "annual_family_income": 18000.00,
        "cadastral_income_rental": 2000.00,
        "cadastral_income_business": 0.00,
        "separable_taxable_incomes": 0.00,
        "alimentation_money": 200.00,
        "living_wages": 8500.00,
        "income_replacement_allowance": 1500.00,
        "foreign_incomes": 500.00,
    },
    {
        "email": "dave@example.com",
        "password": "dave123",
        "faculty": "Economics",
        "ects_amount": 30,
        "domicile": "Leuven",
        "annual_family_income": 40000.00,
        "cadastral_income_rental": 3000.00,
        "cadastral_income_business": 1000.00,
        "separable_taxable_incomes": 1000.00,
        "alimentation_money": 0.00,
        "living_wages": 7500.00,
        "income_replacement_allowance": 0.00,
        "foreign_incomes": 0.00,
    },
    {
        "email": "eve@example.com",
        "password": "eve123",
        "faculty": "Arts",
        "ects_amount": 60,
        "domicile": "Namur",
        "annual_family_income": 15000.00,
        "cadastral_income_rental": 0.00,
        "cadastral_income_business": 0.00,
        "separable_taxable_incomes": 200.00,
        "alimentation_money": 150.00,
        "living_wages": 9500.00,
        "income_replacement_allowance": 0.00,
        "foreign_incomes": 100.00,
    },
]

# Loop through each user and create a UserProfile
for user in fake_users:
    # Hash password securely
    hashed_password = make_password(user["password"])
    
    # Create a UserProfile object and save it to the database
    profile = UserProfile(
        email=user["email"],
        password=hashed_password,
        faculty=user["faculty"],
        ects_amount=user["ects_amount"],
        domicile=user["domicile"],
        annual_family_income=Decimal(user["annual_family_income"]),
        cadastral_income_rental=Decimal(user["cadastral_income_rental"]),
        cadastral_income_business=Decimal(user["cadastral_income_business"]),
        separable_taxable_incomes=Decimal(user["separable_taxable_incomes"]),
        alimentation_money=Decimal(user["alimentation_money"]),
        living_wages=Decimal(user["living_wages"]),
        income_replacement_allowance=Decimal(user["income_replacement_allowance"]),
        foreign_incomes=Decimal(user["foreign_incomes"]),
    )
    
    # Save to the database
    profile.save()

print("✅ 5 pseudo users added successfully.")
