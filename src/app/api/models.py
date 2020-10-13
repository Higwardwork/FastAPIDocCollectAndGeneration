from pydantic import BaseModel
from enum import Enum


class FileExtension(str, Enum):
    xlsx = '.xlsx'
    docx = '.docx'


class TemplateSchema(BaseModel):
    title: str
    description: str


class TemplateDB(TemplateSchema):
    id: int


class FileSchema(BaseModel):
    t_id: int
    name: str
    extension: FileExtension
    description: str
    path: str


class FileDB(FileSchema):
    id: int
