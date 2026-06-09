def normalize(posts):
    normalized = []
    for p in posts:
        normalized.append({
            "source": p.get("source"),
            "title": p.get("title"),
            "url": p.get("url"),
            "score": p.get("score", 0),
            "comments": p.get("comments", 0),
            "created": p.get("created"),
        })
    return normalized
