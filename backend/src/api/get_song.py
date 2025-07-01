from fastapi import APIRouter

router = APIRouter("/song")

@router.post("/get_song")
def get_song():
    return {"message": "get_song endpoint called"} 