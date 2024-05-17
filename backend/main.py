from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import schemas

app = FastAPI()

@app.post("/test/")
def post_test():
    return True

@app.get("/test/")
def get_test():
    return True
