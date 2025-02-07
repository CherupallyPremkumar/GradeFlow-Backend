from sqlalchemy import Table, Column, Integer, String
from app.db.database import metadata

clients = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("name", String),
    Column("email", String),
    Column("location", String),
)