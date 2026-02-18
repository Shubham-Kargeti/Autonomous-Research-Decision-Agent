from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import AsyncSessionLocal
from app.db.models import User
from app.auth.auth0 import verify_auth0_token  # NEW
import uuid

security = HTTPBearer()


# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ==========================================================
# GET CURRENT USER (Auth0 Based)
# ==========================================================
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials

    # Verify Auth0 JWT
    payload = verify_auth0_token(token)

    auth0_sub = payload.get("sub")
    email = payload.get("email")
    name = payload.get("name")

    if not auth0_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    # Check if user exists in DB
    result = await db.execute(
        select(User).where(User.auth0_sub == auth0_sub)
    )
    user = result.scalar_one_or_none()

    # If user doesn't exist → create automatically
    if not user:
        user = User(
            id=uuid.uuid4(),
            auth0_sub=auth0_sub,
            email=email,
            name=name,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user
