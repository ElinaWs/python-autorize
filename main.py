from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.database import Base, engine
from src.products.router import product_router
from src.auth.router import user_router, auth
from src.products.router import router as products_router
app.include_router(products_router)

# from src.models.user import User
# from src.models.product import Product
# from src.models.order import Order
# from src.models.comment import Comment

# User.metadata.create_all(bind=engine)
# Product.metadata.create_all(bind=engine)
# Order.metadata.create_all(bind=engine)
# Comment.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

auth.handle_errors(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    product_router,
    prefix="/api/v1",
)

app.include_router(
    user_router,
    prefix="/api/v1",
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", log_level="info")