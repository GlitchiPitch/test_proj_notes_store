from fastapi import APIRouter, Depends
from sqlalchemy import select

from core.auth import get_current_user
from core.config import settings
from core.database import session_getter
from core.models import User, Note
from core.schemas import NoteCreate, NoteRead
from core.speller import check_text

router = APIRouter(prefix=settings.notes.prefix)

@router.get(settings.notes.get_all)
async def get_all_notes(
        session = Depends(session_getter),
        current_user: User = Depends(get_current_user),
) -> list[NoteRead]:
    statement = select(Note).where(Note.owner_id == current_user.id)
    result = await session.execute(statement)
    notes = result.scalars().all()
    notes = [NoteRead(
        title=note.title,
        description=note.description,
    ) for note in notes]
    return notes

@router.post(settings.notes.create)
async def create_note(
        note_data: NoteCreate,
        session = Depends(session_getter),
        current_user: User = Depends(get_current_user),
) -> NoteRead:
    note = Note(
        title=check_text(note_data.title),
        description=check_text(note_data.description),
        owner_id=current_user.id,
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return NoteRead(
        title=note.title,
        description=note.description,
    )
