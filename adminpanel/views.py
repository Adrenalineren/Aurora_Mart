from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AdminProfile
from storefront.models import CustomerProfile #, Product, Cart
from django.contrib.auth import logout

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password) 
        
        if user is not None:
            # if the credentials are correct
            try:
                admin_profile = AdminProfile.objects.get(user=user)
                login(request, user)
                return redirect('adminpanel:dashboard')
            #logs the admin in and redirects to the dashboard
            except AdminProfile.DoesNotExist:
                messages.error(request, 'You do not have admin privileges')
                #if no adminprofile show error message
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
        AdminProfile.objects.create(user=user)
        login(request, user)
        
        messages.success(request, 'Admin account created successfully!')
        return redirect('adminpanel:dashboard')
    
    return render(request, 'adminpanel/signup.html')

@login_required
def admin_dashboard(request):
    # Check if user has admin profile
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)

        total_customers = 0
        total_products = 0
        total_orders = 0
        context = {
            'total_customers': total_customers,
            'total_products': total_products,
            'total_orders': total_orders,
        }
        return render(request, 'adminpanel/dashboard.html', context)
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('index')
@login_required
def admin_customers(request):
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        customers = CustomerProfile.objects.select_related('user').all()
        return render(request, 'adminpanel/customers.html', {'customers': customers})
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied.')
        return redirect('index')

@login_required
def admin_products(request):
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        products = Product.objects.select_related('category').all()
        return render(request, 'adminpanel/products.html', {'products': products})
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied.')
        return redirect('index')

@login_required
def admin_orders(request):
    try:
        admin_profile = AdminProfile.objects.get(user=request.user)
        orders = Cart.objects.filter(items__isnull=False).distinct().select_related('user').prefetch_related('items__product')
        return render(request, 'adminpanel/orders.html', {'orders': orders})
    except AdminProfile.DoesNotExist:
        messages.error(request, 'Access denied.')
        return redirect('index')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('adminpanel:login')