import pandas as pd
from storefront.models import Product

# Path to your Excel file
file_path = "/Users/aswinraja/Desktop/IS2108/IS2108 - AY2526S1 - Pair Project/data/b2c_products_500.csv"

# Read the Excel file
df = pd.read_excel(file_path)

for _, row in df.iterrows():
    Product.objects.update_or_create(
        sku=row['SKU'],
        defaults={
            'name': row['name'],
            'description': row['description'],
            'category': row['category'],
            'subcategory': row.get('subcategory', ''),
            'price': row['price'],
            'rating': row.get('rating', 0),
            'stock': row.get('stock', 0),
            'reorder_threshold': row.get('reorder threshold', 0),
        }
    )

print("Product data imported successfully!")
