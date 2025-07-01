# Music Player Integration Setup

This document explains how to integrate the backend and frontend for the music player application.

## Prerequisites

Make sure you have:
- Python 3.8+ installed
- Node.js 16+ installed
- npm or yarn package manager

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Start the backend server:
```bash
python src/main.py
```

The backend will be available at `http://localhost:8080`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

The backend provides the following endpoints:

### GET /player/status
Returns the current player state including:
- Current song information
- Play/pause state
- Current time
- Playlist

### POST /player/control
Controls music playback. Send a JSON payload with:
- `action`: "play", "pause", "next", "previous", or "seek"
- `position`: (optional) for seek action, position in seconds

Example:
```json
{
  "action": "play"
}
```

### POST /get_song (Legacy)
Returns current song information.

## Integration Features

The frontend now integrates with the backend to provide:

1. **Play/Pause Control**: Clicking the play button sends requests to the backend to control playback
2. **Track Navigation**: Previous/Next buttons change tracks through the backend
3. **Seek Control**: Dragging the progress bar updates the playback position
4. **Real-time Updates**: The UI reflects the current state from the backend
5. **Error Handling**: Shows user-friendly error messages when backend is unavailable

## Development Workflow

1. Start the backend server first (`python src/main.py` from backend directory)
2. Start the frontend development server (`npm run dev` from frontend directory)
3. Open `http://localhost:5173` in your browser
4. The frontend will automatically communicate with the backend on `http://localhost:8080`

## Adding New Features

### Backend
- Add new routes in `backend/src/api/get_song.py`
- Update the player state management logic
- Add new data models in `backend/src/models/models.py`

### Frontend
- Add new API functions in `frontend/src/services/api.ts`
- Update the UI components in `frontend/src/App.tsx`
- Handle new player states and actions

## Troubleshooting

- **CORS errors**: Make sure the backend CORS middleware includes your frontend URL
- **Connection refused**: Ensure the backend server is running on port 8080
- **API errors**: Check the browser console and backend logs for detailed error messages
