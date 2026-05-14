from pydantic import BaseModel


class Shade(BaseModel):
    name: str
    hexColor: str
    skinTone: str


class Product(BaseModel):
    id: int
    brand: str
    name: str
    category: str
    price: int
    description: str
    shades: list[Shade]