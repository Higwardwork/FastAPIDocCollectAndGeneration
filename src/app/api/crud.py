from app.api.models import TemplateSchema
from app.db import templates, database


async def post(payload: TemplateSchema):
    query = templates.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = templates.select().where(id == templates.c.id)
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
