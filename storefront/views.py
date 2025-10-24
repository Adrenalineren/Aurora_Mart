"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            profile, created = CustomerProfile.objects.get_or_create(user=user)
            if profile.profile_completed:
                return redirect('storefront:dashboard')
            else:
                return redirect('storefront:additional_info')
        else:
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
        profile.occupation = request.POST.get('occupation')
        profile.education = request.POST.get('education')
        if 'household_size' in request.POST:
            profile.household_size = request.POST.get('household_size')
        if 'has_children' in request.POST:
            profile.has_children = True
        else:
            profile.has_children = False
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
    return redirect('storefront:customer_login')
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomerProfile
from adminpanel.models import AdminProfile
from storefront.models import CustomerProfile

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # CHECK IF USER IS ADMIN
            from adminpanel.models import AdminProfile
            if AdminProfile.objects.filter(user=user).exists():
                # This is an admin, send to admin dashboard
                return redirect('adminpanel:dashboard')
            
            # Regular customer flow
            profile, created = CustomerProfile.objects.get_or_create(user=user)
            if profile.profile_completed:
                return redirect('storefront:dashboard')
            else:
                return redirect('storefront:additional_info')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'storefront/login.html')


def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'storefront/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'storefront/signup.html')
        
        # CREATE REGULAR USER (NOT ADMIN)
        user = User.objects.create_user(username=username, password=password)
        CustomerProfile.objects.create(user=user)
        login(request, user)
        
        return redirect('storefront:additional_info')
    
    return render(request, 'storefront/signup.html')


@login_required
def additional_info(request):
    # IF ADMIN SOMEHOW GETS HERE, REDIRECT THEM
    from adminpanel.models import AdminProfile
    if AdminProfile.objects.filter(user=request.user).exists():
        return redirect('adminpanel:dashboard')
    
    profile = CustomerProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile.age = request.POST.get('age')
        profile.gender = request.POST.get('gender')
        profile.employment_status = request.POST.get('employment_status')
        profile.income_range = request.POST.get('income_range')
        profile.occupation = request.POST.get('occupation', '')
        profile.education = request.POST.get('education', '')
        profile.household_size = request.POST.get('household_size', 1)
        profile.has_children = 'has_children' in request.POST
        profile.profile_completed = True
        profile.save()
        
        messages.success(request, 'Profile completed successfully!')
        return redirect('storefront:dashboard')
    
    return render(request, 'storefront/additional_info.html')


def customer_dashboard(request):
    # Check if user is an admin
    if AdminProfile.objects.filter(user=request.user).exists():
        profile = None  # Admins don’t have a CustomerProfile
    else:
        # Try to get the customer profile
        try:
            profile = CustomerProfile.objects.get(user=request.user)
        except CustomerProfile.DoesNotExist:
            messages.error(request, "No customer profile found. Please sign up as a customer.")
            return redirect('storefront:signup')

    context = {
        'profile': profile,
        'is_admin': AdminProfile.objects.filter(user=request.user).exists(),
    }
    return render(request, 'storefront/dashboard.html', context)


def customer_logout(request):
    logout(request)
    return redirect('storefront:login')