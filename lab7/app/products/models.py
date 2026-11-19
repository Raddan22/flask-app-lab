from app import db
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

class Category(db.Model):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    
    products: Mapped[List["Product"]] = relationship(
        "Product",
        back_populates="category",
        lazy="select"
    )

class Product(db.Model):
    __tablename__ = 'products'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="products")
    
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Змінено на server_default (Частина 6)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )
    
    def __repr__(self) -> str:
        return f"Product {self.name} - ${self.price}"