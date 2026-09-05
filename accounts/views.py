import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from billing.models import Subscription


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    active_sub = Subscription.objects.filter(user=request.user, active=True).order_by('-id').first()
    pending_payments = request.user.subscription_set.filter(payment__status='Pending')
    return render(request, 'accounts/dashboard.html', {
        'active_sub': active_sub,
        'has_pending': pending_payments.exists()
    })

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    profile = user.userprofile
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()

        profile.phone_number = request.POST.get('phone_number', '')
        profile.whatsapp_number = request.POST.get('whatsapp_number', '')
        
        if 'avatar' in request.FILES:
            if profile.avatar:
                if os.path.isfile(profile.avatar.path):
                    os.remove(profile.avatar.path)
            profile.avatar = request.FILES['avatar']
            
        profile.save()
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('dashboard')
        
    return render(request, 'accounts/edit_profile.html')
