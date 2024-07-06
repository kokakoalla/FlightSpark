import asyncpg
from .config import Config

async def get_database_connection():
    return await asyncpg.connect(Config.DATABASE_URL)