from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from authx import TokenPayload

from src.database import get_db
from src.models.product import Product
from src.models.user import User
from src.auth.router import auth
from src.products.schemas import ProductCreateSchema, ProductUpdateSchema, ProductOutSchema
from fastapi.security import HTTPBearer

security = HTTPBearer()

product_router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@product_router.get("/", response_model=list[ProductOutSchema])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@product_router.get("/my_products", response_model=list[ProductOutSchema])
def get_my_products(
    payload: TokenPayload = Depends(auth.access_token_required),
    db: Session = Depends(get_db)
):
    return db.query(Product).filter(
        Product.owner_id == int(payload.sub)
    ).all()


@product_router.get("/{product_id}", response_model=ProductOutSchema)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Продукт не найден"
        )

    return product


@product_router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreateSchema,
    payload: TokenPayload = Depends(auth.access_token_required),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == int(payload.sub)).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    new_product = Product(
        title=product_data.title,
        description=product_data.description,
        price=product_data.price,
        owner_id=user.id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Продукт создан",
        "product": new_product
    }


@product_router.put("/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdateSchema,
    payload: TokenPayload = Depends(auth.access_token_required),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Продукт не найден"
        )

    if product.owner_id != int(payload.sub):
        raise HTTPException(
            status_code=403,
            detail="Можно изменять только свои продукты"
        )

    if product_data.title is not None:
        product.title = product_data.title

    if product_data.description is not None:
        product.description = product_data.description

    if product_data.price is not None:
        product.price = product_data.price

    db.commit()
    db.refresh(product)

    return {
        "message": "Продукт обновлен",
        "product": product
    }


@product_router.delete("/{product_id}")
def delete_product(
    product_id: int,
    payload: TokenPayload = Depends(auth.access_token_required),
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Продукт не найден"
        )

    if product.owner_id != int(payload.sub):
        raise HTTPException(
            status_code=403,
            detail="Можно удалять только свои продукты"
        )

    db.delete(product)
    db.commit()

    return {"message": "Продукт удален"}