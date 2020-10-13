import os
from databases import Database
from sqlalchemy import (create_engine, MetaData, Column, Table, DateTime, Integer, String, ForeignKey)
from sqlalchemy import (func)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
templates = Table(
    "templates",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(250)),
    Column("creation_data", DateTime, default=func.now(), nullable=False)
)

files = Table(
    "files",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("extension", String(10)),
    Column("description", String(250)),
    Column("t_id", Integer, ForeignKey("templates.id")),
    Column("path", String(250)),
    Column("load_data", DateTime, default=func.now(), nullable=False)
)

database = Database(DATABASE_URL)
