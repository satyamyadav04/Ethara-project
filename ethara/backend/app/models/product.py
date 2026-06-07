from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=True)
    stock_quantity = Column(Integer, default=0, nullable=False)
    low_stock_threshold = Column(Integer, default=10)
    unit = Column(String(50), default="pcs")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order_items = relationship("OrderItem", back_populates="product")
