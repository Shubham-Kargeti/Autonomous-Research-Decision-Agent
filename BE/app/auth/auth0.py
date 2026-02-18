from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import HTTPException, status
from app.config import settings

ALGORITHMS = ["RS256"]

def get_jwks():
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    response = requests.get(jwks_url)
    return response.json()


def verify_auth0_token(token: str):
    try:
        jwks = get_jwks()

        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header",
            )

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=settings.AUTH0_AUDIENCE,
            issuer=settings.AUTH0_ISSUER,
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
