from django.urls import path
from . import views 

app_name = 'storefront'

urlpatterns = [

    path('login/', views.customer_login, name = 'login'),
    path('signup/', views.customer_signup, name = 'signup'),
    path('additional_info/', views.additional_info, name = 'additional_info'),
    path('dashboard/', views.customer_dashboard, name ='dashboard'),
    path('logout/', views.customer_logout, name='logout'),
]