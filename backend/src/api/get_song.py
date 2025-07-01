from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.utils.spotify_service import spotify_service

router = APIRouter()

class PlaybackRequest(BaseModel):
    action: str  # "play", "pause", "next", "previous"
    position: Optional[int] = None  # for seeking

@router.get("/player/status")
def get_player_status():
    """Get current Spotify player status"""
    if not spotify_service.is_available():
        raise HTTPException(status_code=503, detail="Spotify API not available. Check credentials.")
    
    try:
        # Get current playback state from Spotify
        playback_state = spotify_service.get_current_playback()
        
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
def control_player(request: PlaybackRequest):
    """Control Spotify playback"""
    if not spotify_service.is_available():
        raise HTTPException(status_code=503, detail="Spotify API not available. Check credentials.")
    
    try:
        if request.action == "play":
            spotify_service.start_playback()
        elif request.action == "pause":
            spotify_service.pause_playback()
        elif request.action == "next":
            spotify_service.next_track()
        elif request.action == "previous":
            spotify_service.previous_track()
        elif request.action == "seek" and request.position is not None:
            spotify_service.seek_to_position(request.position * 1000)  # Convert to milliseconds
        else:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Return updated status
        return get_player_status()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to control Spotify: {str(e)}")

@router.post("/get_song")
def get_song():
    """Legacy endpoint - returns current song"""
    status = get_player_status()
    return status.get("current_song")

@router.post("/refresh-spotify-metadata")
def refresh_spotify_metadata():
    """Refresh song metadata from Spotify API"""
    if not spotify_service.is_available():
        raise HTTPException(status_code=503, detail="Spotify API not available. Check credentials.")
    
    try:
        # Just return current status since we're using live Spotify data
        status = get_player_status()
        return {
            "message": "Using live Spotify data",
            "spotify_available": True,
            "current_song": status.get("current_song")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh Spotify metadata: {str(e)}")

@router.get("/spotify-status")
def get_spotify_status():
    """Check if Spotify API is available and configured"""
    return {
        "spotify_available": spotify_service.is_available(),
        "message": "Spotify API is ready" if spotify_service.is_available() else "Spotify API not configured. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables."
    }

@router.get("/spotify-auth")
def spotify_auth():
    """Get Spotify authorization URL"""
    if not spotify_service.spotify_oauth:
        raise HTTPException(status_code=503, detail="Spotify OAuth not configured")
    
    auth_url = spotify_service.get_auth_url()
    if not auth_url:
        raise HTTPException(status_code=500, detail="Failed to generate authorization URL")
    
    return {
        "auth_url": auth_url,
        "message": "Visit this URL to authorize the application"
    }

@router.get("/callback")
def spotify_callback(code: str):
    """Handle Spotify OAuth callback"""
    if not spotify_service.spotify_oauth:
        raise HTTPException(status_code=503, detail="Spotify OAuth not configured")
    
    success = spotify_service.get_access_token(code)
    if success:
        return {
            "message": "Spotify authorization successful!",
            "spotify_available": True
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to complete Spotify authorization")