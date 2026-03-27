

## Commands to run this mini project

### Description
- This is the mini microservices project which is built in fastAPI.
- It has 2 modules inventory and payment 
- Both have different redis databases 
- they are communicating via APIs and redis stream Events 


### To run the Inventory Microservice
```
uv run uvicorn microservices_fastapi.inventory_microservice.main:app
```
### To run the Payment Microservice
```
uv run uvicorn microservices_fastapi.payment_microservice.main:app  --port 8001
```
### To run the inventory consumer
```
uv run python -m  microservices_fastapi.inventory_microservice.consumer
```

### Environ Variables needed
```
REDIS_HOST=
REDIS_PORT=
REDIS_USERNAME=
REDIS_PASSWORD=