import unittest
from app import create_app, db
from app.posts.models import Post

class TestPostsCRUD(unittest.TestCase):
    def setUp(self):
        # Створюємо застосунок у режимі тестування (використовує in-memory SQLite)
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Створюємо таблиці в тестовій базі
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        # Після кожного тесту видаляємо сесію та таблиці
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Тест створення (Create)"""
        response = self.client.post('/post/create', data={
            'title': 'Тестовий пост',
            'content': 'Це контент тестового поста',
            'category': 'news',
            'enabled': 'y',  # BooleanField передається як 'y'
            'publish_date': '2026-11-11T12:00'
        }, follow_redirects=True)
        
        # Перевіряємо, що сторінка завантажилась успішно (200 OK)
        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо, що пост з'явився в базі
        post = Post.query.first()
        self.assertIsNotNone(post)
        self.assertEqual(post.title, 'Тестовий пост')
        self.assertEqual(post.category, 'news')
        self.assertEqual(post.author, 'Anonymous') # Бо сесії немає

    def test_read_posts_list(self):
        """Тест читання списку (Read)"""
        # Спочатку додаємо пост вручну
        post = Post(title='Пост для списку', content='Контент', is_active=True)
        db.session.add(post)
        db.session.commit()

        response = self.client.get('/post')
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи є назва поста в HTML
        self.assertIn(b'\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82 \xd0\xb4\xd0\xbb\xd1\x8f \xd1\x81\xd0\xbf\xd0\xb8\xd1\x81\xd0\xba\xd1\x83', response.data) # "Пост для списку" в байтах

    def test_read_detail_post(self):
        """Тест читання деталей (Read)"""
        post = Post(title='Детальний пост', content='Повний текст', is_active=True)
        db.session.add(post)
        db.session.commit()

        response = self.client.get(f'/post/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\x94\xd0\xb5\xd1\x82\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\xbf\xd0\xbe\xd1\x81\xd1\x82', response.data) # "Детальний пост"

    def test_update_post(self):
        """Тест редагування (Update)"""
        post = Post(title='Стара назва', content='Старий контент', is_active=True)
        db.session.add(post)
        db.session.commit()

        response = self.client.post(f'/post/{post.id}/update', data={
            'title': 'Нова назва',
            'content': 'Новий контент',
            'category': 'tech',
            'enabled': 'y'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        updated_post = db.session.get(Post, post.id)
        self.assertEqual(updated_post.title, 'Нова назва')
        self.assertEqual(updated_post.content, 'Новий контент')

    def test_delete_post(self):
        """Тест видалення (Delete)"""
        post = Post(title='Пост на видалення', content='Контент', is_active=True)
        db.session.add(post)
        db.session.commit()
        post_id = post.id

        # Перевіряємо, що він є
        self.assertIsNotNone(db.session.get(Post, post_id))

        # Відправляємо POST-запит на видалення
        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Перевіряємо, що його більше немає
        self.assertIsNone(db.session.get(Post, post_id))

if __name__ == '__main__':
    unittest.main()