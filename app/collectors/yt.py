import httpx

async def fetch_youtube():
    url = "https://yt-api.org/trending?geo=US"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)

        if r.status_code != 200:
            print(f"❌ YouTube API error: {r.status_code} - {r.text}")
            return []

        try:
            data = r.json()
        except Exception as e:
            print(f"❌ JSON decode error (YouTube): {e}")
            return []

    posts = []
    for item in data.get("data", []):
        posts.append({
            "source": "youtube",
            "title": item.get("title"),
            "url": f"https://www.youtube.com/watch?v={item.get('videoId')}",
            "score": item.get("viewCount", 0),
            "comments": item.get("commentCount", 0),
            "created": item.get("publishedTimeText"),
            "thumbnail": item.get("thumbnail", {}).get("url"),
            "channel": item.get("channelTitle"),
        })

    return posts
