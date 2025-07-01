#!/usr/bin/env python3
"""
Integration Test Script for Music Player Backend/Frontend
Tests all API endpoints and verifies they work correctly
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api_endpoint(method, endpoint, data=None, expected_status=200):
    """Test an API endpoint and return the response"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        print(f"{method} {endpoint}: Status {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ Success!")
            if response.content:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2)}")
                return result
        else:
            print(f"❌ Expected status {expected_status}, got {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed! Make sure the backend server is running on port 8000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
    return None

def main():
    print("🎵 Music Player Integration Test\n")
    print("Make sure the backend server is running with: python -m src.main\n")
    
    # Test 1: Get initial player status
    print("1. Testing GET /player/status")
    status = test_api_endpoint("GET", "/player/status")
    if not status:
        print("❌ Failed to get player status. Exiting.")
        return
    
    print(f"Current song: {status['current_song']['title']} by {status['current_song']['artist']}")
    print(f"Playing: {status['is_playing']}")
    print()
    
    # Test 2: Play music
    print("2. Testing POST /player/control (play)")
    play_result = test_api_endpoint("POST", "/player/control", {"action": "play"})
    if play_result:
        print(f"Now playing: {play_result['is_playing']}")
    print()
    
    # Test 3: Pause music
    print("3. Testing POST /player/control (pause)")
    pause_result = test_api_endpoint("POST", "/player/control", {"action": "pause"})
    if pause_result:
        print(f"Now playing: {pause_result['is_playing']}")
    print()
    
    # Test 4: Next track
    print("4. Testing POST /player/control (next)")
    next_result = test_api_endpoint("POST", "/player/control", {"action": "next"})
    if next_result:
        print(f"Now playing: {next_result['current_song']['title']}")
        print(f"Song index: {next_result['current_song_index']}")
    print()
    
    # Test 5: Previous track
    print("5. Testing POST /player/control (previous)")
    prev_result = test_api_endpoint("POST", "/player/control", {"action": "previous"})
    if prev_result:
        print(f"Now playing: {prev_result['current_song']['title']}")
        print(f"Song index: {prev_result['current_song_index']}")
    print()
    
    # Test 6: Seek to position
    print("6. Testing POST /player/control (seek)")
    seek_result = test_api_endpoint("POST", "/player/control", {"action": "seek", "position": 30})
    if seek_result:
        print(f"Seeked to: {seek_result['current_time']} seconds")
    print()
    
    # Test 7: Legacy get_song endpoint
    print("7. Testing POST /get_song (legacy)")
    song_result = test_api_endpoint("POST", "/get_song")
    print()
    
    print("🎉 Integration test complete!")
    print("\nTo test the frontend integration:")
    print("1. Make sure the backend is running (python -m src.main)")
    print("2. Start the frontend (npm run dev in frontend directory)")
    print("3. Open http://localhost:5173 in your browser")
    print("4. Try clicking the play, pause, next, and previous buttons")

if __name__ == "__main__":
    main()
