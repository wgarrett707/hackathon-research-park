# SpotOn - Spotify Integration Running Instructions

## Quick Start

### 1. Start the Backend (Terminal 1)
```powershell
cd "c:\Users\Owner\hackathon\hackathon-research-park\backend"
# Activate your virtual environment
.\venv\Scripts\Activate.ps1
# Install dependencies if needed
pip install -r requirements.txt
# Start the FastAPI server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend (Terminal 2)
```powershell
cd "c:\Users\Owner\hackathon\hackathon-research-park\frontend"
# Install dependencies if needed
npm install
# Start the development server
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

## Spotify Setup Requirements

Before using the app, make sure you have:

1. **Spotify Premium Account** - Required for playback control
2. **Spotify App Open** - The app controls your existing Spotify session
3. **Spotify Developer App** - Set up at https://developer.spotify.com/dashboard
4. **Environment Variables** - Configure in backend/.env:
   ```
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:8000/callback
   ```

## Features

### Current Working Features
- ✅ Real Spotify playback control (play/pause/skip/seek)
- ✅ Live album covers and song metadata from Spotify
- ✅ Real-time progress tracking
- ✅ Device detection and control
- ✅ Modern animated UI with responsive design
- ✅ Explore and Repeat button UI (visual only)
- ✅ Scrolling banner animation
- ✅ Mobile-responsive layout

### UI Features from Main Branch
- ✅ Animated "SpotOn is..." text cycling
- ✅ Gradient background effects
- ✅ Enhanced header with search and profile
- ✅ Responsive design (mobile/desktop layouts)
- ✅ Scrolling text banner at bottom
- ✅ Professional Spotify-inspired styling

## How It Works

1. **Backend** (FastAPI):
   - Handles Spotify OAuth authentication
   - Communicates with Spotify Web API
   - Provides REST endpoints for frontend
   - Controls real Spotify playback

2. **Frontend** (React + Vite):
   - Polls backend every 2 seconds for current song state
   - Displays live album covers and track info
   - Sends control commands to backend
   - Beautiful, responsive UI with animations

## Troubleshooting

### Backend Issues
- Make sure Python dependencies are installed: `pip install -r requirements.txt`
- Check that Spotify credentials are correct in .env file
- Ensure Spotify app is open and playing music

### Frontend Issues
- Make sure Node dependencies are installed: `npm install`
- Check that backend is running on port 8000
- Verify CORS is properly configured in backend

### Spotify Integration Issues
- Ensure you have Spotify Premium (required for playback control)
- Check that redirect URI matches in Spotify Developer Console
- Make sure an active device is available in Spotify

## File Structure

```
hackathon-research-park/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/get_song.py      # Spotify API endpoints
│   │   └── utils/spotify_service.py  # Spotify integration
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.tsx              # Main React component (merged)
    │   └── services/api.ts      # API service layer
    └── package.json
```

## Next Steps

1. Test all features to ensure they work correctly
2. Add error handling for device selection
3. Implement actual functionality for Explore/Repeat buttons
4. Add more sophisticated music recommendation features
5. Enhance mobile user experience
