from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import random
from datetime import datetime
from src.utils.spotify_service import spotify_service

# Try to import the sophisticated location logic, fallback if it fails
try:
    from src.utils.spotify import get_genre_from_location_and_time, get_song_from_spotify
    from src.models.models import LocationPoint
    SOPHISTICATED_LOCATION_AVAILABLE = True
    print("✅ Sophisticated location logic imported successfully")
except ImportError as e:
    print(f"⚠️ Could not import sophisticated location logic: {e}")
    SOPHISTICATED_LOCATION_AVAILABLE = False

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint to test connectivity"""
    return {"status": "healthy", "message": "Backend is running"}

class PlaybackRequest(BaseModel):
    action: str  # "play", "pause", "next", "previous"
    position: Optional[int] = None  # for seeking

class LocationData(BaseModel):
    latitude: float
    longitude: float

class LocationSkipRequest(BaseModel):
    latitude: float
    longitude: float
    direction: str  # "next" or "previous"

@router.get("/player/status")
async def get_player_status(x_connection_id: Optional[str] = Header(None)):
    """Get current Spotify player status"""
    
    print(f"🔍 Player status request - Connection ID: {x_connection_id}")
    
    # If no connection ID provided, return a "not authenticated" state
    if not x_connection_id:
        print("❌ No connection ID provided")
        return {
            "is_playing": False,
            "current_song": None,
            "current_time": 0,
            "message": "No Nango connection ID provided. Please authenticate with Spotify first."
        }
    
    # Set the connection if provided
    if x_connection_id:
        print(f"🔗 Setting connection: {x_connection_id}")
        spotify_service.set_connection(x_connection_id)
        # Ensure the Spotify client is initialized
        if not spotify_service.spotify:
            print("🔄 Initializing Spotify client...")
            await spotify_service._initialize_spotify_client()
    
    if not spotify_service.spotify:
        print("❌ Spotify client still not available after initialization")
        return {
            "is_playing": False,
            "current_song": None,
            "current_time": 0,
            "message": "Spotify API not available. Please authenticate with Nango first."
        }
    
    print("✅ Spotify client is available, fetching playback state...")
    
    try:
        # Get current playback state from Spotify
        playback_state = await spotify_service.get_current_playback()
        
        if not playback_state:
            return {
                "is_playing": False,
                "current_song": None,
                "current_time": 0,
                "message": "No active Spotify session found"
            }
        
        # Extract current song info
        track = playback_state.get('item', {})
        current_song = {
            "id": track.get('id'),
            "title": track.get('name'),
            "artist": ', '.join([artist['name'] for artist in track.get('artists', [])]),
            "album": track.get('album', {}).get('name'),
            "album_cover": track.get('album', {}).get('images', [{}])[0].get('url') if track.get('album', {}).get('images') else None,
            "spotify_id": track.get('id')
        }
        
        return {
            "is_playing": playback_state.get('is_playing', False),
            "current_song": current_song,
            "current_time": playback_state.get('progress_ms', 0) // 1000,  # Convert to seconds
            "duration": track.get('duration_ms', 0) // 1000 if track else 0,
            "device": playback_state.get('device', {}).get('name', 'Unknown')
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Spotify status: {str(e)}")

@router.post("/player/control")
async def control_player(request: PlaybackRequest, x_connection_id: Optional[str] = Header(None)):
    """Control Spotify playback"""
    
    # Set the connection if provided
    if x_connection_id:
        spotify_service.set_connection(x_connection_id)
    
    if not spotify_service.spotify:
        raise HTTPException(status_code=503, detail="Spotify API not available. Please authenticate with Nango first.")
    
    try:
        if request.action == "play":
            await spotify_service.start_playback()
        elif request.action == "pause":
            await spotify_service.pause_playback()
        elif request.action == "next":
            await spotify_service.next_track()
        elif request.action == "previous":
            await spotify_service.previous_track()
        elif request.action == "seek" and request.position is not None:
            await spotify_service.seek_to_position(request.position * 1000)  # Convert to milliseconds
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Return updated status
        return await get_player_status(x_connection_id)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to control Spotify: {str(e)}")

@router.post("/get_song")
async def get_song(x_connection_id: Optional[str] = Header(None)):
    """Legacy endpoint - returns current song"""
    status = await get_player_status(x_connection_id)
    return status.get("current_song")

@router.post("/refresh-spotify-metadata")
async def refresh_spotify_metadata(x_connection_id: Optional[str] = Header(None)):
    """Refresh song metadata from Spotify API"""
    
    # Set the connection if provided
    if x_connection_id:
        spotify_service.set_connection(x_connection_id)
    
    if not spotify_service.spotify:
        raise HTTPException(status_code=503, detail="Spotify API not available. Please authenticate with Nango first.")
    
    try:
        # Just return current status since we're using live Spotify data
        status = await get_player_status(x_connection_id)
        return {
            "message": "Using live Spotify data",
            "spotify_available": True,
            "current_song": status.get("current_song")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh Spotify metadata: {str(e)}")

@router.get("/spotify-status")
async def get_spotify_status(x_connection_id: Optional[str] = Header(None)):
    """Check if Spotify API is available and configured"""
    
    # Set the connection if provided
    if x_connection_id:
        spotify_service.set_connection(x_connection_id)
    
    has_nango_key = spotify_service.nango_secret_key is not None
    has_connection = spotify_service.connection_id is not None
    has_spotify_client = spotify_service.spotify is not None
    
    return {
        "spotify_available": has_spotify_client,
        "nango_configured": has_nango_key,
        "connection_set": has_connection,
        "message": (
            "Spotify API is ready" if has_spotify_client 
            else "Need Nango connection ID" if has_nango_key and not has_connection
            else "Nango not configured. Set NANGO_SECRET_KEY environment variable."
        )
    }

@router.get("/spotify-auth")
def spotify_auth():
    """Deprecated: Use Nango for Spotify authentication"""
    raise HTTPException(
        status_code=410, 
        detail="This endpoint is deprecated. Use Nango authentication instead. Get a session token from /auth/nango-session-token"
    )

@router.get("/callback")
def spotify_callback(code: str):
    """Deprecated: Use Nango for Spotify authentication"""
    raise HTTPException(
        status_code=410, 
        detail="This endpoint is deprecated. Use Nango authentication instead."
    )

@router.get("/debug/spotify")
async def debug_spotify(x_connection_id: Optional[str] = Header(None)):
    """Debug endpoint to check Spotify connection and playback"""
    
    debug_info = {
        "connection_id_provided": x_connection_id is not None,
        "connection_id": x_connection_id,
        "nango_key_configured": spotify_service.nango_secret_key is not None,
        "spotify_client_initialized": spotify_service.spotify is not None,
    }
    
    if x_connection_id:
        spotify_service.set_connection(x_connection_id)
        
        # Try to initialize if not already done
        if not spotify_service.spotify:
            await spotify_service._initialize_spotify_client()
        
        debug_info.update({
            "spotify_client_after_init": spotify_service.spotify is not None,
        })
        
        if spotify_service.spotify:
            try:
                # Try to get user info to test API access
                user_info = spotify_service.spotify.current_user()
                debug_info["user_info"] = {
                    "id": user_info.get("id"),
                    "display_name": user_info.get("display_name"),
                    "country": user_info.get("country"),
                    "product": user_info.get("product")  # This shows if user has Premium
                }
                
                # Try to get current playback
                playback = await spotify_service.get_current_playback()
                debug_info["playback_response"] = playback is not None
                if playback:
                    debug_info["playback_details"] = {
                        "is_playing": playback.get("is_playing"),
                        "device_name": playback.get("device", {}).get("name"),
                        "device_type": playback.get("device", {}).get("type"),
                        "track_name": playback.get("item", {}).get("name") if playback.get("item") else None
                    }
                
            except Exception as e:
                debug_info["api_error"] = str(e)
    
    return debug_info

@router.post("/get_songs_recs")
async def get_songs_recs(location_data: LocationData, x_connection_id: Optional[str] = Header(None)):
    """Get song recommendations based on user's current location and play them"""
    
    print(f"🗺️ ===== NEW LOCATION-BASED RECOMMENDATION REQUEST =====")
    print(f"🗺️ Getting location-based recommendations for lat: {location_data.latitude}, long: {location_data.longitude}")
    print(f"🔗 Connection ID: {x_connection_id}")
    
    # Set the connection if provided
    if x_connection_id:
        spotify_service.set_connection(x_connection_id)
        # Ensure the Spotify client is initialized
        if not spotify_service.spotify:
            print("🔄 Initializing Spotify client...")
            await spotify_service._initialize_spotify_client()
    
    if not spotify_service.spotify:
        print("❌ Spotify client not available")
        raise HTTPException(status_code=503, detail="Spotify API not available. Please authenticate with Nango first.")
    
    try:
        print("🎵 Generating location-based recommendations...")
        # Generate location-based search terms and find songs
        recommended_tracks = await generate_location_recommendations(location_data)
        
        if not recommended_tracks:
            print("❌ No recommendations generated")
            return {
                "message": "No recommendations found for your location",
                "location": {"latitude": location_data.latitude, "longitude": location_data.longitude},
                "recommendations": []
            }
        
        # Pick a random track instead of always the first one
        import random
        selected_track = random.choice(recommended_tracks)
        print(f"🎯 Attempting to play: {selected_track['name']} by {selected_track['artist']}")
        print(f"🆔 Track Spotify ID: {selected_track['spotify_id']}")
        print(f"🎲 Selected track {recommended_tracks.index(selected_track) + 1} out of {len(recommended_tracks)} recommendations")
        
        try:
            # Try to start playback with the recommended track
            print("📡 Calling Spotify API to start playback...")
            spotify_service.spotify.start_playback(uris=[f"spotify:track:{selected_track['spotify_id']}"])
            print(f"✅ Started playing recommended track: {selected_track['name']} by {selected_track['artist']}")
            
            # Wait a bit for the track to start playing properly
            import asyncio
            print("⏳ Waiting 2 seconds for track to load...")
            await asyncio.sleep(2)
            
            # Return updated status with the new song
            print("🔄 Getting updated player status...")
            status = await get_player_status(x_connection_id)
            print(f"📊 Current player status: {status}")
            
            status['location_recommendations'] = recommended_tracks
            status['selected_track_info'] = selected_track
            status['location'] = {"latitude": location_data.latitude, "longitude": location_data.longitude}
            status['message'] = f"Playing location-based recommendation: {selected_track['name']}"
            
            print(f"✅ Returning status with current_song: {status.get('current_song', {}).get('title', 'Unknown')}")
            return status
            
        except Exception as play_error:
            print(f"❌ Error starting playback: {play_error}")
            print(f"❌ Error type: {type(play_error).__name__}")
            # If we can't play, still return the recommendations
            return {
                "message": f"Found recommendations but couldn't start playback: {str(play_error)}",
                "location": {"latitude": location_data.latitude, "longitude": location_data.longitude},
                "recommendations": recommended_tracks,
                "selected_track_info": selected_track,
                "error": str(play_error)
            }
        
    except Exception as e:
        print(f"❌ Error getting location recommendations: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to get location recommendations: {str(e)}")

