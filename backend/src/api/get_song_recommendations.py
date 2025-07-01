from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import random
from src.utils.spotify import get_genre_from_location_and_time
from pydantic import BaseModel
from src.models.models import LocationPoint
from datetime import datetime




bearer_scheme = HTTPBearer()
router = APIRouter()

    

@router.post("/get_song_recs")
def get_songs(current_location: LocationPoint, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    url = "https://api.spotify.com/v1/me/top/tracks"
    token = credentials.credentials

    headers = {
        "Authorization": f"Bearer {token}"
    }
    query_params = {
        "limit": 20
    }
    response = httpx.get(url, headers=headers, params=query_params)

    res = response.json()
    
    track_ids = []
    
    for i in range(len(res.items)):
        track_ids.append(res.items[i].id)

    pick_random_track_id = random.randint(0, len(res.items) - 1)
    random_track = track_ids[pick_random_track_id]

    current_datetime = datetime.now()

    current_hour = current_datetime.hour

    audio_features = get_genre_from_location_and_time(current_location, current_hour)

    url = "https://api.reccobeats.com/v1/track/recommendation"
    params = {
        "size": 5,
        "seeds": random_track,
        "acousticness": audio_features["acousticness"],
        "danceability": audio_features["danceability"],
        "energy": audio_features["energy"],
        "tempo": audio_features["tempo"],
        "valence": audio_features["valence"],
        "instrumentalness": audio_features["instrumentalness"],
        "speechiness": audio_features["speechiness"]
    }

    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {token}"
    }

    response = httpx.get(url, headers=headers, params=params)

    result = response.json()
    content = result["content"]
    track_id_return = []
    for track in content:
        track_id_return.append('spotify:track:' + track)

    base_add_queue_url = "https://api.spotify.com/v1/me/player/queue"
    for track in track_id_return:
        params_in_upload = {
            "uri": track
        }
        httpx.post(base_add_queue_url, headers=headers, params=params_in_upload)
        
    return track_id_return