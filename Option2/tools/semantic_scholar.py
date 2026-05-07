import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query: str, limit: int = 5):
    """
    Search Semantic Scholar papers.
    """

    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,url,abstract"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return {
            "error": f"Semantic Scholar API error: {response.status_code}"
        }

    data = response.json()

    papers = []

    for p in data.get("data", []):
        papers.append({
            "title": p.get("title"),
            "authors": [a["name"] for a in p.get("authors", [])],
            "year": p.get("year"),
            "citationCount": p.get("citationCount"),
            "url": p.get("url"),
            "abstract": p.get("abstract"),
        })

    return papers