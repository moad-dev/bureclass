import os
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

@app.post("/test/")
def post_test():
    return True

@app.get("/test/")
def get_test():
    return True
