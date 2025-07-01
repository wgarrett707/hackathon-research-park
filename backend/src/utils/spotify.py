from datetime import datetime
from src.models.models import LocationChunk, LocationPoint
from src.utils.spotify_auth import get_spotify_client

def get_song_from_spotify(genre: str):
    pass

def get_genre_from_location_and_time(location_point: LocationPoint, time: datetime):
    current_time = time.hour()
    if 21 <= current_time or current_time < 8:
        time_of_day = "night"
    else:
        time_of_day = "day"
    
    chunks = [
        {
            "name": "downtown",
            "lat_min": 40.106547,
            "lat_max": 40.111303, 
            "lon_min": -88.242023,
            "lon_max": -88.214757,
            "type": "urban",
            "building_types": ["bars", "clubs", "restaurants"]
        },
        {
            "name": "town",
            "lat_min": 40.084082,
            "lat_max": 40.092088,
            "lon_min": -88.209529,
            "lon_max": -88.199730,
            "type": "suburban",
            "building_types": ["apartments", "cafes"]
        },
        {
            "name": "country_roads",
            "lat_min": 40.072587,
            "lat_max": 40.093647,
            "lon_min": -88.238746,
            "lon_max": -88.223972,
            "type": "rural",
            "building_types": ["farmland", "parks"]
        }
    ]
    loc_type = None
    for chunk in range(chunks):
        if location_point.latitude <= chunk["lat_max"] and location_point.latitude >= chunk["lat_min"] and location_point.longitude <= chunk["long_max"] and location_point.longitude >= chunk["long_min"]:
            loc_type = chunk["type"]
            

    audio_features = {
        "acousticness" : 1,
        "danceability": 1,
        "energy": 1,
        "tempo": 1,
        "valence": 1,
        "instrumentalness": 1,
        "speechiness": 1
    }
    if time_of_day == "night" and loc_type == "urban":
        audio_features["energy"] = 0.8
        audio_features["danceability"] = 0.9
        audio_features["tempo"] = 0.6

    if time_of_day == "night" and loc_type == "suburban":
        audio_features["valence"] = 0.4
        audio_features["energy"] = 0.3


    if time_of_day == "night" and loc_type == "rural":
        audio_features["energy"] = 0.2
        audio_features["instrumentalness"] = 0.6   

    if time_of_day == "day" and loc_type == "urban":
        audio_features["speechiness"] = 0.7
        audio_features["tempo"] = 0.8


    if time_of_day == "day" and loc_type == "suburban":
        audio_features["energy"] = 0.6
        audio_features["speechiness"] = 0.6
        
        
    if time_of_day == "day" and loc_type == "rural":
        audio_features["energy"] = 0.7
        audio_features["tempo"] = 0.1
        

    return audio_features




