import random
from app.models import UserProfile, HistoricalData

def populate_historical_data():
    HistoricalData.objects.all().delete()
    school_years = ["2024-2025", "2023-2024", "2022-2023", "2021-2022", "2020-2021", "2019-2020"]

    users = UserProfile.objects.all()

    for user in users:
        # Ensure at least one entry for 2024-2025
        HistoricalData.objects.create(
            user=user,
            school_year="2024-2025",
            income=random.uniform(15000, 30000),
            study_expenses_tuition=random.uniform(5000, 10000),
            study_expenses_books=random.uniform(1000, 3000),
            study_expenses_housing=random.uniform(2000, 5000),
            financial_aid_scholarship=random.uniform(1000, 3000),
            financial_aid_grant=random.uniform(1000, 2000),
        )

        # Add 1-5 additional entries for random school years
        for _ in range(random.randint(1, 5)):
            year = random.choice(school_years)
            HistoricalData.objects.create(
                user=user,
                school_year=year,
                income=random.uniform(15000, 30000),
                study_expenses_tuition=random.uniform(5000, 10000),
                study_expenses_books=random.uniform(1000, 3000),
                study_expenses_housing=random.uniform(2000, 5000),
                financial_aid_scholarship=random.uniform(1000, 3000),
                financial_aid_grant=random.uniform(1000, 2000),
            )

populate_historical_data()