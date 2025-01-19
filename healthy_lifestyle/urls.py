from django.urls import path
from . import views

urlpatterns = [
    path('', views.lifestyle_page, name='lifestyle_page'),
    path('diet_plan/', views.diet_plan, name='diet_plan'),  
]


