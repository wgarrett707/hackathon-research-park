from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api import get_song_router, auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_song_router)
app.include_router(auth_router)

# For development: run with 'python main.py'
# For production: use 'uvicorn backend.src.main:app --reload'
if __name__ == "__main__":
    uvicorn.run("backend.src.main:app", host="0.0.0.0", port=8080, reload=True)
