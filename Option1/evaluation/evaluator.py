def evaluate(result):
    checks = {
        "has_title": "title" in result.lower(),
        "has_year": "year" in result.lower(),
        "has_citations": "citation" in result.lower(),
        "has_link": "http" in result.lower(),
    }
    return checks