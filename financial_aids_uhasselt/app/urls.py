from django.urls import path
from django.views.generic import TemplateView
from app import views

urlpatterns = [
    # Example URL patterns
    path('', views.index, name='index'),  # Home page
    path('simulate/', views.simulate, name='simulate'),  # Simulate page
    path('financial-overview/', views.financial_overview, name='financial_overview'),
    path('financial-support/', views.financial_support, name='financial_support'),
    path("calculate-income/", views.calculate_income_view, name="calculate_income"),
    path('save-data/', views.save_user_data, name='save_user_data'),
    path('calendar/', TemplateView.as_view(template_name="calendar.html"), name='calendar'),
]