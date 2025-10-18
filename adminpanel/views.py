from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AdminProfile

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user is an admin
            try:
                admin_profile = AdminProfile.objects.get(user=user)
                login(request, user)
                return redirect('adminpanel:dashboard')
            except AdminProfile.DoesNotExist:
                messages.error(request, 'You do not have admin privileges')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'adminpanel/login.html')

def admin_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'adminpanel/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'adminpanel/signup.html')
        
        # Create admin user
        user = User.objects.create_user(username=username, password=password, is_staff=True)
        
        # Create admin profile
        AdminProfile.objects.create(user=user)
        
        # Log them in
        login(request, user)
        
        messages.success(request, 'Admin account created successfully!')
        return redirect('adminpanel:dashboard')
    
    return render(request, 'adminpanel/signup.html')

@login_required
def admin_dashboard(request):
    # Check if user has admin profile
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        return render(request, 'adminpanel/dashboard.html')
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('index')