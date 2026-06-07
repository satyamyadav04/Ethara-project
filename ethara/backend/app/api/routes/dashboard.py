from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import product_service, customer_service, order_service

router = APIRouter()


@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    revenue = order_service.get_revenue_stats(db)
    total_products = product_service.count_products(db)
    low_stock = product_service.count_low_stock(db)
    total_customers = customer_service.count_customers(db)
    total_orders = order_service.count_orders(db)

    recent_orders = order_service.get_recent_orders(db, limit=5)
    recent = []
    for o in recent_orders:
        recent.append({
            "id": o.id,
            "order_number": o.order_number,
            "customer_name": o.customer.name if o.customer else "",
            "status": o.status.value,
            "total_amount": o.total_amount,
            "created_at": o.created_at.isoformat() if o.created_at else None,
        })

    return {
        "total_products": total_products,
        "low_stock_products": low_stock,
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_revenue": revenue["total_revenue"],
        "monthly_revenue": revenue["monthly_revenue"],
        "last_month_revenue": revenue["last_month_revenue"],
        "recent_orders": recent,
    }
