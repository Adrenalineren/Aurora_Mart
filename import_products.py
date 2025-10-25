import os
import django
import csv

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auroramart.settings')  # Replace with your project name
django.setup()

from storefront.models import Product  # Replace with your app name

csv_file = '/Users/aswinraja/Downloads/IS2108 - AY2526S1 - Pair Project 2/data/b2c_products_500.csv'

with open(csv_file, 'r', encoding='latin-1') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        Product.objects.update_or_create(
            sku_code=row['sku_code'],
            defaults={
                'product_name': row['product_name'],
                'product_description': row['product_description'],
                'product_category': row['product_category'],
                'product_subcategory': row['product_subcategory'],
                'quantity_on_hand': int(row['quantity_on_hand']),
                'reorder_quantity': int(row['reorder_quantity']),
                'unit_price': float(row['unit_price']),
                'product_rating': float(row['product_rating']),
            }
        )
        print(f'Imported: {row["product_name"]}')

print('Import completed!')
