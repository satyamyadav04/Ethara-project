from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class CustomerOut(CustomerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    total_orders: int = 0

    model_config = {"from_attributes": True}
