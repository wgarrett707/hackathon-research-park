from pydantic import BaseModel
from datetime import datetime

class LocationPoint(BaseModel):
    latitude: float
    longitude: float


class SongRequestInfo(BaseModel):
    location: LocationPoint
    time: datetime
    song_name: str


class LocationChunk(BaseModel):
    topRight: LocationPoint
    bottomLeft: LocationPoint

