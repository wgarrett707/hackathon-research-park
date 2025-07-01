# SpotOn - Spotify Music Player with Nango Authentication

A modern music player that integrates with Spotify using Nango-based OAuth for seamless authentication and playback control.

## 🚀 Features

- **Nango-powered Spotify Authentication**: Secure OAuth flow without exposing Spotify credentials
- **Real-time Playback Control**: Play, pause, skip, seek through tracks
- **Live Status Updates**: Real-time display of currently playing song, artist, album, and position
- **Modern UI**: Beautiful, responsive interface inspired by Spotify's design
- **Cross-device Control**: Control any active Spotify device from the web interface

## 📋 Prerequisites

- **Python 3.8+** with `pip` and `venv`
- **Node.js 16+** with `npm`
- **Nango Account**: Sign up at [nango.dev](https://nango.dev)
- **Spotify Developer Account**: Register at [developer.spotify.com](https://developer.spotify.com)

## 🛠️ Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <your-repo-url>
cd hackathon-research-park
```

### 2. Environment Configuration

Create a `.env` file in the root directory:
```env
# Nango Configuration
NANGO_SECRET_KEY=your_nango_secret_key_here

# Optional: For development/debugging
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

**Important**: Get your `NANGO_SECRET_KEY` from your Nango dashboard after setting up the Spotify integration.

### 3. Install Dependencies

Run the VS Code task `Install Dependencies` or manually:

**Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Frontend:**
```powershell
cd frontend
npm install
```

### 4. Nango Setup

1. Create a Nango account at [nango.dev](https://nango.dev)
2. Set up a Spotify integration in your Nango dashboard
3. Configure your Spotify app credentials in Nango
4. Copy your Nango secret key to the `.env` file

## 🎵 Running the Application

### Quick Start (VS Code Task)
Use the VS Code task `Start Full Stack App` which will start both servers automatically.

### Manual Start

**Start Backend (Terminal 1):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
```

**Start Frontend (Terminal 2):**
```powershell
cd frontend
npm run dev
```

## 🔧 Usage

1. **Open the Application**: Navigate to `http://localhost:5173` (or the port shown by Vite)

2. **Authenticate with Spotify**: 
   - Click the profile button (W) in the top-right corner
   - Complete the Nango/Spotify OAuth flow
   - Grant necessary permissions (playback control, read currently playing)

3. **Control Playback**:
   - Start playing music on any Spotify device
   - Use the web interface to control playback
   - View real-time status updates

## 🏗️ Architecture

### Backend (FastAPI + Python)
- **`src/main.py`**: Application entry point and FastAPI configuration
- **`src/api/get_song.py`**: Spotify playback control endpoints
- **`src/api/auth.py`**: Nango authentication endpoints  
- **`src/utils/spotify_service.py`**: Spotify API integration with Nango

### Frontend (React + TypeScript + Vite)
- **`src/App.tsx`**: Main application component with Spotify controls
- **`src/services/api.ts`**: Backend API integration with Nango connection handling

### Key API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/player/status` | GET | Get current playback state |
| `/player/control` | POST | Control playback (play/pause/next/previous/seek) |
| `/spotify-status` | GET | Check Spotify/Nango connection status |
| `/auth/nango-session-token` | GET | Get Nango session token for frontend |

## 🔐 Authentication Flow

1. Frontend requests Nango session token from backend
2. Frontend initializes Nango SDK with session token
3. User completes Spotify OAuth via Nango
4. Frontend receives connection ID from Nango
5. All subsequent API calls include the connection ID in `X-Connection-Id` header
6. Backend uses connection ID to fetch fresh Spotify tokens from Nango

## 🐛 Troubleshooting

### "Spotify API not available" Error
- Ensure you've completed the Nango/Spotify authentication
- Check that your `NANGO_SECRET_KEY` is correctly set
- Verify the Nango connection ID is being sent in requests

### Backend Won't Start
- Activate the Python virtual environment: `.\venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`
- Check that port 8080 is not in use

### Frontend Build Errors
- Ensure Node.js 16+ is installed
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that `@nangohq/frontend` and `cuid` are installed

### Playback Not Working
- Ensure you have an active Spotify Premium account
- Start playing music on any Spotify device first
- Check that the app has the necessary Spotify permissions

## 📝 Development Notes

- The app uses Nango instead of direct Spotify OAuth for better security and token management
- All backend endpoints are async and support automatic token refresh via Nango
- The frontend automatically includes the Nango connection ID in all API requests
- Real-time status updates poll the backend every 2 seconds

## 🎯 Next Steps

- [ ] Add playlist management
- [ ] Implement music recommendations based on location
- [ ] Add volume control
- [ ] Support for multiple device selection
- [ ] Enhanced error handling and user feedback

## 📄 License

This project is for educational/hackathon purposes. Spotify integration requires compliance with Spotify's Terms of Service and Developer Terms.
