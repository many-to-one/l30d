import httpx

async def fetch_stackoverflow():
    url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&site=stackoverflow"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

    if r.status_code != 200:
        return []

    data = r.json()
    posts = []

    for q in data["items"]:
        posts.append({
            "source": "stackoverflow",
            "title": q["title"],
            "url": q["link"],
            "score": q["score"],
            "comments": q["answer_count"],
            "created": q["creation_date"],
        })

    return posts
