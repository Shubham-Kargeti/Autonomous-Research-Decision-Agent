import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    APP_ENV = os.getenv("APP_ENV", "development")
    APP_DEBUG = os.getenv("APP_DEBUG", "false").lower() == "true"
    


settings = Settings()