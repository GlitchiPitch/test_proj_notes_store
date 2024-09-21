from fastapi import APIRouter, Depends
from sqlalchemy import select
from .auth import get_current_user
from .config import settings
from .database import session_getter
from .models import User, Note
from .schemas import NoteCreate
from typing import List

from core.speller import check_text

router = APIRouter(prefix=settings.notes.prefix)

@router.get(settings.notes.get_all, response_model=List[Note])
async def get_all_notes(
        session = Depends(session_getter),
        current_user: User = Depends(get_current_user),
):
    statement = select(Note).where(Note.owner_id == current_user.id)
    result = await session.execute(statement)
    notes = result.scalars().all()
    return notes

@router.post(settings.notes.create, response_model=Note)
async def create_note(
        note_data: NoteCreate,
        session = Depends(session_getter),
        current_user: User = Depends(get_current_user),
):
    note = Note(
        title=check_text(note_data.title),
        description=check_text(note_data.description),
        owner_id=current_user.id,
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note
