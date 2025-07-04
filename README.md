# 🌍🎵 SpotOn - Contextual Music Discovery

An intelligent music player that recommends songs based on your real-time location and time of day. Using advanced machine learning algorithms and geospatial analysis, SpotOn creates the perfect soundtrack for wherever you are and whatever you're doing.

## 🚀 What Makes SpotOn Special

### 🧠 Intelligent Location-Based Recommendations
- **Sophisticated Geospatial Analysis**: Uses coordinate chunking to determine if you're in urban, suburban, or rural areas
- **Time-Aware Logic**: Different moods for day vs. night listening
- **Audio Feature Mapping**: Dynamically adjusts music characteristics (energy, acousticness, tempo, valence) based on your environment
- **AI-Powered Discovery**: Integrates with Reccobeats API for ML-driven recommendations using audio features

### 🎯 Smart Music Matching
- **Urban Night**: Chill but sophisticated tracks with moderate energy and danceable beats
- **Rural Day**: Folk and country vibes with acoustic elements and pleasant moods  
- **Suburban Evening**: Relaxed and cozy atmosphere with balanced audio features
- **City Morning**: High-energy, upbeat tracks to power your day

### 🔄 Real-Time Adaptation
- **Fresh Location on Every Skip**: Always gets your current location for the most relevant recommendations
- **Fallback Logic**: Gracefully handles API failures with Spotify's native recommendation engine
- **Randomization**: Avoids repetitive suggestions while maintaining context-aware recommendations

## 🎵 Core Features

- **Location-Aware Playback**: Music automatically adapts to where you are
- **Time-Sensitive Recommendations**: Different vibes for different times of day
- **Spotify Integration**: Full playback control with your Spotify Premium account
- **Real-time Player**: Live updates of current track, position, and player state
- **Modern UI**: Spotify-inspired design with smooth animations and responsive layout
- **Error Resilience**: Robust fallback systems ensure music never stops

## 🏗️ Technical Architecture

### Backend (FastAPI + Python)
- **Advanced Geospatial Logic**: Coordinate chunking system to classify location types
- **Audio Feature Engine**: Sophisticated mapping of location/time to Spotify audio features
- **Reccobeats API Integration**: ML-powered track recommendations using audio characteristics
- **Spotify Web API**: Premium account integration for playback control
- **Async Architecture**: Non-blocking HTTP requests for optimal performance
- **Robust Error Handling**: Multiple fallback layers ensure reliable service

### Frontend (React + TypeScript + Vite)
- **Real-Time Location**: Browser geolocation API for precise positioning
- **Spotify Web Playback SDK**: Direct player control and state management
- **Material-UI Components**: Professional, accessible user interface
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **State Management**: React hooks for efficient player state synchronization

### Key Algorithms & APIs
- **Location Classification**: Converts GPS coordinates to urban/suburban/rural categories
- **Audio Feature Mapping**: Complex logic for mood-appropriate music characteristics
- **Reccobeats ML API**: Advanced recommendation engine using audio feature similarity
- **Nango Authentication**: Secure OAuth flow for Spotify integration

## 🎯 How It Works

1. **Location Detection**: Get user's real-time GPS coordinates
2. **Environment Analysis**: Classify location type (urban/suburban/rural) and time of day
3. **Audio Feature Generation**: Map environment to optimal music characteristics (energy, acousticness, etc.)
4. **AI Recommendation**: Query Reccobeats API with audio features for ML-powered suggestions
5. **Playback Control**: Start playing recommended tracks through Spotify
6. **Continuous Adaptation**: Fresh location and recommendations on every track skip

## 🧪 Advanced Features We Built

### Sophisticated Location Logic
```python
# Urban night: Chill but sophisticated
audio_features = {
    "energy": 0.4,          # Moderate energy
    "danceability": 0.6,    # Still danceable  
    "tempo": 0.4,           # Slower tempo
    "valence": 0.3,         # Slightly melancholic
    "acousticness": 0.3     # Some acoustic elements
}
```

### Reccobeats AI Integration
- Uses audio features instead of genre seeds for more nuanced recommendations
- Converts location/time context into 7 key audio characteristics
- Fallback to Spotify's native recommendation engine
- Randomization to prevent repetitive suggestions

