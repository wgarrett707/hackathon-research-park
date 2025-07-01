# hackathon-research-park

A full-stack music player application with React frontend and FastAPI backend integration.

## 🎵 Features

- **Play/Pause Control**: Start and stop music playback
- **Track Navigation**: Skip to next/previous tracks
- **Seek Control**: Jump to any position in the current track
- **Real-time Updates**: UI reflects backend state changes
- **Modern UI**: Spotify-inspired design with smooth animations
- **Error Handling**: User-friendly error messages for connection issues

## 🚀 Quick Start

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

## 🔗 API Integration

The frontend communicates with the backend through these endpoints:

- **GET /player/status** - Get current player state
- **POST /player/control** - Control playback (play/pause/next/previous/seek)
- **POST /get_song** - Get current song (legacy endpoint)

### Testing the Integration

Run the integration test to verify everything works:
```bash
python test_integration.py
```

This will test all API endpoints and provide feedback on the integration status.

## 🛠️ Development

### Project Structure
```
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes
│   │   ├── models/         # Data models
│   │   ├── utils/          # Utility functions
│   │   └── main.py         # Application entry point
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── services/       # API client functions
│   │   ├── routes/         # React Router pages
│   │   └── App.tsx         # Main component
│   └── package.json        # Node.js dependencies
└── INTEGRATION_GUIDE.md    # Detailed integration docs
```

### Adding New Features

1. **Backend**: Add new routes in `backend/src/api/get_song.py`
2. **Frontend**: Add API functions in `frontend/src/services/api.ts`
3. **UI**: Update components in `frontend/src/App.tsx`

## 📚 Documentation

- [Integration Guide](INTEGRATION_GUIDE.md) - Detailed setup and integration instructions
- [Frontend README](frontend/README.md) - Frontend-specific documentation

## 🐛 Troubleshooting

- **Connection refused**: Ensure backend is running on port 8080
- **CORS errors**: Backend includes CORS middleware for development
- **Module import errors**: Run backend with `python -m src.main` from backend directory

---

For more details on frontend configuration, see `frontend/README.md`.