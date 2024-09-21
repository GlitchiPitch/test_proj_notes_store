from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.database import create_database, delete_database, close_db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    yield
    await delete_database()
    await close_db_connection()

app = FastAPI(
    lifespan=lifespan,
)

if __name__ == '__main__':
    uvicorn.run(app)
