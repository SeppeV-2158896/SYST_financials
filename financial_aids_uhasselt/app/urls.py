from django.urls import path
from . import views

urlpatterns = [
    # Example URL patterns
    path('', views.index, name='index'),  # Home page
    path('simulate/', views.simulate, name='simulate'),  # Simulate page
    path('financial-overview/', views.financial_overview, name='financial_overview'),
    path('financial-support/', views.financial_support, name='financial_support'),
]