from fastapi import APIRouter, HTTPException
from app.api import crud
from app.api.models import TemplateSchema, TemplateDB
from typing import List, Optional

router = APIRouter()


@router.post("/", response_model=TemplateDB, status_code=201, description="Создание нового шаблона")
async def create_template(payload: TemplateSchema):
    note_id = await crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }

    return response_object


@router.get("/{id}/", response_model=TemplateDB)
async def read_template(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Template not found")
    return note


@router.get("/", response_model=List[TemplateDB])
async def read_all_templates():
    return await crud.get_all()


@router.put("/{id}/", response_model=TemplateDB)
async def update_note(id: int, payload: TemplateSchema):
    template = await crud.get(id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    template_id = await crud.put(id, payload)

    response_object = {
        "id": template_id,
        "title": payload.title,
        "description": payload.description,
    }

    return response_object


@router.delete("/{id}/", response_model=TemplateDB)
async def delete_template(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Template not found")
    await crud.delete(id)

    return note
