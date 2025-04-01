from fastapi import FastAPI
from src.api.peaks import router as peaks_router
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
IS_PRODUCTION = os.getenv("PRODUCTION", "FALSE").lower() == "true"
app = FastAPI(
    title="Peaks API",
    description="Find data about mountains.",
    version="1.0",
    docs_url=None if IS_PRODUCTION else "/docs",  # Disable Swagger UI
    redoc_url=None if IS_PRODUCTION else "/redoc",  # Disable ReDoc
    openapi_url=None if IS_PRODUCTION else "/openapi.json"
)
app.include_router(peaks_router)


# @app.get("/")
# def read_root():
#     return