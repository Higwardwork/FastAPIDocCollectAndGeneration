from fastapi import APIRouter, HTTPException
from app.api import crud
from app.api.models import TemplateSchema, TemplateDB
from typing import List

router = APIRouter()


@router.post("/", response_model=TemplateDB, status_code=201, description="Создание нового шаблона")
async def create_template(payload: TemplateSchema):
    template_id = await crud.post(payload)

    response_object = {
        "id": template_id,
        "title": payload.title,
        "description": payload.description,
    }

    return response_object


@router.get("/{id}/", response_model=TemplateDB)
async def read_template(id: int):
    template = await crud.get(id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.get("/{title}/", response_model=TemplateDB)
async def find_template(title: str):
    template = await crud.get_by_title(title)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.get("/", response_model=List[TemplateDB])
async def read_all_templates():
    return await crud.get_all()


@router.put("/{id}/", response_model=TemplateDB)
async def update_template(id: int, payload: TemplateSchema):
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
    template = await crud.get(id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    await crud.delete(id)

    return template
