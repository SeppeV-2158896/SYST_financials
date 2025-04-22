from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=200, unique=True)
    tag = models.CharField(max_length=50, unique=True, null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.question_text
    
class FinancialSupport(models.Model):
    applicable = models.BooleanField(default=False)

    def __str__(self):
        return f"Financial Support (Applicable: {self.applicable})"
    
class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)  # You'd normally use Django's built-in User model with hashing

    # Basic questions
    email = models.EmailField()
    faculty = models.CharField(max_length=100)
    ects_amount = models.PositiveIntegerField()
    domicile = models.CharField(max_length=255)
    living_unit_points = models.IntegerField(null=True, blank=True)  # Points for living unit

    # Financial questions
    annual_family_income = models.DecimalField(max_digits=12, decimal_places=2)
    cadastral_income_rental = models.DecimalField(max_digits=12, decimal_places=2)
    cadastral_income_business = models.DecimalField(max_digits=12, decimal_places=2)
    separable_taxable_incomes = models.DecimalField(max_digits=12, decimal_places=2)
    alimentation_money = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    living_wages = models.DecimalField(max_digits=12, decimal_places=2)
    income_replacement_allowance = models.DecimalField(max_digits=12, decimal_places=2)
    foreign_incomes = models.DecimalField(max_digits=12, decimal_places=2)

    study_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.email
    
class IncomeThreshold(models.Model):
    punten_leefeenheid = models.IntegerField()

    # Studietoelage income ranges
    min_inkomensgrens = models.DecimalField(max_digits=10, decimal_places=2)
    max_inkomensgrens = models.DecimalField(max_digits=10, decimal_places=2)

    # UHasselt Categories
    categorie_1 = models.DecimalField(max_digits=10, decimal_places=2)
    categorie_2 = models.DecimalField(max_digits=10, decimal_places=2)
    categorie_3 = models.DecimalField(max_digits=10, decimal_places=2)
    categorie_4 = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Punten {self.punten_leefeenheid}"