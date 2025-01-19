from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('allergy/', views.allergies, name = 'Allergies & Intolerances'),
    path('illness/', views.health_and_illness, name='Health Concerns'),
    path('lifestyle/', views.health_lifestyle, name='Healthy Lifestyle')
    #need to add more paths
]
