from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from src.utils.spotify_service import spotify_service

router = APIRouter()

@router.get("/health")
def health_check():
    """Health check endpoint to test connectivity"""
    return {"status": "healthy", "message": "Backend is running"}

class PlaybackRequest(BaseModel):
    action: str  # "play", "pause", "next", "previous"
    position: Optional[int] = None  # for seeking

@router.get("/player/status")
async def get_player_status(x_connection_id: Optional[str] = Header(None)):
    """Get current Spotify player status"""
    
    # If no connection ID provided, return a "not authenticated" state
    if not x_connection_id:
        return {
            "is_playing": False,
            "current_song": None,
            "current_time": 0,
            "message": "No Nango connection ID provided. Please authenticate with Spotify first."
        }
    
    # Set the connection if provided
    spotify_service.set_connection(x_connection_id)
    
    if not spotify_service.spotify:
        return {
            "is_playing": False,
            "current_song": None,
            "current_time": 0,
            "message": "Spotify API not available. Please authenticate with Nango first."
        }
    
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