async def generate_location_recommendations(location: LocationData) -> List[Dict[str, Any]]:
    """Generate song recommendations based on location using sophisticated logic if available"""
    
    if SOPHISTICATED_LOCATION_AVAILABLE:
        try:
            print("🎯 Using sophisticated location logic...")
            
            # Create LocationPoint object for your existing function
            location_point = LocationPoint(
                latitude=location.latitude,
                longitude=location.longitude
            )
            
            # Get current time
            current_time = datetime.now()
            
            # Use your sophisticated location and time analysis
            location_analysis = get_genre_from_location_and_time(location_point, current_time)
            
            print(f"🗺️ Location analysis: {location_analysis}")
            
            # Get songs using Spotify's recommendation engine with your audio features
            recommended_tracks = get_song_from_spotify(
                location_analysis["audio_features"], 
                spotify_service.spotify
            )
            
            # Add metadata about why this was recommended
            for track in recommended_tracks:
                track['recommendation_reason'] = f"{location_analysis['time_of_day'].title()} time in {location_analysis['location_type']} area"
                track['location_type'] = location_analysis['location_type']
                track['time_of_day'] = location_analysis['time_of_day']
                track['audio_features_used'] = location_analysis['audio_features']
            
            print(f"✅ Found {len(recommended_tracks)} sophisticated recommendations")
            if recommended_tracks:
                return recommended_tracks
            else:
                print("⚠️ No tracks from sophisticated method, falling back...")
                
        except Exception as e:
            print(f"❌ Error in sophisticated location recommendations: {e}")
            print("🔄 Falling back to simple recommendations...")
    
    # Fallback to simple recommendations
    return await generate_simple_location_recommendations(location)

