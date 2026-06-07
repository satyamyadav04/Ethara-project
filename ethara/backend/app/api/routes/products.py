from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.services import product_service
from typing import List, Optional

router = APIRouter()


@router.get("/", response_model=List[ProductOut])
def list_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, le=500),
    search: Optional[str] = None,
    category: Optional[str] = None,
    low_stock_only: bool = False,
    db: Session = Depends(get_db),
):
    return product_service.get_products(db, skip, limit, search, category, low_stock_only)


@router.get("/categories", response_model=List[str])
def list_categories(db: Session = Depends(get_db)):
    return product_service.get_categories(db)


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    existing = product_service.get_product_by_sku(db, product.sku)
    if existing:
        raise HTTPException(status_code=400, detail="Product with this SKU already exists")
    return product_service.create_product(db, product)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    updated = product_service.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = product_service.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
