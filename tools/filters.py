def filter_papers(papers, min_year=None, max_year=None, min_citations=None, max_citations=None):
    results = []

    for p in papers:
        year = p.get("year", 0)
        citations = p.get("citationCount", 0)

        if min_year is not None and year < min_year:
            continue
        if max_year is not None and year > max_year:
            continue
        if min_citations is not None and citations < min_citations:
            continue
        if max_citations is not None and citations > max_citations:
            continue

        results.append(p)

    return results