async def generate_simple_location_recommendations(location: LocationData) -> List[Dict[str, Any]]:
    """Fallback simple location-based recommendations that should always work"""
    
    print("🔄 Using simple location recommendations...")
    
    latitude = location.latitude
    longitude = location.longitude
    
    # Enhanced fallback logic with more variety
    base_terms = []
    if 40 <= latitude <= 50 and -125 <= longitude <= -65:  # Northern US/Canada
        base_terms = ["indie folk", "acoustic", "alternative rock", "indie pop", "folk rock"]
    elif 25 <= latitude <= 40 and -125 <= longitude <= -65:  # Southern US
        base_terms = ["country", "blues", "southern rock", "americana", "folk"]
    elif 35 <= latitude <= 60 and -10 <= longitude <= 30:  # Europe
        base_terms = ["electronic", "ambient", "indie", "house", "techno"]
    else:  # Default - more global variety
        base_terms = ["popular", "trending", "indie", "rock", "pop", "electronic"]
    
    # Add some randomness and time-based variety
    import random
    from datetime import datetime
    
    # Add time-based terms
    current_hour = datetime.now().hour
    if 6 <= current_hour <= 12:  # Morning
        base_terms.extend(["morning", "upbeat", "energetic"])
    elif 12 <= current_hour <= 18:  # Afternoon
        base_terms.extend(["chill", "mellow", "afternoon"])
    elif 18 <= current_hour <= 22:  # Evening
        base_terms.extend(["evening", "relaxing", "smooth"])
    else:  # Night
        base_terms.extend(["night", "ambient", "downtempo"])
    
    # Shuffle and pick random search terms
    random.shuffle(base_terms)
    search_terms = base_terms[:3]  # Use 3 random terms
    
    print(f"🎲 Using randomized search terms: {search_terms}")
    
    recommendations = []
    
    for search_term in search_terms:
        try:
            print(f"🔍 Searching for: {search_term}")
            # Add randomness to the search by using different offsets
            offset = random.randint(0, 100)  # Random offset to get different results
            results = spotify_service.spotify.search(q=search_term, type='track', limit=10, offset=offset)
            
            if results['tracks']['items']:
                # Take a random selection from the results
                available_tracks = results['tracks']['items']
                random.shuffle(available_tracks)
                
                for track in available_tracks[:3]:  # Take up to 3 from each search
                    track_info = {
                        'spotify_id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'duration_ms': track['duration_ms'],
                        'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'preview_url': track['preview_url'],
                        'external_urls': track['external_urls'],
                        'popularity': track['popularity'],
                        'recommendation_reason': f"Regional recommendation: {search_term}",
                        'location_type': "regional",
                        'time_of_day': "any"
                    }
                    recommendations.append(track_info)
                    
            if len(recommendations) >= 9:  # Get more recommendations
                break
                
        except Exception as e:
            print(f"❌ Error in search for {search_term}: {e}")
            continue
    
    # If still no recommendations, get some popular tracks with randomness
    if len(recommendations) == 0:
        try:
            print("🔍 Getting popular tracks as last resort...")
            # Use random years and genres for variety
            random_years = ["2024", "2023", "2022", "2021"]
            random_genres = ["pop", "rock", "indie", "electronic", "alternative"]
            
            for _ in range(3):  # Try multiple searches
                year = random.choice(random_years)
                genre = random.choice(random_genres)
                search_query = f"year:{year} genre:{genre}"
                offset = random.randint(0, 500)
                
                popular_results = spotify_service.spotify.search(q=search_query, type='track', limit=5, offset=offset)
                for track in popular_results['tracks']['items']:
                    track_info = {
                        'spotify_id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'album': track['album']['name'],
                        'duration_ms': track['duration_ms'],
                        'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'preview_url': track['preview_url'],
                        'external_urls': track['external_urls'],
                        'popularity': track['popularity'],
                        'recommendation_reason': f"Popular track ({year} {genre})",
                        'location_type': "global",
                        'time_of_day': "any"
                    }
                    recommendations.append(track_info)
                    
                if len(recommendations) >= 6:
                    break
                    
        except Exception as e:
            print(f"❌ Error getting popular tracks: {e}")
    
    # Shuffle the final recommendations for even more randomness
    random.shuffle(recommendations)
    
    print(f"✅ Simple recommendations found: {len(recommendations)} tracks")
    return recommendations[:12]  # Return up to 12 recommendations