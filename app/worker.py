import time
import redis
import json
from app.db import get_session
from app.models import Job

r = redis.Redis.from_url("redis://redis:6379")

print("Worker started...")

while True:
    _, raw = r.blpop("jobs_queue")  # blokuje aż pojawi się zadanie
    job = json.loads(raw)

    print(f"Processing job: {job}")

    # przykładowa logika
    session = get_session()
    db_job = session.query(Job).filter(Job.id == job["id"]).first()
    db_job.status = "done"
    session.commit()

    print(f"Job {job['id']} completed")
