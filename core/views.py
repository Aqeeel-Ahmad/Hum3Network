from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback
from support.models import Complaint
from billing.models import Package

def home(request):
    packages = Package.objects.filter(active=True).order_by('price')[:3]
    return render(request, 'core/home.html', {'packages': packages})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def submit_feedback(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        message = request.POST.get('message')
        if name and email and rating and message:
            Feedback.objects.create(name=name, email=email, rating=rating, message=message)
            messages.success(request, 'Thank you for your feedback!')
    return redirect('home')

def submit_complaint(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to submit a complaint.')
            return redirect('login')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        if subject and description:
            Complaint.objects.create(user=request.user, subject=subject, description=description)
            messages.success(request, 'Your complaint has been submitted and will be reviewed shortly.')
    return redirect('home')
