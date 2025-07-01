import { useState, useEffect } from 'react';
import './index.css';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { getPlayerStatus, playMusic, pauseMusic, nextTrack, previousTrack, seekToPosition } from './services/api';
import type { PlayerState } from './services/api';

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function App() {
  const [playerState, setPlayerState] = useState<PlayerState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Poll for player status updates every 2 seconds
  useEffect(() => {
    const fetchPlayerState = async () => {
      try {
        const state = await getPlayerStatus();
        setPlayerState(state);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch player state:', err);
        setError('Failed to connect to backend. Make sure the backend server is running on port 8000.');
      }
    };

    // Initial fetch
    fetchPlayerState();

    // Poll every 2 seconds
    const interval = setInterval(fetchPlayerState, 2000);

    return () => clearInterval(interval);
  }, []);

  const handlePlayPause = async () => {
    try {
      setIsLoading(true);
      let newState;
      if (playerState?.is_playing) {
        newState = await pauseMusic();
      } else {
        newState = await playMusic();
      }
      setPlayerState(newState);
      setError(null);
    } catch (err) {
      console.error('Failed to control playback:', err);
      setError('Failed to control playback');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNext = async () => {
    try {
      setIsLoading(true);
      const newState = await nextTrack();
      setPlayerState(newState);
      setError(null);
    } catch (err) {
      console.error('Failed to skip to next track:', err);
      setError('Failed to skip track');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePrevious = async () => {
    try {
      setIsLoading(true);
      const newState = await previousTrack();
      setPlayerState(newState);
      setError(null);
    } catch (err) {
      console.error('Failed to skip to previous track:', err);
      setError('Failed to skip track');
    } finally {
      setIsLoading(false);
    }
  };

  const handleScrub = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const newTime = Number(e.target.value);
    
    try {
      setIsLoading(true);
      const newState = await seekToPosition(newTime);
      setPlayerState(newState);
      setError(null);
    } catch (err) {
      console.error('Failed to seek:', err);
      setError('Failed to seek');
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading state if player state hasn't loaded yet
  if (!playerState) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-black text-white">
        {error ? (
          <div className="text-center">
            <div className="text-red-500 mb-4">{error}</div>
            <button 
              onClick={() => window.location.reload()} 
              className="px-4 py-2 bg-green-500 rounded text-black"
            >
              Retry
            </button>
          </div>
        ) : (
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-white mx-auto mb-4"></div>
            <div>Loading music player...</div>
          </div>
        )}
      </div>
    );
  }

  // Show message if no song is currently playing
  if (!playerState.current_song) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-black text-white">
        <div className="text-center">
          <div className="text-2xl mb-4">🎵</div>
          <div className="text-lg mb-2">No song is currently playing</div>
          <div className="text-gray-400 mb-4">Start playing something on Spotify to control it here</div>
          {error && (
            <div className="text-red-500 mb-4">{error}</div>
          )}
          <button 
            onClick={() => window.location.reload()} 
            className="px-4 py-2 bg-green-500 rounded text-black"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  const currentTime = playerState.current_time || 0;
  const duration = playerState.duration || 0;

  return (
    <div> 
      <div className="wrapper">
        <div className="gradient gradient-1"></div>
        <div className="gradient gradient-2"></div>
        <div className="gradient gradient-3"></div>
      </div>
      
      <div className="w-screen h-screen min-h-screen min-w-full flex items-center justify-center relative">
        {/* Header */}
        <div className="absolute top-0 left-0 right-0 flex justify-between items-center p-4 z-10">
          <div className="flex items-center gap-3">
            <img
              src="/images/spotify-logo.png"
              alt="Spotify"
              className="h-8 w-auto"
            />
            <button
              className="w-8 h-8 rounded-full flex items-center justify-center bg-gray-700 hover:bg-gray-600 transition-colors"
              style={{ 
                backgroundColor: '#282828',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label="Home"
            >
              <HomeIcon sx={{ fontSize: 20, color: 'white' }} />
            </button>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="relative">
              <input
                type="text"
                placeholder="Search..."
                className="w-64 h-8 px-3 pr-10 rounded-full bg-gray-700 text-white placeholder-gray-400 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                style={{ backgroundColor: '#282828' }}
              />
              <SearchIcon 
                sx={{ 
                  fontSize: 18, 
                  color: '#9CA3AF',
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)'
                }} 
              />
            </div>
            
            <button
              className="w-8 h-8 rounded-full flex items-center justify-center bg-gray-700 hover:bg-gray-600 transition-colors"
              style={{ 
                backgroundColor: '#282828',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label="Notifications"
            >
              <NotificationsIcon sx={{ fontSize: 20, color: 'white' }} />
            </button>
            
            <button
              className="w-8 h-8 rounded-full flex items-center justify-center text-black font-semibold text-sm"
              style={{ 
                backgroundColor: 'rgb(25, 230, 140)',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label="Profile"
            >
              W
            </button>
          </div>
        </div>
        
        <div className="w-full max-w-sm rounded-xl shadow-lg bg-[#282828] p-6 flex flex-col items-center mx-4">
          {error && (
            <div className="w-full mb-4 p-2 bg-red-900 text-red-200 rounded text-sm text-center">
              {error}
            </div>
          )}
          {isLoading && (
            <div className="w-full mb-4 p-2 bg-blue-900 text-blue-200 rounded text-sm text-center flex items-center justify-center">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-200 mr-2"></div>
              Loading audio...
            </div>
          )}
          <img
            src={playerState.current_song.album_cover}
            alt="Album Cover"
            className="w-40 h-40 rounded-lg mb-4 shadow-md object-cover"
          />
          <div className="text-white text-lg font-semibold text-center mb-1">
            {playerState.current_song.title}
          </div>
          <div className="text-gray-400 text-sm text-center mb-4">{playerState.current_song.artist}</div>
          <div className="w-full flex items-center gap-2 mb-4">
            <span className="text-xs text-gray-400 w-8 text-right">
              {formatTime(currentTime)}
            </span>
            <input
              type="range"
              min={0}
              max={duration}
              value={currentTime}
              onChange={handleScrub}
              className="flex-1 accent-green-500 h-1 rounded-lg"
              disabled={isLoading}
            />
            <span className="text-xs text-gray-400 w-8 text-left">
              {formatTime(duration)}
            </span>
          </div>
          <div className="flex items-center justify-center gap-4 mb-4">
            <button
              onClick={handlePrevious}
              disabled={isLoading}
              className="w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#282828' }}
              aria-label="Previous"
            >
              <SkipPreviousIcon sx={{ fontSize: 28, color: 'white' }} />
            </button>
            <button
              onClick={handlePlayPause}
              disabled={isLoading}
              className="w-16 h-16 flex items-center justify-center rounded-full bg-white hover:bg-gray-100 transition-colors shadow-lg focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ 
                backgroundColor: 'white',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label={playerState.is_playing ? 'Pause' : 'Play'}
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-600"></div>
              ) : playerState.is_playing ? (
                <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="10" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                  <rect x="24" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                </svg>
              ) : (
                <PlayArrowIcon sx={{ fontSize: 32, color: '#4B5563' }} />
              )}
            </button>
            <button
              onClick={handleNext}
              disabled={isLoading}
              className="w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              style={{ backgroundColor: '#282828' }}
              aria-label="Next"
            >
              <SkipNextIcon sx={{ fontSize: 28, color: 'white' }} />
            </button>
          </div>
          <div className="mt-8 text-gray-500 text-xs text-center">
            SpotOn &mdash; Inspired by Spotify
            {playerState.is_playing && <div className="mt-1 text-green-400">🎵 Playing on Spotify</div>}
            {playerState.device && <div className="mt-1 text-blue-400">📱 {playerState.device}</div>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
