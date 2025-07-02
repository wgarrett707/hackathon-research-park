from datetime import datetime
from src.models.models import LocationChunk, LocationPoint
from src.utils.spotify_auth import get_spotify_client

def get_song_from_spotify(audio_features: dict, spotify_client):
    """Get song recommendations based on audio features"""
    try:
        # Add some randomization to avoid getting the same songs every time
        import random
        
        # Create slight variations in the audio features for variety
        varied_features = {}
        for key, value in audio_features.items():
            if key == "tempo":
                # Tempo is scaled differently, keep original logic
                varied_features[f"target_{key}"] = value * 200
            else:
                # Add small random variation (±0.1) while keeping within bounds
                variation = random.uniform(-0.1, 0.1)
                varied_value = max(0.0, min(1.0, value + variation))
                varied_features[f"target_{key}"] = varied_value
        
        print(f"🎵 Using varied audio features: {varied_features}")
        
        # Get recommendations using Spotify's recommendation engine
        recommendations = spotify_client.recommendations(
            limit=15,  # Get more recommendations for better variety
            **varied_features
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
        
        # Shuffle the results to add more randomness
        random.shuffle(tracks)
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

    # # TESTING - REMOVE THIS IN PRODUCTION
    # location_point.latitude = 40.106549
    # location_point.longitude = -88.23
    # time_of_day = "night"
    
    loc_type = None
    for chunk in chunks:
        if (location_point.latitude <= chunk["lat_max"] and location_point.latitude >= chunk["lat_min"] and 
            location_point.longitude <= chunk["lon_max"] and location_point.longitude >= chunk["lon_min"]):
            loc_type = chunk["type"]
            break
    loc_type = "urban" 
    print(f"🗺️ Detected location type: {loc_type} at {time_of_day} time")
    
    # Start with balanced audio features (0.5 = neutral)
    audio_features = {
        "acousticness": 0.5,
        "danceability": 0.5,
        "energy": 0.5,
        "tempo": 0.5,
        "valence": 0.5,
        "instrumentalness": 0.3,  # Lower default - most songs have vocals
        "speechiness": 0.1        # Lower default - most songs aren't very speech-heavy
    }
    
    # Adjust audio features based on location and time
    if time_of_day == "night" and loc_type == "urban":
        # Night in the city - chill but sophisticated
        audio_features["energy"] = 0.4          # Moderate energy
        audio_features["danceability"] = 0.6    # Still danceable
        audio_features["tempo"] = 0.4           # Slower tempo
        audio_features["valence"] = 0.3         # Slightly melancholic
        audio_features["instrumentalness"] = 0.2 # Some vocals
        audio_features["speechiness"] = 0.1     # Not speech-heavy
        audio_features["acousticness"] = 0.3    # Some acoustic elements

    elif time_of_day == "night" and loc_type == "suburban":
        # Night in suburbs - relaxed and cozy
        audio_features["valence"] = 0.5         # Neutral mood
        audio_features["energy"] = 0.3          # Lower energy
        audio_features["acousticness"] = 0.6    # More acoustic
        audio_features["danceability"] = 0.4    # Less danceable
        audio_features["tempo"] = 0.3           # Slower

    elif time_of_day == "night" and loc_type == "rural":
        # Night in countryside - peaceful and introspective
        audio_features["energy"] = 0.3          # Low energy
        audio_features["instrumentalness"] = 0.5 # More instrumental
        audio_features["acousticness"] = 0.7    # Very acoustic
        audio_features["valence"] = 0.4         # Contemplative
        audio_features["tempo"] = 0.3           # Slow tempo

    elif time_of_day == "day" and loc_type == "urban":
        # Day in the city - energetic and upbeat
        audio_features["speechiness"] = 0.2     # Some speech elements (but not too much)
        audio_features["tempo"] = 0.7           # Faster tempo
        audio_features["energy"] = 0.7          # High energy
        audio_features["danceability"] = 0.7    # Very danceable
        audio_features["valence"] = 0.7         # Happy/positive

    elif time_of_day == "day" and loc_type == "suburban":
        # Day in suburbs - moderate energy, pleasant
        audio_features["energy"] = 0.6          # Good energy
        audio_features["speechiness"] = 0.1     # Minimal speech
        audio_features["valence"] = 0.6         # Positive mood
        audio_features["danceability"] = 0.6    # Moderately danceable
        audio_features["tempo"] = 0.6           # Moderate tempo
        
    elif time_of_day == "day" and loc_type == "rural":
        # Day in countryside - folk and country vibes
        audio_features["energy"] = 0.5          # Moderate energy
        audio_features["tempo"] = 0.4           # Relaxed tempo
        audio_features["acousticness"] = 0.8    # Very acoustic
        audio_features["valence"] = 0.6         # Pleasant mood
        audio_features["instrumentalness"] = 0.3 # Some instrumental tracks
    
    print(f"🎵 Audio features for {time_of_day} {loc_type}: {audio_features}")
    
    return {
        "location_type": loc_type,
        "time_of_day": time_of_day,
        "audio_features": audio_features
    }
