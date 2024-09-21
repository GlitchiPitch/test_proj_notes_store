from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from .config import settings
from .database import session_getter
from .models import User
from .schemas import UserCreate
from passlib.context import CryptContext

router = APIRouter(prefix=settings.user.prefix)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password):
    return pwd_context.hash(password)

@router.post(settings.user.register, response_model=User)
async def register_user(
    user_data: UserCreate,
    session=Depends(session_getter),
):
    statement = select(User).where(User.username == user_data.username)
    result = await session.execute(statement)
    user = result.scalars().first()

    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = await get_password_hash(user_data.password)
    new_user = User(username=user_data.username, password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
