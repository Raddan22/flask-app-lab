import unittest
import os
import sys

# Додаємо шлях до кореня проєкту, щоб імпортувати модулі
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.products import models

class TestProductCRUD(unittest.TestCase):
    def setUp(self):
        # Перед кожним тестом очищаємо базу даних, щоб тести не впливали один на одного
        models.products_table.truncate()
        
    def tearDown(self):
        # Після кожного тесту також очищаємо базу
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
        
        # Перевіряємо, чи створився ID
        self.assertIsNotNone(product['id'])
        self.assertEqual(product['id'], 1)
        
        # Перевіряємо, чи є товар у базі
        all_products = models.get_all_products()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0]['name'], 'Тестовий товар')

    def test_get_product(self):
        """Тест читання (Read)"""
        # Спочатку додаємо товар
        data = {'name': 'Товар для читання', 'content': 'Опис', 'price': 50.0, 'category': 'other', 'quantity': 5, 'image': None}
        added = models.add_product(data)
        
        # Читаємо його за ID
        product = models.get_product_by_id(added['id'])
        
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], 'Товар для читання')
        
        # Перевіряємо, що неіснуючий товар повертає None
        self.assertIsNone(models.get_product_by_id(999))

    def test_update_product(self):
        """Тест редагування (Update)"""
        # Додаємо товар
        data = {'name': 'Стара назва', 'content': 'Старий опис', 'price': 10.0, 'category': 'food', 'quantity': 1, 'image': None}
        added = models.add_product(data)
        
        # Оновлюємо його
        new_data = {'name': 'Нова назва', 'price': 20.0}
        models.update_product(added['id'], new_data)
        
        # Перевіряємо зміни
        updated = models.get_product_by_id(added['id'])
        self.assertEqual(updated['name'], 'Нова назва')
        self.assertEqual(updated['price'], 20.0)
        # Перевіряємо, що старі дані, яких не торкалися, залишилися
        self.assertEqual(updated['category'], 'food')

    def test_delete_product(self):
        """Тест видалення (Delete)"""
        # Додаємо товар
        data = {'name': 'Товар на видалення', 'content': 'Опис', 'price': 5.0, 'category': 'other', 'quantity': 1, 'image': None}
        added = models.add_product(data)
        
        # Перевіряємо, що він є
        self.assertIsNotNone(models.get_product_by_id(added['id']))
        
        # Видаляємо
        models.delete_product(added['id'])
        
        # Перевіряємо, що його більше немає
        self.assertIsNone(models.get_product_by_id(added['id']))
        self.assertEqual(len(models.get_all_products()), 0)

if __name__ == '__main__':
    unittest.main()