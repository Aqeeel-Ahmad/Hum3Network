from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('complaint/', views.submit_complaint, name='submit_complaint'),
]
