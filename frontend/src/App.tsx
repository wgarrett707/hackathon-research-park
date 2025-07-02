import { useState, useEffect, useRef } from 'react';
import './index.css';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Nango from '@nangohq/frontend';
import cuid from 'cuid';

import ExploreIcon from '@mui/icons-material/Explore';
import RepeatIcon from '@mui/icons-material/Repeat';
import { getPlayerStatus, playMusic, pauseMusic, nextTrack, previousTrack, seekToPosition, setConnectionId as setApiConnectionId } from './services/api';
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
  const [isExploreActive, setIsExploreActive] = useState(false);
  const [isRepeatActive, setIsRepeatActive] = useState(false);
  const [textIndex, setTextIndex] = useState(0);
  const [pausePolling, setPausePolling] = useState(false);

  const user_id = cuid() // Convert to constant since we don't need to update it
  const [sessionToken, setSessionToken] = useState<string | null>(null)
  const [connectionId, setConnectionId] = useState<string | null>(null)


  const intervalRef = useRef<number | null>(null);

  const signInSpotify = async () => {
    try {
      const sessionToken = await fetch(`http://127.0.0.1:8080/auth/nango-session-token?user_id=${user_id}`)
      const sessionTokenJson = await sessionToken.json()
      console.log(sessionTokenJson)
      setSessionToken(sessionTokenJson)
      const nango = new Nango({ connectSessionToken: sessionTokenJson})
      
      const res = await nango.auth("spotify")
      console.log(res)
      
      // Set the connection ID in both local state and API service
      setConnectionId(res.connectionId)  // Local state
      setApiConnectionId(res.connectionId)  // API service
    } catch (err) {
      console.error("Error fetching session token")
      console.error(err)
    }
    
  }

  const handleLogout = async () => {
    try {
      // Call backend to revoke the Nango connection
      if (connectionId) {
        await fetch(`http://127.0.0.1:8080/auth/logout?connection_id=${connectionId}`, {
          method: 'POST'
        })
      }
      
      // Clear local state
      setConnectionId(null)
      setApiConnectionId(null)
      setSessionToken(null)
      setPlayerState(null)
      setError(null)
      
      console.log('User logged out successfully')
    } catch (err) {
      console.error('Error during logout:', err)
      // Still clear local state even if backend call fails
      setConnectionId(null)
      setApiConnectionId(null)
      setSessionToken(null)
      setPlayerState(null)
      setError(null)
    }
  }

  const phrases = ["is here.", "is enabled.", "is on.", "is ready.", "is live."];

  // Poll for player status updates every 2 seconds - only when authenticated
  useEffect(() => {
    // Only fetch player state if we have a connection ID (user is authenticated)
    if (!connectionId || pausePolling) {
      return;
    }

    const fetchPlayerState = async () => {
      try {
        const state = await getPlayerStatus();
        setPlayerState(state);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch player state:', err);
        setError('Failed to connect to backend. Make sure the backend server is running on port 8080.');
      }
    };

    // Initial fetch
    fetchPlayerState();

    // Poll every 2 seconds
    const interval = setInterval(fetchPlayerState, 2000);

    return () => clearInterval(interval);
  }, [connectionId, pausePolling]); // Depend on connectionId and pausePolling

  // Animated text cycling effect
  useEffect(() => {
    const textInterval = setInterval(() => {
      setTextIndex((prev) => (prev + 1) % phrases.length);
    }, 2000);

    return () => clearInterval(textInterval);
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

  const handleExploreToggle = () => {
    setIsExploreActive(!isExploreActive);
  };

  const handleRepeatToggle = () => {
    setIsRepeatActive(!isRepeatActive);
  };

  const getCurrentLocation = (): Promise<{ latitude: number; longitude: number }> => {
    console.log('🗺️ Getting current location...');
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        console.error('❌ Geolocation is not supported by this browser.');
        reject(new Error('Geolocation is not supported by this browser.'));
        return;
      }

      console.log('🔍 Requesting geolocation permission...');
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const coords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          console.log('✅ Location obtained:', coords);
          resolve(coords);
        },
        (error) => {
          console.error('❌ Geolocation error:', error);
          console.error('Error code:', error.code);
          console.error('Error message:', error.message);
          reject(error);
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 60000 // Cache for 1 minute
        }
      );
    });
  };

  const handleSkipWithLocation = async (direction: 'next' | 'previous') => {
    console.log(`🎵 handleSkipWithLocation called with direction: ${direction}`);
    try {
      setIsLoading(true);
      // Temporarily pause polling to avoid conflicts during location-based skips
      setPausePolling(true);
      console.log('⏸️ Polling paused for location-based skip');
      
      // Always get fresh location for each request
      console.log('🗺️ Getting fresh location...');
      const location = await getCurrentLocation();
      console.log(`✅ ${direction} button clicked with fresh coordinates:`, location);
      
      // Get new location-based recommendations for both directions
      console.log('📡 Sending request to backend...');
      const response = await fetch('http://127.0.0.1:8080/get_songs_recs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Connection-ID': connectionId || ''
        },
        body: JSON.stringify(location)
      });
      
      console.log('📥 Backend response status:', response.status);
      
      if (response.ok) {
        const result = await response.json();
        console.log(`✅ Location-based recommendations for ${direction}:`, result);
        
        // Update player state with the new song
        if (result.current_song) {
          console.log('🎵 Updating player state with new song:', result.current_song.title);
          setPlayerState(result);
        } else {
          console.warn('⚠️ No current_song in backend response');
        }
        
        // Wait a bit longer for the new song to start playing properly
        // This prevents the UI from showing 0:00 while the track is loading
        console.log('⏳ Waiting 3 seconds for track to start...');
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        // Force a fresh player state update after the delay
        try {
          console.log('🔄 Getting fresh player state after delay...');
          const freshState = await getPlayerStatus();
          console.log('✅ Fresh player state after location skip:', freshState);
          setPlayerState(freshState);
        } catch (err) {
          console.warn('❌ Failed to get fresh player state after skip:', err);
        }
        
        setError(null);
      } else {
        const errorText = await response.text();
        console.error('❌ Failed to get location recommendations. Status:', response.status);
        console.error('❌ Error response:', errorText);
        setError('Failed to get location-based recommendations');
        
        // Fallback to regular skip if location-based fails
        console.log('🔄 Falling back to regular skip...');
        if (direction === 'next') {
          await handleNext();
        } else {
          await handlePrevious();
        }
      }
      
    } catch (error) {
      console.error('❌ Error in handleSkipWithLocation:', error);
      setError('Failed to get your location or recommendations');
      
      // Fallback to regular skip if location fails
      console.log('🔄 Falling back to regular skip due to error...');
      if (direction === 'next') {
        await handleNext();
      } else {
        await handlePrevious();
      }
    } finally {
      setIsLoading(false);
      // Resume polling after location-based skip is complete
      setPausePolling(false);
      console.log('▶️ Polling resumed after location-based skip');
    }
  };

  // Show authentication screen if not logged in
  if (!connectionId) {
    return (
      <div className="w-screen h-screen flex items-center justify-center bg-black text-white">
        <div className="text-center">
          <div className="text-2xl mb-4">🎵 SpotOn</div>
          <div className="text-lg mb-2">Connect to Spotify</div>
          <div className="text-gray-400 mb-6">Sign in with your Spotify account to control playback</div>
          
          <button 
            onClick={signInSpotify}
            className="px-6 py-3 bg-green-500 rounded-full text-black font-semibold hover:bg-green-400 transition-colors cursor-pointer"
            style={{
              backgroundColor: '#22c55e',
              color: '#000000',
              padding: '12px 24px',
              borderRadius: '9999px',
              border: 'none',
              fontWeight: '600',
              fontSize: '16px',
              cursor: 'pointer',
              display: 'inline-block'
            }}
          >
            🎵 Sign in with Spotify
          </button>
          
          {error && (
            <div className="text-red-500 mt-4">{error}</div>
          )}
        </div>
      </div>
    );
  }

  // Show loading state if player state hasn't loaded yet (only after authentication)
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

  // Show message if no song is currently playing (only after authentication)
  if (!playerState?.current_song) {
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
    <div className="w-full h-full min-h-screen bg-black">
      <div className="wrapper">
        <div className="gradient gradient-1"></div>
        <div className="gradient gradient-2"></div>
        <div className="gradient gradient-3"></div>
      </div>
      
      <div className="w-full h-screen flex items-center justify-center relative">
        {/* Header */}
        <div className="absolute top-0 left-0 right-0 flex justify-between items-center p-3 lg:p-6 z-10">
          <div className="flex items-center gap-2 lg:gap-4">
            <img
              src="/images/spotify-logo.png"
              alt="Spotify"
              className="h-8 lg:h-12 w-auto"
            />
            <button
              className="w-8 h-8 lg:w-12 lg:h-12 flex items-center justify-center bg-gray-700 hover:bg-gray-600 transition-colors"
              style={{ 
                backgroundColor: '#282828',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label="Home"
            >
              <HomeIcon sx={{ fontSize: { xs: 18, lg: 24 }, color: 'white' }} />
            </button>
          </div>
          
          <div className="flex items-center gap-2 lg:gap-4">
            <div className="relative hidden sm:block">
              <input
                type="text"
                placeholder="Search..."
                className="w-48 lg:w-80 h-8 lg:h-12 px-3 lg:px-4 pr-10 lg:pr-12 rounded-full bg-gray-700 text-white placeholder-gray-400 text-sm lg:text-base focus:outline-none focus:ring-2 focus:ring-green-500"
                style={{ backgroundColor: '#282828' }}
              />
              <SearchIcon 
                sx={{ 
                  fontSize: { xs: 16, lg: 22 }, 
                  color: '#9CA3AF',
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)'
                }} 
              />
            </div>
            
            <button
              className="w-8 h-8 lg:w-12 lg:h-12 flex items-center justify-center bg-gray-700 hover:bg-gray-600 transition-colors"
              style={{ 
                backgroundColor: '#282828',
                borderRadius: '50%',
                border: 'none',
                padding: 0
              }}
              aria-label="Notifications"
            >
              <NotificationsIcon sx={{ fontSize: { xs: 18, lg: 24 }, color: 'white' }} />
            </button>
            
            {/* Logout Button */}
            <button
              onClick={handleLogout}
              className="px-3 py-1 lg:px-4 lg:py-2 bg-red-600 hover:bg-red-500 transition-colors rounded-full text-white text-xs lg:text-sm font-medium"
              style={{ 
                backgroundColor: '#dc2626',
                border: 'none'
              }}
              aria-label="Sign Out"
            >
              Sign Out
            </button>
          </div>
        </div>
        
        <div className="flex flex-col lg:flex-row items-center justify-center w-full px-4 h-full">
          {/* Animated Text - Hidden on mobile, shown on desktop */}
          <div className="hidden lg:flex flex-col items-start justify-center lg:w-1/2 lg:pr-8 lg:ml-8">
            <div className="text-white text-7xl font-bold text-left flex items-baseline">
              <span className="mr-3">SpotOn </span>
              <span className="inline-block overflow-hidden h-20 flex items-center">
                <div 
                  className="transition-transform duration-500 ease-in-out"
                  style={{ transform: `translateY(-${textIndex * 80}px)` }}
                >
                  {phrases.map((phrase, index) => (
                    <div key={index} className="h-20 flex items-center">
                      {phrase}
                    </div>
                  ))}
                </div>
              </span>
            </div>
            <div className="text-white text-2xl mt-12 ml-8 space-y-4">
              <div className="flex items-start">
                <span className="mr-4 text-green-400">•</span>
                <span>plays music based on surroundings</span>
              </div>
              <div className="flex items-start">
                <span className="mr-4 text-green-400">•</span>
                <span>adapts automatically to your location</span>
              </div>
              <div className="flex items-start">
                <span className="mr-4 text-green-400">•</span>
                <span>urban, rural, day, night, and more</span>
              </div>
            </div>
          </div>
          
          <div className="w-full max-w-xs lg:max-w-sm rounded-xl shadow-2xl lg:shadow-lg bg-[#282828] p-4 lg:p-6 flex flex-col items-center">
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
              className="w-32 h-32 lg:w-40 lg:h-40 rounded-lg mb-3 lg:mb-4 shadow-md object-cover"
            />
            <div className="text-white text-base lg:text-lg font-semibold text-center mb-1">
              {playerState.current_song.title}
            </div>
            <div className="text-gray-400 text-xs lg:text-sm text-center mb-3 lg:mb-4">
              {playerState.current_song.artist}
            </div>
            <div className="w-full flex items-center gap-2 mb-3 lg:mb-4">
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
            <div className="flex items-center justify-center gap-3 lg:gap-4 mb-3 lg:mb-4">
              <button
                onClick={handleExploreToggle}
                disabled={isLoading}
                className="control-button w-10 h-10 lg:w-12 lg:h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ backgroundColor: '#282828' }}
                aria-label="Explore"
              >
                <ExploreIcon sx={{ 
                  fontSize: { xs: 22, lg: 28 }, 
                  color: isExploreActive ? '#1ed760' : 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                onClick={() => handleSkipWithLocation('previous')}
                // onClick={handlePrevious}
                disabled={isLoading}
                className="control-button w-10 h-10 lg:w-12 lg:h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ backgroundColor: '#282828' }}
                aria-label="Previous"
              >
                <SkipPreviousIcon sx={{ 
                  fontSize: { xs: 22, lg: 28 }, 
                  color: 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                onClick={handlePlayPause}
                disabled={isLoading}
                className="w-14 h-14 lg:w-16 lg:h-16 flex items-center justify-center rounded-full bg-white hover:bg-gray-100 transition-colors shadow-lg focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
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
                  <svg width="28" height="28" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="lg:w-8 lg:h-8">
                    <rect x="10" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                    <rect x="24" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                  </svg>
                ) : (
                  <PlayArrowIcon sx={{ fontSize: { xs: 28, lg: 32 }, color: '#4B5563' }} />
                )}
              </button>
              <button
                onClick={() => handleSkipWithLocation('next')}
                // onClick={handleNext}
                disabled={isLoading}
                className="control-button w-10 h-10 lg:w-12 lg:h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ backgroundColor: '#282828' }}
                aria-label="Next"
              >
                <SkipNextIcon sx={{ 
                  fontSize: { xs: 22, lg: 28 }, 
                  color: 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                onClick={handleRepeatToggle}
                disabled={isLoading}
                className="control-button w-10 h-10 lg:w-12 lg:h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                style={{ backgroundColor: '#282828' }}
                aria-label="Repeat"
              >
                <RepeatIcon sx={{ 
                  fontSize: { xs: 22, lg: 28 }, 
                  color: isRepeatActive ? '#1ed760' : 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
            </div>
            <div className="mt-6 lg:mt-8 text-gray-500 text-xs text-center">
              SpotOn &mdash; Inspired by Spotify
              {playerState.is_playing && <div className="mt-1 text-green-400">🎵 Playing on Spotify</div>}
              {playerState.device && <div className="mt-1 text-blue-400">📱 {playerState.device}</div>}
            </div>
          </div>
        </div>
      </div>
      
      {/* Scrolling Text Banner - Hidden on mobile, shown on desktop */}
      <div className="hidden lg:block fixed bottom-0 left-0 right-0 bg-black text-green-400 py-3 overflow-hidden">
        <div className="scrolling-text whitespace-nowrap">
          SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON SPOTIFY SPOTON
        </div>
      </div>
    </div>
  );
}

export default App;
