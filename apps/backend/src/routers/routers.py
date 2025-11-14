from fastapi import APIRouter
from src.routers.endpoints.predict import router as prediction_router

router = APIRouter()

router.include_router(prediction_router)

