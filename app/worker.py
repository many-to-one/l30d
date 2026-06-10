import time
import redis
import json
from db import get_session
from models import Job

r = redis.Redis.from_url(
    "redis://redis:6379",
    socket_timeout=None,
    socket_connect_timeout=30,
    health_check_interval=30,
)

print("Worker started...")

while True:
    try:
        result = r.blpop("jobs_queue", timeout=30)

        if result is None:
            continue

        _, raw = result

        if isinstance(raw, bytes):
            raw = raw.decode()

        job = json.loads(raw)

        print(f"Processing job: {job}")

        session = get_session()

        try:
            db_job = (
                session.query(Job)
                .filter(Job.id == job["id"])
                .first()
            )

            if db_job:
                db_job.status = "done"
                session.commit()

            print(f"Job {job['id']} completed")

        finally:
            session.close()

    except redis.exceptions.TimeoutError:
        print("Redis timeout...")
        continue

    except redis.exceptions.ConnectionError:
        print("Redis connection lost, reconnecting...")
        time.sleep(5)

        r = redis.Redis.from_url(
            "redis://redis:6379",
            socket_timeout=None,
            socket_connect_timeout=30,
            health_check_interval=30,
        )

    except Exception as e:
        print("Worker error:", e)
        time.sleep(5)