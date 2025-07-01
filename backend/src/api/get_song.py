from fastapi import APIRouter

router = APIRouter()

@router.post("/get_song")
def get_song():
    return {"message": "get_song endpoint called"} 