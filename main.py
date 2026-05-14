from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.database import Base, engine

from src.models.user import User
from src.models.product import Product

from src.auth.router import user_router, auth
from src.products.router import product_router


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

app.include_router(user_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "API works"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)