import unittest
from app import create_app, db
from app.posts.models import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Створюємо застосунок у режимі тестування (використовує in-memory SQLite)
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        # Після кожного тесту очищаємо базу
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page(self):
        """Тест 1: Перевірка доступності сторінки реєстрації"""
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        """Тест 2: Перевірка доступності сторінки входу"""
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_user(self):
        """Тест 3: Перевірка збереження користувача в БД при реєстрації"""
        response = self.client.post('/users/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        # Перевіряємо, що пароль захешований (не дорівнює відкритому тексту)
        self.assertNotEqual(user.password, 'password123')
        # Перевіряємо, що хеш правильний
        self.assertTrue(user.check_password('password123'))

    def test_login_logout(self):
        """Тест 4: Перевірка входу та виходу користувача"""
        # 1. Створюємо користувача вручну
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # 2. Логін
        response = self.client.post('/users/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, testuser!', response.data)  # Перевіряємо привітання
        
        # 3. Вихід
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully logged out.', response.data)

if __name__ == '__main__':
    unittest.main()