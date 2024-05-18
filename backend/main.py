import os
import random
from fastapi import Depends, FastAPI, HTTPException, UploadFile
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

@app.post("/actualize")
def actualize(file: UploadFile):
    """
    Актуализация базы наименований строительных ресурсов. Принимает excel (.xlsx) файл классификатора строительных ресурсов, доступный по адресу https://fgiscs.minstroyrf.ru/ksr
    """
    if file.content_type != "application/vnd.ms-excel" \
        and file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(400, detail="Invalid document type")
    try: 
        pass # TODO: read excel file
    except Exception:
        raise HTTPException(422, detail="Invalid document content")
    # TODO: update elasticsearch indexes
    return {"status": True}

@app.get("/search")
def search(object_name: str, limit: int):
    """
    Определение нескольких строительных ресурсов, наименование которых похоже на заданное.
    """
    return [
        schemas.Material(**{
            "code": "00.00.00.000.00.0.00.00-0000-0000",
            "object_name": "Звуковая отвёртка!",
            "score": 1.0,
        })
    ] * limit

@app.post("/test/")
def post_test():
    return True

@app.get("/test/")
def get_test():
    return True
