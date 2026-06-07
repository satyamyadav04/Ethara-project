from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sku: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = None
    price: float = Field(..., gt=0)
    cost_price: Optional[float] = None
    stock_quantity: int = Field(default=0, ge=0)
    low_stock_threshold: int = Field(default=10, ge=0)
    unit: str = "pcs"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    stock_quantity: Optional[int] = None
    low_stock_threshold: Optional[int] = None
    unit: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_low_stock: bool = False

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        instance = super().model_validate(obj, *args, **kwargs)
        instance.is_low_stock = obj.stock_quantity <= obj.low_stock_threshold
        return instance
