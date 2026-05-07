import time
import requests
from typing import Dict, Any, List

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query: str, limit: int = 5) -> Dict[str, Any]:
    time.sleep(1.5)  # rate limit protection

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,url,abstract"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 429:
        return {
            "status": "rate_limit",
            "papers": []
        }

    if response.status_code != 200:
        return {
            "status": "error",
            "message": str(response.status_code),
            "papers": []
        }

    data = response.json()

    papers = [
        {
            "title": p.get("title"),
            "authors": [a["name"] for a in p.get("authors", [])],
            "year": p.get("year"),
            "citationCount": p.get("citationCount"),
            "url": p.get("url"),
            "abstract": p.get("abstract"),
        }
        for p in data.get("data", [])
    ]
    print(papers)
    return {
        "status": "ok",
        "papers": papers
    }