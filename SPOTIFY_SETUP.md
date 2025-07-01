# 🎵 Spotify API Integration Setup

This guide shows you how to get real album covers and metadata from Spotify.

## Step 1: Get Spotify API Credentials

1. **Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)**
2. **Log in** with your Spotify account
3. **Click "Create App"**
4. **Fill out the form:**
   - App Name: "My Music Player"
   - App Description: "Personal music player project"
   - Website: `http://localhost:5173`
   - Redirect URI: `http://localhost:5173` (not used for this project)
   - Check "Web API" in the APIs used section
5. **Click "Save"**
6. **Copy your Client ID and Client Secret**

## Step 2: Set Environment Variables

### Windows (PowerShell):
```powershell
# Set environment variables (replace with your actual credentials)
$env:SPOTIFY_CLIENT_ID = "your_client_id_here"
$env:SPOTIFY_CLIENT_SECRET = "your_client_secret_here"

# Verify they're set
echo $env:SPOTIFY_CLIENT_ID
echo $env:SPOTIFY_CLIENT_SECRET
```

### Windows (Command Prompt):
```cmd
set SPOTIFY_CLIENT_ID=your_client_id_here
set SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### For Permanent Setup (Windows):
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Environment Variables"
3. Under "User variables", click "New"
4. Add `SPOTIFY_CLIENT_ID` with your client ID
5. Add `SPOTIFY_CLIENT_SECRET` with your client secret
6. Restart your terminal/IDE

## Step 3: Test Spotify Integration

1. **Restart your backend** (important - it needs to load the new environment variables):
   ```bash
   cd backend
   python -m src.main
   ```

2. **Test Spotify status:**
   ```bash
   curl http://localhost:8080/spotify-status
   ```

3. **Refresh metadata to get real album covers:**
   ```bash
   curl -X POST http://localhost:8080/refresh-spotify-metadata
   ```

## Step 4: Update Frontend to Use Spotify Data

The frontend will automatically use the new album covers once the backend is updated.

## What You'll Get

✅ **Real album covers** from Spotify  
✅ **Accurate song metadata** (correct titles, artists, albums)  
✅ **30-second Spotify previews** (optional)  
✅ **High-quality images** (640x640, 300x300, 64x64)  

## Example Result

Before:
```json
{
  "title": "Blinding Lights",
  "artist": "The Weeknd",
  "album_cover": "https://via.placeholder.com/300x300/..."
}
```

After:
```json
{
  "title": "Blinding Lights",
  "artist": "The Weeknd", 
  "album": "After Hours",
  "album_cover": "https://i.scdn.co/image/ab67616d0000b273...",
  "spotify_preview_url": "https://p.scdn.co/mp3-preview/...",
  "spotify_id": "0VjIjW4GlULA42X6..."
}
```

## Troubleshooting

### "Spotify API not configured"
- Check that environment variables are set correctly
- Restart your backend after setting variables
- Verify credentials at [Spotify Dashboard](https://developer.spotify.com/dashboard)

### "No results found for track"
- Song titles need to match Spotify's database exactly
- Try different search terms or artist names
- Some songs might not be available on Spotify

### API Rate Limits
- Spotify allows 100 requests per minute for most endpoints
- The app caches results to minimize API calls

## Alternative: Manual Album Cover URLs

If you prefer not to use Spotify API, you can manually find album cover URLs:

1. **Search on Spotify Web Player**
2. **Right-click album cover → "Copy image address"**
3. **Use the URL directly in your backend:**

```python
"album_cover": "https://i.scdn.co/image/ab67616d0000b273..."
```

## Next Steps

Once Spotify integration is working:
- Add more songs to your playlist
- Use Spotify search to find new songs
- Consider integrating Spotify Web Playback SDK for actual streaming
