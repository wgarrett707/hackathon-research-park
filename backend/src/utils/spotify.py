from datetime import datetime
from src.models.models import LocationChunk, LocationPoint
from src.utils.spotify_auth import get_spotify_client

def get_song_from_spotify(audio_features: dict, spotify_client):
    """Get song recommendations based on audio features"""
    try:
        # Get recommendations using Spotify's recommendation engine
        recommendations = spotify_client.recommendations(
            limit=10,
            target_acousticness=audio_features.get("acousticness", 0.5),
            target_danceability=audio_features.get("danceability", 0.5),
            target_energy=audio_features.get("energy", 0.5),
            target_instrumentalness=audio_features.get("instrumentalness", 0.5),
            target_speechiness=audio_features.get("speechiness", 0.5),
            target_tempo=audio_features.get("tempo", 0.5) * 200,  # Scale tempo to BPM range
            target_valence=audio_features.get("valence", 0.5)
        )
        
        tracks = []
        for track in recommendations['tracks']:
            track_info = {
                'spotify_id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'external_urls': track['external_urls'],
                'popularity': track['popularity']
            }
            tracks.append(track_info)
            
        return tracks
        
    except Exception as e:
        print(f"❌ Error getting Spotify recommendations: {e}")
        return []

def get_genre_from_location_and_time(location_point: LocationPoint, time: datetime):
    current_time = time.hour
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
    for chunk in chunks:
        if (location_point.latitude <= chunk["lat_max"] and location_point.latitude >= chunk["lat_min"] and 
            location_point.longitude <= chunk["lon_max"] and location_point.longitude >= chunk["lon_min"]):
            loc_type = chunk["type"]
            break

    audio_features = {
        "acousticness": 1,
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

    elif time_of_day == "night" and loc_type == "suburban":
        audio_features["valence"] = 0.4
        audio_features["energy"] = 0.3

    elif time_of_day == "night" and loc_type == "rural":
        audio_features["energy"] = 0.2
        audio_features["instrumentalness"] = 0.6   

    elif time_of_day == "day" and loc_type == "urban":
        audio_features["speechiness"] = 0.7
        audio_features["tempo"] = 0.8

    elif time_of_day == "day" and loc_type == "suburban":
        audio_features["energy"] = 0.6
        audio_features["speechiness"] = 0.6
        
    elif time_of_day == "day" and loc_type == "rural":
        audio_features["energy"] = 0.7
        audio_features["tempo"] = 0.1
    
    return {
        "location_type": loc_type,
        "time_of_day": time_of_day,
        "audio_features": audio_features
    }







