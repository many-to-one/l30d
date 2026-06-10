import httpx

async def fetch_reddit(query: str):
    url = f"https://www.reddit.com/search.json?q={query}&sort=top&t=month"
    # headers = {"User-Agent": "Mozilla/5.0"}
    headers = {"User-Agent": "Last30DaysApp/1.0 by u/alex"}


    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)

        if r.status_code != 200:
            print(f"❌ Reddit API error: {r.status_code} - {r.text}")
            return []

        try:
            data = r.json()
        except Exception as e:
            print(f"❌ JSON decode error: {e}")
            return []

    posts = []
    for item in data.get("data", {}).get("children", []):
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