### Real-Time Geolocation
- Browser geolocation API with high accuracy enabled
- Fresh coordinates on every track skip
- Coordinate chunking for location type classification
- Error handling for location access denial

## 🚀 Quick Start

### Prerequisites
- **Spotify Premium Account** (required for playback control)
- **Python 3.12+** with Miniconda/Anaconda
- **Node.js 18+** with npm
- **Browser with Geolocation Support**

### Option 1: Use the Convenience Scripts

**Windows Batch Scripts:**
```bash
# Start backend (in one terminal)
start-backend.bat

# Start frontend (in another terminal)  
start-frontend.bat
```

**PowerShell Scripts:**
```powershell
# Start backend (in one terminal)
.\start-backend.ps1

# Start frontend (in another terminal)
.\start-frontend.ps1
```

### Option 2: Manual Setup

### Backend Setup (FastAPI)

1. **Install [Miniconda/Anaconda](https://docs.conda.io/en/latest/miniconda.html) if you don't have it already.**
2. **Create and activate a new conda environment:**
   ```bash
   conda create -n hackathon-rp python=3.12 -y
   conda activate hackathon-rp
   ```
3. **Install backend dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. **Run the FastAPI server:**
   ```bash
   python -m src.main
   ```
   The backend API will be available at http://localhost:8080

### Frontend Setup (Vite + React)

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The app will be available at http://localhost:5173

## 🏆 Hackathon Achievements

### What We Built in 48 Hours
- **Advanced Geospatial Music Engine**: Location-aware recommendation system
- **ML-Powered Discovery**: Integration with Reccobeats API for audio feature-based recommendations  
- **Real-Time Adaptation**: Fresh location tracking on every song skip
- **Robust Fallback System**: Multiple layers ensuring music never stops playing
- **Full Spotify Integration**: Premium account playback control via Web API
- **Professional UI**: Spotify-inspired design with smooth animations

### Technical Challenges Solved
- **Complex Audio Feature Mapping**: Sophisticated algorithm to convert location/time into music characteristics
- **Async API Integration**: Non-blocking requests to multiple external APIs
- **Cross-Platform Compatibility**: Works seamlessly across devices and browsers
- **Error Resilience**: Graceful degradation when services are unavailable
- **Real-Time State Sync**: Player state updates across frontend and backend

### Innovation Highlights
- **Context-Aware AI**: First music app to use both geographic location AND time of day for ML recommendations
- **Coordinate Chunking**: Novel approach to classify urban/suburban/rural environments from GPS data
- **Multi-API Architecture**: Intelligent switching between Reccobeats AI and Spotify recommendations
- **Location Privacy**: Processes coordinates locally without storing personal location data

## 🔗 API Integration & Testing

The frontend communicates with the backend through these key endpoints:

- **POST /get_songs_recs** - Location-based song recommendations (our main innovation!)
- **GET /player/status** - Get current player state
- **POST /player/control** - Control playback (play/pause/next/previous/seek)
- **GET /debug/spotify** - Debug Spotify connection and user info

### Live Demo Endpoints
- **Frontend**: http://localhost:5173 - React app with location-aware music player
- **Backend**: http://localhost:8080 - FastAPI server with ML recommendation engine
- **API Docs**: http://localhost:8080/docs - Interactive Swagger documentation

### Testing the Integration

Run the integration test to verify everything works:
```bash
python test_integration.py
```

This will test all API endpoints and provide feedback on the integration status.

### Try It Out!
1. **Start the servers** using the quick start scripts above
2. **Open http://localhost:5173** in your browser
3. **Allow location access** when prompted
4. **Connect your Spotify Premium account**
5. **Hit the skip button** and watch as music adapts to your location and time!

## 🎯 Demo Scenarios

### Urban Explorer
- Walk around downtown → Get energetic, city-appropriate tracks
- Sit in a café at night → Receive chill, sophisticated background music

### Suburban Commuter  
- Morning drive → Upbeat tracks to start your day
- Evening relaxation → Balanced, pleasant background music

### Nature Lover
- Hiking in rural areas → Folk and acoustic tracks with natural vibes
- Stargazing at night → Peaceful, introspective instrumental music

## 🛠️ Development & Architecture

### Project Structure
```
├── backend/                          # FastAPI backend
│   ├── src/
│   │   ├── api/
│   │   │   └── get_song.py          # 🎯 Location-based recommendation API
│   │   ├── models/
│   │   │   └── models.py            # 📍 LocationPoint, LocationChunk classes
│   │   ├── utils/
│   │   │   ├── spotify.py           # 🧠 Sophisticated location logic
│   │   │   └── spotify_auth.py      # 🔐 Spotify authentication
│   │   └── main.py                  # 🚀 Application entry point
│   └── requirements.txt             # 📦 Python dependencies (aiohttp, fastapi, etc.)
├── frontend/                        # React frontend
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts              # 🌐 API client functions
│   │   ├── routes/
│   │   │   └── index.tsx           # 🎵 Main music player UI
│   │   └── App.tsx                 # 📱 Location tracking & player control
│   └── package.json                # 📦 Node.js dependencies
└── README.md                       # 📖 This comprehensive guide
```

### Key Innovation Files
- **`spotify.py`**: Coordinate chunking + audio feature mapping algorithm
- **`get_song.py`**: Reccobeats API integration + fallback logic  
- **`App.tsx`**: Real-time location tracking + player state management

### Adding New Features

1. **Backend**: Add new routes in `backend/src/api/get_song.py`
2. **Frontend**: Add API functions in `frontend/src/services/api.ts`
3. **UI**: Update components in `frontend/src/App.tsx`
4. **Location Logic**: Enhance algorithms in `backend/src/utils/spotify.py`

### Future Enhancements
- **Weather Integration**: Factor in weather conditions for mood-based recommendations
- **Activity Detection**: Use accelerometer data to detect walking, driving, sitting
- **Social Features**: Share location-based playlists with friends
- **Machine Learning**: Train custom models on user listening patterns
- **Offline Mode**: Cache recommendations for areas with poor connectivity

## 🌟 Why This Project Stands Out

### 🧪 Technical Innovation
- **First-of-its-kind**: Combines real-time geolocation with AI music recommendations
- **Sophisticated Logic**: Not just genre-based, but audio feature-driven recommendations
- **Multi-API Architecture**: Intelligent fallback between Reccobeats AI and Spotify
- **Real-Time Processing**: Sub-second response times for location-based recommendations

### 🎯 User Experience Excellence
- **Seamless Integration**: Works with existing Spotify Premium accounts
- **Privacy-First**: Location data processed locally, never stored
- **Responsive Design**: Beautiful UI that works on any device
- **Error Resilience**: Music never stops playing, even if services fail

### 🏗️ Production-Ready Features
- **Comprehensive Error Handling**: Graceful degradation at every level
- **Async Architecture**: Non-blocking operations for optimal performance  
- **Detailed Logging**: Debug information for troubleshooting and monitoring
- **Modular Design**: Easy to extend with new features and integrations

## � Troubleshooting

### Common Issues & Solutions

**🔗 Connection refused**: Ensure backend is running on port 8080
```bash
# Check if backend is running
curl http://localhost:8080/health
```

**📍 Location access denied**: Enable location permissions in your browser
- Chrome: Settings → Privacy and security → Site Settings → Location
- Firefox: about:preferences#privacy → Permissions → Location

**🎵 Spotify Premium required**: This app requires Spotify Premium for playback control
- Free accounts can view recommendations but cannot control playback

**🌐 CORS errors**: Backend includes CORS middleware for development
**📦 Module import errors**: Always run backend with `python -m src.main` from backend directory

### Debug Mode
Enable detailed logging by checking the browser console and backend terminal output:
- **Frontend**: Open DevTools → Console for location and API request logs
- **Backend**: Terminal shows Reccobeats API calls, location analysis, and errors

## 📚 Resources & Documentation

- **[Reccobeats API Docs](https://api.reccobeats.com/docs)** - ML-powered music recommendation engine
- **[Spotify Web API](https://developer.spotify.com/documentation/web-api/)** - Playback control and user data
- **[Frontend README](frontend/README.md)** - Detailed React app documentation

---

**🏆 Built with ❤️ at Research Park Hackathon 2025**

*SpotOn represents the future of context-aware music discovery, combining cutting-edge location intelligence with AI-powered recommendations to create the perfect soundtrack for your life.*