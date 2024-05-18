from asyncio.subprocess import Process
import os
import hashlib
import asyncio
import pathlib
from fastapi import (
    FastAPI, HTTPException, UploadFile, status, Form
)
from fastapi.responses import (
    JSONResponse
)
from typing import Annotated

from . import schemas


async def run_subprocess(cmd, callback):
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    await callback(process, stdout, stderr)


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

actualization_lock = asyncio.Lock()
last_job_successful: bool|None = None


@app.get("/actualize")
def actualize_status():
    if actualization_lock.locked():
        status = 'running'
    elif last_job_successful:
        status = 'completed'
    else:
        status = 'failed'
    return {"status": status}


@app.post("/actualize")
async def actualize(password: Annotated[str, Form()], file: UploadFile):
    """
    Актуализация базы наименований строительных ресурсов. Принимает excel (.xlsx) файл классификатора строительных ресурсов, доступный по адресу https://fgiscs.minstroyrf.ru/ksr
    """
    async def on_job_complete(process: Process, _, stderr):
        global last_job_successful
        print(stderr.decode())
        last_job_successful = process.returncode == 0
    
    if file.content_type != "application/vnd.ms-excel" \
        and file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(400, detail="Invalid document type")

    if password != os.getenv("ADMIN_PASSWORD"):
        raise HTTPException(403, detail="Invalid credentials")

    pathlib.Path("data").mkdir(parents=True, exist_ok=True)
    with open("data/ksr.xlsx", "wb") as local_file:
        local_file.write(file.file.read())
    
    if actualization_lock.locked():
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED, 
            detail="A job is already in progress. Please wait until the current job is completed."
        )

    async with actualization_lock:
        asyncio.create_task(run_subprocess(
            ['python', 'backend/actualize_job.py'],
            on_job_complete
        ))

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED, 
        content={'message': "Accepted", 'status_url': '/actualize'}
    );

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
