import requests

BASE_URL = "https://api.openalex.org/works"

def search_papers(
    query: str,
    limit: int = 10,
    min_year: int | None = None,
    max_year: int | None = None,
    min_citations: int | None = None,
    max_citations: int | None = None,
):
    params = {
        "search": query,
        "per-page": limit,
        "select": "title,authorships,publication_year,cited_by_count,doi,abstract_inverted_index"
    }

    filters = []
    if min_year is not None:
        filters.append(f"publication_year:>{min_year - 1}")
    if max_year is not None:
        filters.append(f"publication_year:<{max_year + 1}")
    if min_citations is not None:
        filters.append(f"cited_by_count:>{min_citations - 1}")
    if max_citations is not None:
        filters.append(f"cited_by_count:<{max_citations + 1}")

    if filters:
        params["filter"] = ",".join(filters)

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"OpenAlex API error: {response.status_code}")
    data = response.json()
    results = []
    for work in data.get("results", []):
        # OpenAlex stores abstracts as inverted index — reconstruct it
        abstract = ""
        inv = work.get("abstract_inverted_index") or {}
        if inv:
            words = [""] * (max(max(v) for v in inv.values()) + 1)
            for word, positions in inv.items():
                for pos in positions:
                    words[pos] = word
            abstract = " ".join(words)
        results.append({
            "title": work.get("title"),
            "authors": [a["author"]["display_name"] for a in work.get("authorships", [])],
            "year": work.get("publication_year"),
            "citationCount": work.get("cited_by_count"),
            "url": f"https://doi.org/{work['doi']}" if work.get("doi") else None,
            "abstract": abstract
        })
    return results