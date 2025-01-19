from django.urls import path
from . import views

urlpatterns = [
    path('allergy-page', views.allergy_meals_view, name='allergy-page'),
]

