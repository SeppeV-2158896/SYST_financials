from django.db import migrations, models

def add_percentage_covered(apps, schema_editor):
    SupportSystem = apps.get_model('app', 'SupportSystem')
    
    # Add percentage covered for each support system
    support_percentages = {
        "Flemish Support": 100,
        "UHasselt Support 1": 75,
        "UHasselt Support 2": 65,
        "UHasselt Support 3": 55,
        "UHasselt Support 4": 45,
    }

    for name, percentage in support_percentages.items():
        support = SupportSystem.objects.filter(name=name).first()
        if support:
            support.percentage_covered = percentage
            support.save()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0007_supportsystem'),  # Update this to the latest migration file
    ]

    operations = [
        migrations.AddField(
            model_name='supportsystem',
            name='percentage_covered',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(add_percentage_covered),
    ]
