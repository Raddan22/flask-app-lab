import os
from tinydb import TinyDB, Query
from datetime import datetime

# Шлях до JSON-файлу бази даних
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'products.json')

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = TinyDB(DB_PATH)
products_table = db.table('products')
ProductQuery = Query()

def get_all_products():
    return products_table.all()

def get_product_by_id(product_id):
    return products_table.get(ProductQuery.id == product_id)

def add_product(data):
    # Генеруємо новий id (максимальний + 1)
    all_products = get_all_products()
    new_id = max([p['id'] for p in all_products], default=0) + 1
    
    product = {
        'id': new_id,
        'name': data['name'],
        'content': data['content'],
        'price': data['price'],
        'category': data['category'],
        'quantity': data['quantity'],
        'image': data['image'],
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    products_table.insert(product)
    return product

def update_product(product_id, data):
    products_table.update(data, ProductQuery.id == product_id)

def delete_product(product_id):
    products_table.remove(ProductQuery.id == product_id)
