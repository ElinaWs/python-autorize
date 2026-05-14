from fastapi import APIRouter

from src.products.models import products

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products():
    return products


@router.get("/recommend/{skin_tone}")
def recommend_products(skin_tone: str):

    recommended = []

    for product in products:

        matched_shades = []

        for shade in product["shades"]:

            if shade["skinTone"] == skin_tone:
                matched_shades.append(shade)

        if matched_shades:
            recommended.append({
                "id": product["id"],
                "brand": product["brand"],
                "name": product["name"],
                "category": product["category"],
                "price": product["price"],
                "description": product["description"],
                "shades": matched_shades
            })

    return recommended