from django.db import models
from django.contrib.auth.models import User 

class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('male', "Male"),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    EMPLOYMENT_STATUS = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('self_employed', 'Self-Employed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
    ]
    OCCUPATION = [
        ('admin', 'Admin'),
        ('education', 'Education'),
        ('sales', 'Sales'),
        ('service', 'Service'),
        ('skilled_trades', 'Skilled Trade'),
        ('tech', 'Tech'),
    ]

    EDUCATION = [
        ('bachelor', 'Bachelor'),
        ('diploma', 'Diploma'),
        ('doctorate', 'Doctorate'),
        ('master', 'Master'),
        ('secondary', 'Secondary'),
    ]
    INCOME_RANGE = [
        ('below_25k', '$0 - 25,000'),
        ('25k-50k', '$25,000 - $50,000'),
        ('50k-75k', '$50,000 - $75,000'),
        ('75k-100k', '$75,000 - $100,000'),
        ('above_100k', '$100,000+'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS, null=True, blank=True)
    occupation = models.CharField(max_length=20, choices=OCCUPATION, null=True, blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION, null=True, blank=True)
    household_size = models.IntegerField(null=True, blank=True)
    has_children = models.BooleanField(default=False)
    income_range = models.CharField(max_length=20, choices=INCOME_RANGE, null=True, blank=True)
    profile_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Product(models.Model):
    sku_code = models.CharField(max_length=100, unique=True, primary_key= True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_category = models.CharField(max_length=100)
    product_subcategory = models.CharField(max_length=100, blank=True, null=True)
    quantity_on_hand = models.IntegerField(default=0)
    reorder_quantity = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_rating = models.FloatField(default=0)


    def __str__(self):
        return self.product_name

