from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

class NotesConfig(BaseModel):
    prefix: str = '/notes'
    create: str = '/create'
    get_all: str = '/get_all'

class UserConfig(BaseModel):
    prefix: str = '/user'
    create: str = '/create'

class DatabaseConfig(BaseModel):
    url: PostgresDsn = "postgresql+asyncpg://user:pass@0.0.0.0:5432/notes"
    test_url: PostgresDsn = "postgresql+asyncpg://user:pass@0.0.0.0:7070/test_notes"

class Settings(BaseSettings):
    notes: NotesConfig = NotesConfig()
    user: UserConfig = UserConfig()
    db: DatabaseConfig = DatabaseConfig()

settings = Settings()