from app.models import SupportSystem

# Add or update Flemish Support
flemish_support, created = SupportSystem.objects.get_or_create(name="Flemish Support")
flemish_support.description = "Support for Flemish students"
flemish_support.min_category = 1
flemish_support.max_category = 4
flemish_support.link = "https://www.studietoelagen.be/"
flemish_support.save()

# Add or update UHasselt Support 1–4
for i in range(1, 5):
    uhasselt_support, created = SupportSystem.objects.get_or_create(name=f"UHasselt Support {i}")
    uhasselt_support.description = f"UHasselt Support Category {i}"
    uhasselt_support.min_category = i
    uhasselt_support.max_category = i
    uhasselt_support.link = "/calendar/"
    uhasselt_support.save()