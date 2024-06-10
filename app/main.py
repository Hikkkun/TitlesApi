from fastapi import FastAPI
from .routers import manga, ranobe
import uvicorn

app = FastAPI()

app.include_router(manga.router)
app.include_router(ranobe.router)

@app.get("/")
def read_root():
    return {"message": "API для Ранобе и Манги"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)