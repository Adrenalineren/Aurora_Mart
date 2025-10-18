from django.urls import path 
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('signup/', views.admin_signup, name='signup'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
]