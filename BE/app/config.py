import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Settings:
    # ===============================
    # LLM CONFIG
    # ===============================
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # ===============================
    # APP CONFIG
    # ===============================
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "false").lower() == "true"

    # ===============================
    # DATABASE CONFIG
    # ===============================
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME")

    # ===============================
    # AUTH0 CONFIG (NEW)
    # ===============================
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN")
    AUTH0_AUDIENCE: str = os.getenv("AUTH0_AUDIENCE")
    AUTH0_ISSUER: str = os.getenv("AUTH0_ISSUER")

    @property
    def DATABASE_URL(self) -> str:
        encoded_password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{encoded_password}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def AUTH0_JWKS_URL(self) -> str:
        """
        URL used to fetch public signing keys for verifying RS256 tokens.
        """
        return f"https://{self.AUTH0_DOMAIN}/.well-known/jwks.json"


settings = Settings()