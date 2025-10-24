from django.urls import path 
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    ## path('signup/', views.admin_signup, name='signup'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('customers/', views.admin_customers, name='customers'),
    path('products/', views.admin_products, name='products'),
    path('orders/', views.admin_orders, name='orders'),
    path('logout/', views.admin_logout, name='logout'),
]