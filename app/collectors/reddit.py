import httpx

async def fetch_reddit(query: str):
    url = f"https://www.reddit.com/search.json?q={query}&sort=top&t=month"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        data = r.json()

    posts = []
    for item in data["data"]["children"]:
        d = item["data"]
        posts.append({
            "source": "reddit",
            "title": d["title"],
            "url": "https://reddit.com" + d["permalink"],
            "score": d["score"],
            "comments": d["num_comments"],
            "created": d["created_utc"],
        })
    return posts
