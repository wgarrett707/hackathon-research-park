# 🎵 Audio Playback Guide

Your music player now supports **real audio playback**! Here's how it works and how to customize it.

## How Audio Playback Works

### 1. **HTML5 Audio API**
The frontend uses the HTML5 `<audio>` element to play music files:
- Supports MP3, WAV, OGG, and other web-compatible formats
- Handles loading, playing, pausing, and seeking
- Provides real-time playback position updates

### 2. **Audio Service** (`frontend/src/services/audioService.ts`)
- Manages audio playback state
- Synchronizes with backend player state
- Handles audio events (play, pause, ended, error)
- Provides smooth seeking and volume control

### 3. **Integration Flow**
```
User clicks play → Frontend calls backend API → Backend updates state → 
Frontend loads audio file → HTML5 Audio plays music → Real-time sync
```

## Current Audio Sources

The app currently uses **free demo music** from SoundHelix:
- Song 1: `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3`
- Song 2: `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3`
- Song 3: `https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3`

## How to Add Your Own Music

### Option 1: Local Files (Simple)

1. **Add music files to the frontend:**
   ```
   frontend/public/music/
   ├── song1.mp3
   ├── song2.mp3
   └── song3.mp3
   ```

2. **Update the backend with local URLs:**
   ```python
   # In backend/src/api/get_song.py
   "audio_url": "/music/song1.mp3"  # Served by Vite dev server
   ```

### Option 2: Cloud Storage (Recommended)

1. **Upload to a cloud service:**
   - **AWS S3**: `https://your-bucket.s3.amazonaws.com/music/song.mp3`
   - **Google Cloud**: `https://storage.googleapis.com/your-bucket/song.mp3`
   - **Azure Blob**: `https://account.blob.core.windows.net/music/song.mp3`

2. **Update backend with cloud URLs:**
   ```python
   "audio_url": "https://your-bucket.s3.amazonaws.com/music/song.mp3"
   ```

### Option 3: Spotify API Integration

For a production app, integrate with Spotify Web Playback SDK:

1. **Register Spotify App**: Get Client ID from [Spotify Developer Dashboard](https://developer.spotify.com/)

2. **Install Spotify SDK**:
   ```bash
   npm install spotify-web-api-sdk
   ```

3. **Use Spotify Web Playback SDK** (requires Premium):
   ```typescript
   // Replace audioService with Spotify SDK
   const player = new Spotify.Player({
     name: 'Your Music Player',
     getOAuthToken: cb => { cb(token); }
   });
   ```

## Audio Format Support

### **Supported Formats:**
- ✅ **MP3** - Best compatibility, recommended
- ✅ **AAC/M4A** - Good quality, modern browsers
- ✅ **OGG** - Open source, Firefox/Chrome
- ✅ **WAV** - Uncompressed, large files

### **Not Supported:**
- ❌ **FLAC** - Limited browser support
- ❌ **WMA** - Microsoft proprietary
- ❌ **Protected AAC** - DRM protected

## Testing Audio Playback

1. **Start the servers:**
   ```bash
   # Terminal 1: Backend
   cd backend && python -m src.main

   # Terminal 2: Frontend  
   cd frontend && npm run dev
   ```

2. **Open the app**: Navigate to `http://localhost:5173`

3. **Test features:**
   - Click ▶️ **Play** - Should load and play audio
   - Click ⏸️ **Pause** - Should pause audio
   - Click ⏭️ **Next** - Should change song and play new audio
   - Drag **seek bar** - Should jump to new position
   - Check **browser console** for audio loading messages

## Troubleshooting Audio Issues

### **No Audio Playing:**
- Check browser console for errors
- Ensure audio URLs are accessible (try opening in browser)
- Some browsers require user interaction before playing audio

### **CORS Errors:**
- Make sure audio files are served with proper CORS headers
- Use same domain or configure CORS on your audio server

### **Autoplay Blocked:**
- Most browsers block autoplay without user interaction
- The app handles this by requiring a play button click

### **Loading Slowly:**
- Use smaller MP3 files (128kbps is usually sufficient)
- Consider using a CDN for faster loading
- Implement audio preloading for next/previous tracks

## Advanced Features You Can Add

### **Volume Control:**
```typescript
audioService.setVolume(0.5); // 50% volume
```

### **Playlist Management:**
```typescript
// Add shuffle, repeat modes
// Preload next track for seamless playback
```

### **Audio Visualization:**
```typescript
// Use Web Audio API for visualizations
const context = new AudioContext();
const analyser = context.createAnalyser();
```

### **Offline Support:**
```typescript
// Cache audio files using Service Workers
// Play cached music when offline
```

## Production Considerations

1. **Audio CDN**: Use a fast CDN for audio files
2. **Compression**: Optimize audio files for web (128-192 kbps MP3)
3. **Licensing**: Ensure you have rights to use the music
4. **Analytics**: Track play counts, skip rates, etc.
5. **Error Handling**: Graceful fallbacks for failed audio loads

Your music player now has real audio playback! 🎉
