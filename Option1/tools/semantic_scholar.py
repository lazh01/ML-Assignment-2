import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_papers(query: str, limit: int = 10):
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,citationCount,url,abstract"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return []

    data = response.json()
    return data.get("data", [])