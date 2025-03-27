from django.urls import path
from . import views

urlpatterns = [
    # Example URL patterns
    path('', views.index, name='index'),  # Home page
]