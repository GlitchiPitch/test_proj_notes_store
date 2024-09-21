from fastapi import APIRouter, Depends
from sqlalchemy import select
from core.auth import get_current_user
from core.database import session_getter
from core.models import User, Note
from core.schemas import NoteCreate
from typing import List

from core.speller import check_text

router = APIRouter(prefix='/notes')

@router.get('/get_all', response_model=List[Note])
async def get_all_notes(
        session = Depends(session_getter),
        current_user: User = Depends(get_current_user),
):
    statement = select(Note).where(Note.owner_id == current_user.id)
    result = await session.execute(statement)
    notes = result.scalars().all()
    return notes

@router.post('/create', response_model=Note)
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
