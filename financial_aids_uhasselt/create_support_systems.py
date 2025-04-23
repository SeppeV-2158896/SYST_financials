from app.models import SupportSystem

def add_support_systems():
    SupportSystem.objects.all().delete()
    
    systems = [
        {"name": "Flemish Support", "description": "Support for categories 0-3", "min_category": 0, "max_category": 3, "link": "https://www.studietoelagen.be/"},
        {"name": "UHasselt Support 1", "description": "UHasselt support for category 1", "min_category": 1, "max_category": 1, "link": "http://127.0.0.1:8000/calendar/"},
        {"name": "UHasselt Support 2", "description": "UHasselt support for category 2", "min_category": 1, "max_category": 2, "link": "http://127.0.0.1:8000/calendar/"},
        {"name": "UHasselt Support 3", "description": "UHasselt support for category 3", "min_category": 1, "max_category": 3, "link": "http://127.0.0.1:8000/calendar/"},
        {"name": "UHasselt Support 4", "description": "UHasselt support for category 4", "min_category": 0, "max_category": 4, "link": "http://127.0.0.1:8000/calendar/"},
    ]

    for system in systems:
        SupportSystem.objects.get_or_create(**system)

add_support_systems()