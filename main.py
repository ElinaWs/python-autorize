from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.models.user import User
from src.models.product import Product
from src.auth.router import user_router, auth
from src.products.router import product_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authorization API",
    description="FastAPI project with users, roles, products and SQLite",
    version="1.0.0",
)

auth.handle_errors(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API works"}