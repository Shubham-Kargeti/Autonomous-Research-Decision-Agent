from langchain_groq import ChatGroq
from app.config import settings

def get_llm():
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model=settings.GROQ_MODEL,
        temperature=0.3,
    )

def call_llm(system_prompt: str, user_prompt: str) -> str:
    llm = get_llm()

    response = llm.invoke([
        ("system", system_prompt),
        ("human", user_prompt),
    ])

    return response.content
