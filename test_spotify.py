#!/usr/bin/env python3
"""
Quick test script for Spotify API integration
Run this to verify your Spotify credentials work
"""

import os
import sys
sys.path.append('backend')

from src.utils.spotify_service import spotify_service

def test_spotify_api():
    print("🎵 Testing Spotify API Integration\n")
    
    # Check if API is available
    if not spotify_service.is_available():
        print("❌ Spotify API not available")
        print("💡 Make sure you set these environment variables:")
        print("   SPOTIFY_CLIENT_ID=your_client_id")
        print("   SPOTIFY_CLIENT_SECRET=your_client_secret")
        print("\n📖 See SPOTIFY_SETUP.md for detailed instructions")
        return False
    
    print("✅ Spotify API is available!")
    
    # Test searching for The Weeknd songs
    test_songs = [
        ("Blinding Lights", "The Weeknd"),
        ("Save Your Tears", "The Weeknd"),
        ("In Your Eyes", "The Weeknd")
    ]
    
    print(f"\n🔍 Testing search for {len(test_songs)} songs:\n")
    
    success_count = 0
    for title, artist in test_songs:
        print(f"Searching: {title} by {artist}")
        result = spotify_service.search_track(title, artist)
        
        if result:
            print(f"✅ Found: {result['name']} by {result['artist']}")
            print(f"   Album: {result['album']}")
            print(f"   Cover: {result['album_cover_url'][:60]}...")
            if result['preview_url']:
                print(f"   Preview: Available (30s)")
            else:
                print(f"   Preview: Not available")
            success_count += 1
        else:
            print(f"❌ Not found")
        print()
    
    print(f"📊 Results: {success_count}/{len(test_songs)} songs found")
    
    if success_count > 0:
        print("\n🎉 Spotify integration is working!")
        print("💡 Next steps:")
        print("1. Restart your backend: cd backend && python -m src.main")
        print("2. Test the API: curl -X POST http://localhost:8080/refresh-spotify-metadata")
        print("3. Check your frontend - you should see real album covers!")
        return True
    else:
        print("\n⚠️  No songs found. This might be normal if:")
        print("- Song titles don't match exactly")
        print("- Artists have different names on Spotify")
        print("- Songs aren't available in your region")
        return False

if __name__ == "__main__":
    test_spotify_api()
