def rank(posts):
    def score(p):
        return (
            p.get("score", 0) * 2 +
            p.get("comments", 0) * 1.5
        )
    return sorted(posts, key=score, reverse=True)
