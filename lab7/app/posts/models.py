from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Enum, Boolean
from app import db

class Post(db.Model):
    __tablename__ = 'posts'
    
    # Сучасний синтаксис 2.0
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[str] = mapped_column(
        Enum('news', 'publication', 'tech', 'other', name='category_enum'), 
        default='other'
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    author: Mapped[Optional[str]] = mapped_column(String(20), default='Anonymous')

    def __repr__(self):
        return f'<Post {self.title}>'