from tavily import TavilyClient
from app.config import settings

client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def web_search(query: str):
    print(f"[TOOL:web_search] Searching for: {query}")

    response = client.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = []

    for r in response.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content")
        })

    return results
