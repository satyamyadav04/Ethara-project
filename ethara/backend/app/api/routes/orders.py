from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderOut, OrderItemOut
from app.services import order_service
from app.models.order import OrderStatus
from typing import List, Optional

router = APIRouter()


def enrich_order(order) -> OrderOut:
    """Enrich order ORM object with computed fields."""
    order_out = OrderOut.model_validate(order)
    order_out.customer_name = order.customer.name if order.customer else ""
    order_out.items = []
    for item in order.items:
        item_out = OrderItemOut.model_validate(item)
        item_out.product_name = item.product.name if item.product else ""
        item_out.product_sku = item.product.sku if item.product else ""
        order_out.items.append(item_out)
    return order_out


@router.get("/", response_model=List[OrderOut])
def list_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=500),
    status: Optional[OrderStatus] = None,
    customer_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    orders = order_service.get_orders(db, skip, limit, status, customer_id, search)
    return [enrich_order(o) for o in orders]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return enrich_order(order)


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    try:
        created = order_service.create_order(db, order)
        return enrich_order(created)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    updated = order_service.update_order(db, order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return enrich_order(updated)


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    deleted = order_service.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
