from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="payment_microservice")


# This should be a different database
redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=str(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


class Order(HashModel, index=True):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)


@app.post("/orders")
async def create(
    request: Request, id: str, quantity: int, background_tasks: BackgroundTasks
):  # id, quantity
    req = requests.get(f"http://localhost:8000/products/{id}")

    if req.status_code != 200:
        return {"error": "Product not found"}

    product = req.json()

    order = Order(
        product_id=id,
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=quantity,
        status="pending",
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
    redis.xadd("order_completed", order.model_dump(), "*")
