from typing import Union
from fastapi import FastAPI
from src.api.peaks import router as peaks_router

app = FastAPI()
app.include_router(peaks_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}