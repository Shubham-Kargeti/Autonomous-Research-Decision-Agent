from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.config import settings

ALGORITHM = "HS256"


# -------- Create Token --------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
    hours=settings.ACCESS_TOKEN_EXPIRE_HOURS
)
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )


# -------- Verify Token --------
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
