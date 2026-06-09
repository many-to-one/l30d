from fastapi import FastAPI
from routers.last30days import router as last30days_router

app = FastAPI(title="My Last30Days API")

app.include_router(last30days_router, prefix="/api")
