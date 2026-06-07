from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import Optional, List


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    category: Optional[str] = None,
    low_stock_only: bool = False,
) -> List[Product]:
    query = db.query(Product)

    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.sku.ilike(f"%{search}%"),
            )
        )
    if category:
        query = query.filter(Product.category == category)
    if low_stock_only:
        query = query.filter(Product.stock_quantity <= Product.low_stock_threshold)

    return query.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
    return db.query(Product).filter(Product.sku == sku).first()


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    update_data = product.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True


def get_categories(db: Session) -> List[str]:
    rows = db.query(Product.category).filter(Product.category.isnot(None)).distinct().all()
    return [r[0] for r in rows]


def count_products(db: Session) -> int:
    return db.query(Product).count()


def count_low_stock(db: Session) -> int:
    return db.query(Product).filter(Product.stock_quantity <= Product.low_stock_threshold).count()
