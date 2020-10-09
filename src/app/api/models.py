from pydantic import BaseModel


class TemplateSchema(BaseModel):
    title: str
    description: str


class TemplateDB(TemplateSchema):
    id: int
