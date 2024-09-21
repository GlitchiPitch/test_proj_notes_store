from fastapi.security import HTTPBasicCredentials, HTTPBasic
from sqlalchemy import select
from starlette import status
from fastapi import Depends, HTTPException
from passlib.context import CryptContext

from core.database import session_getter
from core.models import User

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security),
        session=Depends(session_getter),
) -> User:
    statement = select(User).where(User.username == credentials.username)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user or not await verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user
