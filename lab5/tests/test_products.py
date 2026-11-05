import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.products import models

class TestProductCRUD(unittest.TestCase):
    def setUp(self):
        models.products_table.truncate()
        
    def tearDown(self):
        models.products_table.truncate()

    def test_add_product(self):
        """Тест створення (Create)"""
        data = {
            'name': 'Тестовий товар',
            'content': 'Опис тестового товару',
            'price': 99.99,
            'category': 'electronics',
            'quantity': 10,
            'image': None
        }
        product = models.add_product(data)
        
        self.assertIsNotNone(product['id'])
        self.assertEqual(product['id'], 1)
        
        all_products = models.get_all_products()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0]['name'], 'Тестовий товар')

    def test_get_product(self):
        """Тест читання (Read)"""
        data = {'name': 'Товар для читання', 'content': 'Опис', 'price': 50.0, 'category': 'other', 'quantity': 5, 'image': None}
        added = models.add_product(data)
        
        product = models.get_product_by_id(added['id'])
        
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], 'Товар для читання')
        
        self.assertIsNone(models.get_product_by_id(999))

    def test_update_product(self):
        """Тест редагування (Update)"""
        data = {'name': 'Стара назва', 'content': 'Старий опис', 'price': 10.0, 'category': 'food', 'quantity': 1, 'image': None}
        added = models.add_product(data)
        
        new_data = {'name': 'Нова назва', 'price': 20.0}
        models.update_product(added['id'], new_data)
        
        updated = models.get_product_by_id(added['id'])
        self.assertEqual(updated['name'], 'Нова назва')
        self.assertEqual(updated['price'], 20.0)
        # Перевіряємо, що старі дані, яких не торкалися, залишилися
        self.assertEqual(updated['category'], 'food')

    def test_delete_product(self):
        """Тест видалення (Delete)"""
        data = {'name': 'Товар на видалення', 'content': 'Опис', 'price': 5.0, 'category': 'other', 'quantity': 1, 'image': None}
        added = models.add_product(data)
        
        self.assertIsNotNone(models.get_product_by_id(added['id']))
        
        
        models.delete_product(added['id'])
        
        self.assertIsNone(models.get_product_by_id(added['id']))
        self.assertEqual(len(models.get_all_products()), 0)

if __name__ == '__main__':
    unittest.main()
