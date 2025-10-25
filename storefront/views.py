from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from .models import Product

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            try:
                profile = CustomerProfile.objects.get(user=user)
                if profile.profile_completed:
                    return redirect('storefront:dashboard')
                else:
                    return redirect('storefront:additional_info')
            except CustomerProfile.DoesNotExist:
                return redirect('storefront:additional_info')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'storefront/login.html')

def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # check if same
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'storefront/signup.html')
        # check if got existing 
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'storefront/signup.html')
        
        # create user 
        user = User.objects.create_user(username=username, password=password)
        
        # create empty profile
        CustomerProfile.objects.create(user=user)
        
        # loggin them in
        login(request, user)
        
        # redirect to additional info
        return redirect('storefront:additional_info')
    
    return render(request, 'storefront/signup.html')

@login_required
def additional_info(request):
    profile = CustomerProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.employment_status = request.POST.get('employment_status')
        profile.income_range = request.POST.get('income_range')
        profile.profile_completed = True
        profile.save()
        
        messages.success(request, 'Profile completed successfully!')
        return redirect('storefront:dashboard')
    
    return render(request, 'storefront/additional_info.html')

@login_required
def customer_dashboard(request):
    profile = CustomerProfile.objects.get(user=request.user)
    context = {
        'profile':profile
    }
    return render(request, 'storefront/dashboard.html', context)

def customer_logout(request):
    logout(request)
    return redirect('storefront:login')
