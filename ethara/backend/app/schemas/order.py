from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str = ""
    product_sku: str = ""
    quantity: int
    unit_price: float
    subtotal: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate] = Field(..., min_length=1)
    discount: float = Field(default=0.0, ge=0)
    tax: float = Field(default=0.0, ge=0)
    notes: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    discount: Optional[float] = None
    tax: Optional[float] = None
    notes: Optional[str] = None


class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_id: int
    customer_name: str = ""
    status: OrderStatus
    total_amount: float
    discount: float
    tax: float
    notes: Optional[str] = None
    items: List[OrderItemOut] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
