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
    # SECURITY CONFIG
    # ===============================
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_HOURS: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 24)
    )

    @property
    def DATABASE_URL(self) -> str:
        encoded_password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{encoded_password}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
