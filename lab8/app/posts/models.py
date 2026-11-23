from app import db
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional, List

# Асоціативна таблиця для Many-to-Many (Post <-> Tag)
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    
    # One-to-Many: User -> Posts
    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    # One-to-One: User -> Profile
    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Profile(db.Model):
    __tablename__ = 'profiles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[Optional[str]] = mapped_column(String(255))
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    
    # One-to-One: Profile -> User
    user: Mapped["User"] = relationship(back_populates="profile")

class Post(db.Model):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    publish_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[Optional[str]] = mapped_column(String(50))
    
    # One-to-Many: Post -> User
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'))
    user: Mapped[Optional["User"]] = relationship(back_populates="posts")
    
    # One-to-Many: Post -> Comments
    comments: Mapped[List["Comment"]] = relationship(back_populates="post", cascade="all, delete-orphan")
    
    # Many-to-Many: Post <-> Tags
    tags: Mapped[List["Tag"]] = relationship(secondary=post_tags, back_populates="posts")
    
    def __repr__(self):
        return f"Post('{self.title}')"

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    # Many-to-Many: Tag <-> Posts
    posts: Mapped[List["Post"]] = relationship(secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"Tag('{self.name}')"

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # One-to-Many: Comment -> Post
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped["Post"] = relationship(back_populates="comments")