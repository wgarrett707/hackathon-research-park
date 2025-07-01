import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from typing import Optional, Dict, Any

class SpotifyService:
    def __init__(self):
        """Initialize Spotify API client"""
        # You'll need to set these environment variables or replace with your credentials
        client_id = os.getenv('SPOTIFY_CLIENT_ID', 'your_client_id_here')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_client_secret_here')
        redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:8080/callback')
        
        if client_id == 'your_client_id_here' or client_secret == 'your_client_secret_here':
            print("⚠️  Warning: Using placeholder Spotify credentials. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables.")
            self.spotify = None
            self.spotify_oauth = None
        else:
            try:
                # For playback control, we need OAuth with user permissions
                scope = "user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
                self.spotify_oauth = SpotifyOAuth(
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scope=scope,
                    show_dialog=True
                )
                
                # Try to get cached token or create OAuth client
                token_info = self.spotify_oauth.get_cached_token()
                if token_info:
                    self.spotify = spotipy.Spotify(auth=token_info['access_token'])
                    print("✅ Spotify API client initialized with OAuth")
                else:
                    print("⚠️  Spotify OAuth not authenticated. User needs to authorize.")
                    self.spotify = None
                    
            except Exception as e:
                print(f"❌ Failed to initialize Spotify API: {e}")
                self.spotify = None
                self.spotify_oauth = None

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

    def get_current_playback(self) -> Optional[Dict[str, Any]]:
        """Get current playback state"""
        if not self.spotify:
            return None
            
        try:
            return self.spotify.current_playback()
        except Exception as e:
            print(f"❌ Error getting current playback: {e}")
            return None

    def start_playback(self):
        """Start/resume playback"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.start_playback()
        except Exception as e:
            print(f"❌ Error starting playback: {e}")
            raise

    def pause_playback(self):
        """Pause playback"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.pause_playback()
        except Exception as e:
            print(f"❌ Error pausing playback: {e}")
            raise

    def next_track(self):
        """Skip to next track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.next_track()
        except Exception as e:
            print(f"❌ Error skipping to next track: {e}")
            raise

    def previous_track(self):
        """Skip to previous track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.previous_track()
        except Exception as e:
            print(f"❌ Error skipping to previous track: {e}")
            raise

    def seek_to_position(self, position_ms: int):
        """Seek to specific position in current track"""
        if not self.spotify:
            raise Exception("Spotify API not available")
            
        try:
            self.spotify.seek_track(position_ms)
        except Exception as e:
            print(f"❌ Error seeking to position: {e}")
            raise

    def get_auth_url(self) -> Optional[str]:
        """Get Spotify authorization URL for user authentication"""
        if not self.spotify_oauth:
            return None
        return self.spotify_oauth.get_authorize_url()

    def get_access_token(self, code: str) -> bool:
        """Exchange authorization code for access token"""
        if not self.spotify_oauth:
            return False
            
        try:
            token_info = self.spotify_oauth.get_access_token(code)
            if token_info:
                self.spotify = spotipy.Spotify(auth=token_info['access_token'])
                print("✅ Spotify OAuth completed successfully")
                return True
        except Exception as e:
            print(f"❌ Error getting access token: {e}")
        return False

    def is_available(self) -> bool:
        """Check if Spotify API is available"""
        return self.spotify is not None

# Create a global instance
spotify_service = SpotifyService()
