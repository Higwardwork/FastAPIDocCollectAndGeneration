from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from app.api import crud
from app.api.models import FileDB, FileExtension
from fastapi.responses import FileResponse
import json
import shutil
from os import path, mkdir
from types import SimpleNamespace

router = APIRouter()

templates_file_path = "C:\\FastAPI\\Template_Data"

@router.post("/", response_model=FileDB, status_code=201, description="Добавление файла шаблона")
async def create_template_file(payload: str = Form(..., example={
    "t_id": 1,
    "name": "string",
    "extension": ".xlsx",
    "description": "string",
    "path": "string"
}), data: UploadFile = File(...)):
    payload_as_object = json.loads(payload, object_hook=lambda d: SimpleNamespace(**d))

    template = await crud.get(payload_as_object.t_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    file = await crud.post_file(payload_as_object)

    template_file_path = path.join(templates_file_path, str(payload_as_object.t_id))

    if not path.exists(template_file_path):
        mkdir(template_file_path)

    file_object = data.file
    upload_folder = open(path.join(template_file_path, data.filename), 'wb+')
    shutil.copyfileobj(file_object, upload_folder)
    upload_folder.close()

    response_object = {
        "id": file,
        "name": data.filename,
        "extension": path.splitext(data.filename)[1],
        "description": payload_as_object.description,
        "path": template_file_path,
        "t_id": payload_as_object.t_id
    }
    return response_object


@router.get("/{id}/", response_model=FileDB, description="Получить файл, который используется для построения")
async def read_template_file(id: int, file_type: FileExtension):
    template_file_path = path.join(templates_file_path, str(id))
    template = await crud.get(id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if not path.exists(template_file_path):
        raise HTTPException(status_code=404, detail="Файлы для шаблона не загруженны")

    file = await crud.get_file_by_template(id, file_type)
    if not file:
        raise HTTPException(status_code=404, detail="Файл для такого шаблона не существует")

    template_file_path = path.join(template_file_path, file.name)
    print(template_file_path)

    return FileResponse(template_file_path)
