from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    title: str
    description: str | None = None
    price: float


class ProductUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class ProductOutSchema(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    owner_id: int

    class Config:
        from_attributes = True