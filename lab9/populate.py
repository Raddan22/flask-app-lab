from app import create_app, db
from app.posts.models import User, Profile, Post, Tag, Comment

app = create_app()
with app.app_context():
    # 1. Створюємо користувачів
    user1 = User(username="user1", email="user1@example.com", password="pass1")
    user2 = User(username="user2", email="user2@example.com", password="pass2")
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # 2. Створюємо профілі (One-to-One)
    profile1 = Profile(bio="Bio of user1", avatar="avatar1.jpg", user_id=user1.id)
    profile2 = Profile(bio="Bio of user2", avatar="avatar2.jpg", user_id=user2.id)
    db.session.add_all([profile1, profile2])
    db.session.commit()
    
    # 3. Створюємо теги
    tag_tech = Tag(name="Tech")
    tag_art = Tag(name="Art")
    tag_science = Tag(name="Science")
    db.session.add_all([tag_tech, tag_art, tag_science])
    db.session.commit()
    
    # 4. Створюємо пости
    post1 = Post(
        title="Art of Pop Culture",
        content="Test content...",
        category="tech",
        user_id=user1.id,
        tags=[tag_tech, tag_art]
    )
    post2 = Post(
        title="Science News",
        content="Science content...",
        category="news",
        user_id=user2.id,
        tags=[tag_science]
    )
    post3 = Post(
        title="Tech Trends",
        content="Tech content...",
        category="tech",
        user_id=user1.id,
        tags=[tag_tech]
    )
    db.session.add_all([post1, post2, post3])
    db.session.commit()
    
    # 5. Створюємо коментарі
    comment1 = Comment(content="Great post!", post_id=post1.id)
    comment2 = Comment(content="Interesting!", post_id=post1.id)
    db.session.add_all([comment1, comment2])
    db.session.commit()
    
    print("Database populated successfully!")