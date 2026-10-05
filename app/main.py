from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine

from app.database.base import Base

from app.api.upload_routes import router as upload_router
from app.api.review_routes import router as review_router
from app.api.dashboard_routes import router as dashboard_router

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Intelligent Code Review Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(upload_router)
app.include_router(review_router)
app.include_router(dashboard_router)