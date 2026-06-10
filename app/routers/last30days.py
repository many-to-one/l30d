from fastapi import APIRouter, Depends, Query
from collectors.reddit import fetch_reddit
from collectors.hn import fetch_hn
from core.normalize import normalize
from core.rank import rank
from core.summarize import summarize_with_ai

import redis
import json

from db import get_session
from models import Job
from sqlalchemy.ext.asyncio import AsyncSession

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
    data = []
    data += await fetch_reddit(query)
    data += await fetch_hn(query)

    normalized = normalize(data)
    ranked = rank(normalized)
    top = ranked[:20]

    summary = await summarize_with_ai(top)

    return {
        "query": query,
        "results": top,
        "summary": summary
    }
