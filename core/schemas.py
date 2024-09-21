from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str

class User(UserCreate):
    id: int

    class ConfigDict:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str
    description: str | None

class NoteRead(NoteCreate):
    ...

class Note(NoteCreate):
    id: int
    owner_id: int

    class ConfigDict:
        from_attributes = True
