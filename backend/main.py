import os
import random
from fastapi import Depends, FastAPI, HTTPException
from . import schemas

if os.environ.get("DISABLE_SWAGGER") == "true":
    docs_url = None
    redoc_url = None
else:
    docs_url = "/docs"
    redoc_url = "/redoc"

app = FastAPI(
    docs_url=docs_url,
    redoc_url=redoc_url
)

@app.get("/actualize")
def actualize():
    return {"status": random.random() < 0.5}

@app.get("/search")
def search(object_name: str, limit: int):
    return [
        schemas.Material(**{
            "code": "00.00.00.000.00.0.00.00-0000-0000",
            "object_name": "Звуковая отвёртка!",
            "unit_of_measurement": "кг",
            "score": 1.0,
        })
    ] * limit

@app.post("/test/")
def post_test():
    return True

@app.get("/test/")
def get_test():
    return True
