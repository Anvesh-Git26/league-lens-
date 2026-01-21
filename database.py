import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    """Establishes an async connection to the PostgreSQL database."""
    conn = await asyncpg.connect(DATABASE_URL)
    return conn

async def query_structured_data(query: str):
    """
    Executes a read-only SQL query.
    Used by the RAG pipeline to fetch stats like 'Runs by Kohli in 2016'.
    """
    conn = await get_db_connection()
    try:
        # logic to sanitize/execute query
        # For prototype simplicity, we assume the LLM generates valid SQL
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]
    except Exception as e:
        return f"Database Error: {e}"
    finally:
        await conn.close()