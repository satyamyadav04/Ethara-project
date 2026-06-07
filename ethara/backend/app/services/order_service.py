from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate
from typing import Optional, List
import random
import string
from datetime import datetime, timedelta


def generate_order_number() -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{suffix}"


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[OrderStatus] = None,
    customer_id: Optional[int] = None,
    search: Optional[str] = None,
) -> List[Order]:
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    if search:
        query = query.filter(Order.order_number.ilike(f"%{search}%"))
    return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, order: OrderCreate) -> Order:
    total = 0.0
    items_data = []

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product {item.product_id} not found")
        if product.stock_quantity < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}. Available: {product.stock_quantity}")
        subtotal = item.unit_price * item.quantity
        total += subtotal
        items_data.append((item, product, subtotal))

    # Apply discount and tax
    total = total - order.discount + order.tax

    db_order = Order(
        order_number=generate_order_number(),
        customer_id=order.customer_id,
        total_amount=round(total, 2),
        discount=order.discount,
        tax=order.tax,
        notes=order.notes,
    )
    db.add(db_order)
    db.flush()  # Get order ID

    for item, product, subtotal in items_data:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            subtotal=subtotal,
        )
        db.add(db_item)
        # Deduct stock
        product.stock_quantity -= item.quantity

    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order: OrderUpdate) -> Optional[Order]:
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    update_data = order.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    # Restore stock
    for item in db_order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
    db.delete(db_order)
    db.commit()
    return True


def count_orders(db: Session) -> int:
    return db.query(Order).count()


def get_revenue_stats(db: Session):
    today = datetime.utcnow().date()
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)

    total_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status != OrderStatus.cancelled
    ).scalar() or 0.0

    monthly_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status != OrderStatus.cancelled,
        func.date(Order.created_at) >= this_month_start,
    ).scalar() or 0.0

    last_month_revenue = db.query(func.sum(Order.total_amount)).filter(
        Order.status != OrderStatus.cancelled,
        func.date(Order.created_at) >= last_month_start,
        func.date(Order.created_at) < this_month_start,
    ).scalar() or 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "monthly_revenue": round(monthly_revenue, 2),
        "last_month_revenue": round(last_month_revenue, 2),
    }


def get_recent_orders(db: Session, limit: int = 5) -> List[Order]:
    return db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
