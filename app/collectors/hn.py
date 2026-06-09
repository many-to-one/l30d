import httpx

async def fetch_hn(query: str):
    url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()

    posts = []
    for hit in data["hits"]:
        posts.append({
            "source": "hackernews",
            "title": hit["title"],
            "url": hit["url"],
            "score": hit["points"],
            "comments": hit["num_comments"],
            "created": hit["created_at"],
        })
    return posts
