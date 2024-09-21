from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.database import create_database, delete_database, close_db_connection
from core.notes_router import router as notes_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database()
    yield
    await delete_database()
    await close_db_connection()

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(notes_router)

if __name__ == '__main__':
    uvicorn.run(app)
