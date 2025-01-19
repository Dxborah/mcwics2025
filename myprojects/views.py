from django.shortcuts import render
from django.http import JsonResponse

# Home page view
def home(request):
    return render(request, 'home.html')

def allergies(request):
    return render(request, 'allergies/allergy-page.html')

# Health and Illness page view
def health_and_illness(request):
    return render(request, 'health_illness/illness-page.html')

# Health Lifestyle page view
def health_lifestyle(request):
    return render(request, 'health_lifestyle/healthy_lifestyle-page.html')