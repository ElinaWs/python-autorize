from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.product import Product
from src.products.schemas import ProductSchema, ProductCreateUpdateSchema


product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

@product_router.get("/", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)) ->List[ProductSchema]:
    return db.query(Product).filter_by(is_available=True)

@product_router.get("/{id}", response_model=ProductSchema)
def get_product(id: int, db: Session = Depends(get_db)) -> ProductSchema:
    product = db.get(Product, id)
    if product and product.is_available:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@product_router.post("/")
def create_product(
    product: ProductCreateUpdateSchema,
    db: Session = Depends(get_db)
) -> ProductSchema:
    new_product = Product(**product.model_dump(exclude_unset=True))
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@product_router.put("/{id}", response_model=ProductSchema)
def update_product(
    id: int,
    product: ProductCreateUpdateSchema,
    db: Session = Depends(get_db)
) -> ProductSchema:
    db_product = db.get(Product, id)
    if db_product:
        product_data = product.model_dump(exclude_unset=True)
        for key, value in product_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@product_router.delete("/{id}")
def delete_product(id: int, db: Session = Depends(get_db)) -> dict:
    product = db.get(Product, id)
    if product:
        db.delete(product)
        db.commit()
        return {
            "message": "product has been deleted"
        }
    raise HTTPException(status_code=404, detail="Product not found")
