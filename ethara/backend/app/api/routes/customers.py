from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.services import customer_service
from typing import List, Optional

router = APIRouter()


@router.get("/", response_model=List[CustomerOut])
def list_customers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    customers = customer_service.get_customers(db, skip, limit, search)
    result = []
    for c in customers:
        c_out = CustomerOut.model_validate(c)
        c_out.total_orders = customer_service.get_customer_order_count(db, c.id)
        result.append(c_out)
    return result


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    c_out = CustomerOut.model_validate(customer)
    c_out.total_orders = customer_service.get_customer_order_count(db, customer_id)
    return c_out


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    existing = customer_service.get_customer_by_email(db, customer.email)
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this email already exists")
    return customer_service.create_customer(db, customer)


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    updated = customer_service.update_customer(db, customer_id, customer)
    if not updated:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted = customer_service.delete_customer(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")
