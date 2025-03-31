from fastapi import FastAPI
from src.api.peaks import router as peaks_router

app = FastAPI()
app.include_router(peaks_router)
