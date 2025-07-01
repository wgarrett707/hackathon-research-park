import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional
from dotenv import load_dotenv

load_dotenv(".env")

class SpotifyAuth:
    """
    Spotify authentication handler using client credentials flow.
    This is suitable for server-to-server applications where user authorization is not required.
    """
    
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.authenticate()


        if not self.client_id or not self.client_secret:
            raise ValueError(
                "SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables must be set"
            )
    
    def authenticate(self) -> spotipy.Spotify:
        """
        Authenticate with Spotify using client credentials flow.
        
        Returns:
            spotipy.Spotify: Authenticated Spotify client instance
        """
        print(self.client_id, self.client_secret)
        # Create client credentials manager
        client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        # Create Spotify client
        self.sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager
        )
        
        return self.sp
    
    def get_client(self) -> spotipy.Spotify:
        """
        Get the authenticated Spotify client. If not authenticated, authenticate first.
        
        Returns:
            spotipy.Spotify: Authenticated Spotify client instance
        """
        if self.sp is None:
            return self.authenticate()
        return self.sp


def get_spotify_client() -> spotipy.Spotify:
    """
    Convenience function to get an authenticated Spotify client.
    
    Returns:
        spotipy.Spotify: Authenticated Spotify client instance
    """
    return SpotifyAuth().get_client()


if __name__ == "__main__":

    spotify = get_spotify_client()

    birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

    results = spotify.artist_albums(birdy_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])