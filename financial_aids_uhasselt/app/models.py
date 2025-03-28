from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    
class FinancialSupport(models.Model):
    applicable = models.BooleanField(default=False)

    def __str__(self):
        return f"Financial Support (Applicable: {self.applicable})"