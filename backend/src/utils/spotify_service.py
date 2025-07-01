import spotipy
import os
import httpx
from typing import Optional, Dict, Any

class SpotifyService:
    def __init__(self):
        """Initialize Spotify API client with Nango integration"""
        self.nango_secret_key = os.getenv('NANGO_SECRET_KEY')
        self.spotify = None
        self.connection_id = None
        
        if not self.nango_secret_key:
            print("⚠️  Warning: NANGO_SECRET_KEY not set. Spotify functionality will be limited.")
    
    def set_connection(self, connection_id: str) -> bool:
        """Set the Nango connection ID - actual initialization happens lazily"""
        self.connection_id = connection_id
        # Don't initialize immediately since this is a sync method
        # Initialization will happen on first API call
        return True
    
    async def _initialize_spotify_client(self) -> bool:
        """Initialize Spotify client using Nango credentials"""
        if not self.connection_id or not self.nango_secret_key:
            return False
            
        try:
            # Get connection credentials from Nango
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.nango.dev/connection/{self.connection_id}",
                    headers={
                        "Authorization": f"Bearer {self.nango_secret_key}",
                        "Content-Type": "application/json"
                    },
                    params={
                        "provider_config_key": "spotify"
                    }
                )
                
                if response.status_code == 200:
                    connection_data = response.json()
                    print(f"🔍 Nango connection data: {connection_data}")
                    
                    # Check what scopes are available
                    metadata = connection_data.get('metadata', {})
                    scopes = metadata.get('scopes') or connection_data.get('scopes', [])
                    print(f"🔑 Available scopes: {scopes}")
                    
                    credentials = connection_data.get('credentials', {})
                    access_token = credentials.get('access_token')
                    
                    if access_token:
                        # Print first few characters of token for debugging (don't log full token for security)
                        print(f"🔑 Access token received: {access_token[:20]}...")
                        # Initialize Spotipy client with the access token
                        self.spotify = spotipy.Spotify(auth=access_token)
                        print("✅ Spotify API client initialized with Nango credentials")
                        return True
                    else:
                        print("❌ No access token found in Nango connection")
                        return False
                else:
                    print(f"❌ Failed to get Nango connection: {response.status_code}")
                    return False
                    
        except Exception as e:
            print(f"❌ Error initializing Spotify client with Nango: {e}")
            return False

    def search_track(self, track_name: str, artist_name: str) -> Optional[Dict[str, Any]]:
        """Search for a track and return metadata including album cover"""
        if not self.spotify:
            print("❌ Spotify API not available")
            return None
            
        try:
            # Search for the track
            query = f"track:{track_name} artist:{artist_name}"
            results = self.spotify.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                
                # Extract relevant information
                track_info = {
                    'spotify_id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'album_cover_640': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'album_cover_300': track['album']['images'][1]['url'] if len(track['album']['images']) > 1 else None,
                    'album_cover_64': track['album']['images'][2]['url'] if len(track['album']['images']) > 2 else None,
                    'preview_url': track['preview_url'],  # 30-second preview
                    'external_urls': track['external_urls'],
                    'popularity': track['popularity']
                }
                
                print(f"✅ Found track: {track_info['name']} by {track_info['artist']}")
                return track_info
            else:
                print(f"❌ No results found for {track_name} by {artist_name}")
                return None
                
        except Exception as e:
            print(f"❌ Error searching for track: {e}")
            return None

    def get_track_by_id(self, spotify_id: str) -> Optional[Dict[str, Any]]:
        """Get track information by Spotify ID"""
        if not self.spotify:
            return None
            
        try:
            track = self.spotify.track(spotify_id)
            return {
                'spotify_id': track['id'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'album_cover_url': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'preview_url': track['preview_url'],
                'external_urls': track['external_urls']
            }
        except Exception as e:
            print(f"❌ Error getting track by ID: {e}")
            return None

    async def get_current_playback(self) -> Optional[Dict[str, Any]]:
        """Get current playback state"""
        if not self.spotify:
            print("❌ Spotify client not initialized")
            return None
            
        try:
            print("🔍 Fetching current playback state...")
            playback = self.spotify.current_playback()
            
            if playback is None:
                print("⚠️  No active playback session found")
                return None
            elif not playback:
                print("⚠️  Empty playback response")
                return None
            else:
                print(f"✅ Got playback state: playing={playback.get('is_playing')}, device={playback.get('device', {}).get('name', 'Unknown')}")
                return playback
                
        except Exception as e:
            print(f"❌ Error getting current playback: {e}")
            print(f"❌ Error type: {type(e).__name__}")
            print(f"❌ Error details: {str(e)}")
            
            # Try to refresh connection and retry once
            print("🔄 Attempting to refresh Spotify connection...")
            if await self._initialize_spotify_client():
                try:
                    print("🔄 Retrying playback request...")
                    playback = self.spotify.current_playback()
                    if playback:
                        print("✅ Retry successful!")
                        return playback
                    else:
                        print("⚠️  Retry returned empty playback")
                        return None
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
            else:
                print("❌ Failed to refresh Spotify connection")
            return None

    async def start_playback(self):
        """Start/resume playback"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.start_playback()
        except Exception as e:
            print(f"❌ Error starting playback: {e}")
            # Try to refresh connection and retry
            if await self._initialize_spotify_client():
                try:
                    self.spotify.start_playback()
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
                    raise
            else:
                raise

    async def pause_playback(self):
        """Pause playback"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.pause_playback()
        except Exception as e:
            print(f"❌ Error pausing playback: {e}")
            # Try to refresh connection and retry
            if await self._initialize_spotify_client():
                try:
                    self.spotify.pause_playback()
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
                    raise
            else:
                raise

    async def next_track(self):
        """Skip to next track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.next_track()
        except Exception as e:
            print(f"❌ Error skipping to next track: {e}")
            # Try to refresh connection and retry
            if await self._initialize_spotify_client():
                try:
                    self.spotify.next_track()
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
                    raise
            else:
                raise

    async def previous_track(self):
        """Skip to previous track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.previous_track()
        except Exception as e:
            print(f"❌ Error skipping to previous track: {e}")
            # Try to refresh connection and retry
            if await self._initialize_spotify_client():
                try:
                    self.spotify.previous_track()
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
                    raise
            else:
                raise

    async def seek_to_position(self, position_ms: int):
        """Seek to specific position in current track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.seek_track(position_ms)
        except Exception as e:
            print(f"❌ Error seeking to position: {e}")
            # Try to refresh connection and retry
            if await self._initialize_spotify_client():
                try:
                    self.spotify.seek_track(position_ms)
                except Exception as retry_e:
                    print(f"❌ Retry failed: {retry_e}")
                    raise
            else:
                raise

    def is_available(self) -> bool:
        """Check if Spotify API is available"""
        return self.spotify is not None

# Create a global instance
spotify_service = SpotifyService()
