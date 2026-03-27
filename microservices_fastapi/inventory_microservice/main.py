import os
from fastapi import FastAPI
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel

load_dotenv()

# Redis Configurations
redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=str(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


class Product(HashModel, index=True):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


app = FastAPI(title="inventory_microservice")


def format(pk: str):
    product = Product.get(pk)
    return {
        "pk": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


@app.get("/products/{pk}")
def get_product(pk: str):
    return format(pk)


@app.post("/products")
def create(product: Product):
    return product.save()


@app.delete("/products/{pk}")
def delete(pk: str):
    try:
        Product.delete(pk)
        return {"message": f"Product: {pk} deleted successfully"}
    except KeyError:
        return {"error": "Product not found"}
