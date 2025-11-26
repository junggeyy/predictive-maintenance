from fastapi import APIRouter
from src.routers.endpoints.predict import router as prediction_router
from src.routers.endpoints.mcp import router as mcp_router

router = APIRouter()

router.include_router(prediction_router)
router.include_router(mcp_router)

