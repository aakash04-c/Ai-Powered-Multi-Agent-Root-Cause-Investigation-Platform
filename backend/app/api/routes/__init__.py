from fastapi import APIRouter

from app.api.routes.evidence import router as evidence_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.investigations import router as investigations_router

api_router = APIRouter()
api_router.include_router(incidents_router)
api_router.include_router(evidence_router)
api_router.include_router(investigations_router)

__all__ = [
    "api_router",
    "incidents_router",
    "evidence_router",
    "investigations_router",
]
