from app import create_app, db
from app.posts.models import Post
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

app = create_app()
with app.app_context():
    print("=== БЕЗ оптимізації ===")
    stmt = select(Post).order_by(Post.id.desc())
    posts = db.session.scalars(stmt).all()
    for post in posts:
        print(post.title, post.user.username, [tag.name for tag in post.tags])
    
    print("\n=== З оптимізацією (joinedload + selectinload) ===")
    stmt = (
        select(Post)
        .options(
            joinedload(Post.user),
            selectinload(Post.tags)
        )
        .order_by(Post.id.desc())
    )
    posts = db.session.scalars(stmt).all()
    for post in posts:
        print(post.title, post.user.username, [tag.name for tag in post.tags])