from app.api.models import TemplateSchema, FileSchema, FileExtension
from app.db import templates, database, files


# Template Schema
async def post(payload: TemplateSchema):
    query = templates.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = templates.select().where(id == templates.c.id)
    return await database.fetch_one(query=query)


async def get_by_title(title: str):
    query = templates.select().where(title == templates.c.title)
    return await database.fetch_one(query=query)


async def get_all():
    query = templates.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: TemplateSchema):
    query = (
        templates
            .update()
            .where(id == templates.c.id)
            .values(title=payload.title, description=payload.description)
            .returning(templates.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = templates.delete().where(id == templates.c.id)
    return await database.execute(query=query)


# Files
async def post_file(payload: FileSchema):
    query = files.insert().values(name=payload.name, description=payload.description, extension=payload.extension)
    return await database.execute(query=query)


async def get_file(id: int):
    query = files.select().where(id == files.c.id)
    return await database.fetch_one(query=query)


async def get_file_by_template(t_id: int, file_type: FileExtension):
    query = files.select().where(t_id == files.c.t_id).where(file_type == files.c.extension)
    return await database.fetch_one(query=query)
