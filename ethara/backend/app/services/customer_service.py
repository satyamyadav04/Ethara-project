from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.models.customer import Customer
from app.models.order import Order
from app.schemas.customer import CustomerCreate, CustomerUpdate
from typing import Optional, List


def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> List[Customer]:
    query = db.query(Customer)
    if search:
        query = query.filter(
            or_(
                Customer.name.ilike(f"%{search}%"),
                Customer.email.ilike(f"%{search}%"),
                Customer.phone.ilike(f"%{search}%"),
            )
        )
    return query.offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, customer_id: int, customer: CustomerUpdate) -> Optional[Customer]:
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    update_data = customer.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int) -> bool:
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    db.delete(db_customer)
    db.commit()
    return True


def get_customer_order_count(db: Session, customer_id: int) -> int:
    return db.query(Order).filter(Order.customer_id == customer_id).count()


def count_customers(db: Session) -> int:
    return db.query(Customer).count()
