from fastapi import APIRouter, Depends, Query
from collectors.reddit import fetch_reddit
from collectors.hn import fetch_hn
from collectors.gh import fetch_github
from collectors.so import fetch_stackoverflow
from collectors.yt import fetch_youtube
from core.normalize import normalize
from core.rank import rank
from core.summarize import summarize_with_ai

import redis
import json

from db import get_session
from models import Job
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio
from fastapi import Query

router = APIRouter()

# Redis (synchronous client OK for queue)
r = redis.Redis.from_url("redis://redis:6379")


@router.post("/job")
async def create_job(session: AsyncSession = Depends(get_session)):
    job = Job(status="pending")
    session.add(job)
    await session.commit()
    await session.refresh(job)

    # Push job to queue
    r.rpush("jobs_queue", json.dumps({"id": job.id}))

    return {"job_id": job.id, "status": "queued"}




@router.get("/last30days")
async def last30days(query: str = Query(...)):

    reddit, hn, github, stack, youtube = await asyncio.gather(
        with_timeout(fetch_reddit(query), timeout=3),
        with_timeout(fetch_hn(query), timeout=3),
        with_timeout(fetch_github(), timeout=3),
        with_timeout(fetch_stackoverflow(), timeout=3),
        with_timeout(fetch_youtube(), timeout=3),
    )

    # łączenie wyników
    sources = reddit + hn + github + stack + youtube

    normalized = normalize(sources)
    ranked = rank(normalized)
    top = ranked[:20]

    summary = await summarize_with_ai(top)

    return {
        "query": query,
        "results": top,
        "summary": summary
    }



async def with_timeout(coro, timeout=3):
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except Exception as e:
        print(f"⚠️ Timeout or error: {e}")
        return []  # fallback
    


# @router.get("/last30days")
# async def last30days(query: str = Query(...)):
#     data = []
#     data += await fetch_reddit(query)
#     data += await fetch_hn(query)
#     data += await fetch_github(query)
#     data += await fetch_stackoverflow(query)
#     data += await fetch_youtube(query)

#     normalized = normalize(data)
#     ranked = rank(normalized)
#     top = ranked[:20]

#     summary = await summarize_with_ai(top)

#     return {
#         "query": query,
#         "results": top,
#         "summary": summary
#     }
