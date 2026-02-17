from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import AsyncSessionLocal
from app.db.models import User
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.auth.hashing import hash_password, verify_password
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(
        {"user_id": str(new_user.id)}
    )

    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(User).where(User.email == user.email)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"user_id": str(existing_user.id)}
    )

    return {"access_token": token}
