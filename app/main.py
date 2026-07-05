from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.auth import router as auth_router
from app.core.config import settings
from app.api.projects import router as project_router
from app.api.queues import router as queue_router
from app.api.jobs import router as job_router
from app.api.workers import router as worker_router
from app.api.scheduler import router as scheduler_router
from app.api.retry import router as retry_router
from app.api.dashboard import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.dlq import router as dlq_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-inspired Distributed Job Scheduler",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(queue_router)
app.include_router(job_router)
app.include_router(worker_router)
app.include_router(scheduler_router)
app.include_router(retry_router)
app.include_router(dashboard_router)
app.include_router(dlq_router)
@app.get("/", tags=["Root"])
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
async def health():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "application": settings.APP_NAME,
            "version": settings.APP_VERSION,
        },
    )