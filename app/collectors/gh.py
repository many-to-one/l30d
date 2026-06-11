import httpx

async def fetch_github():
    url = "https://ghapi.huchen.dev/repositories"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

    if r.status_code != 200:
        return []

    data = r.json()
    posts = []

    for repo in data:
        posts.append({
            "source": "github",
            "title": repo["name"],
            "url": repo["url"],
            "score": repo["stars"],
            "comments": repo["forks"],
            "created": repo["currentPeriodStars"],
        })

    return posts
