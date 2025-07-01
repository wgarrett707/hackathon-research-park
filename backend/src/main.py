import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.api import get_song_router, auth_router

app = FastAPI(title="Music Player API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(get_song_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "Backend is running"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "SpotOn Music Player API", "docs": "/docs"}

# For development: run with 'python main.py'
# For production: use 'uvicorn backend.src.main:app --reload'
if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)
