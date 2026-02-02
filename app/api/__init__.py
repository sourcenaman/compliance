"""API routes package."""

from fastapi import APIRouter

from app.api.routes.control import router as controls_router
from app.api.routes.framework import router as frameworks_router
from app.api.routes.organization import router as organizations_router

api_router = APIRouter()

api_router.include_router(frameworks_router, prefix="/frameworks", tags=["Frameworks"])
api_router.include_router(controls_router, prefix="/controls", tags=["Controls"])
api_router.include_router(organizations_router, prefix="/organizations", tags=["Organizations"])
