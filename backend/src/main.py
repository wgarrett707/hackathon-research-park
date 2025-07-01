from fastapi import FastAPI
import uvicorn

from src.api import get_song_router

app = FastAPI()


app.include_router(get_song_router)

# For development: run with 'python main.py'
# For production: use 'uvicorn backend.src.main:app --reload'
if __name__ == "__main__":
    uvicorn.run("backend.src.main:app", host="0.0.0.0", port=8000, reload=True)
