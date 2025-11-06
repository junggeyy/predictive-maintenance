from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.core.model_loader import get_classification_model, get_regression_model
from src.routers.routers import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # loading the model on startup & store it for future uses
    get_classification_model()
    get_regression_model()
    print("All models loaded")
    yield

app = FastAPI(
    title="predictive-maintenance-server",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/check")
def health_check():
    return {"message": "Hello, world!"}