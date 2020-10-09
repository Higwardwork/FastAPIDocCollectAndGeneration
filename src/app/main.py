from fastapi import FastAPI, File
from fastapi.responses import FileResponse
from typing import Optional

from app.api import status, templates
from app.db import engine, metadata, database

import locale

locale.setlocale(locale.LC_ALL, "")

app = FastAPI(title="Генерация документов по шаблону.")

metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(status.router)
app.include_router(templates.router, prefix="/template", tags=["template"])
