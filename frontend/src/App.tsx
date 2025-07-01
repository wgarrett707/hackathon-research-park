import { useState, useRef, useEffect } from 'react';
import './index.css';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import SkipNextIcon from '@mui/icons-material/SkipNext';
import SkipPreviousIcon from '@mui/icons-material/SkipPrevious';
import HomeIcon from '@mui/icons-material/Home';
import SearchIcon from '@mui/icons-material/Search';
import NotificationsIcon from '@mui/icons-material/Notifications';
import ExploreIcon from '@mui/icons-material/Explore';
import RepeatIcon from '@mui/icons-material/Repeat';

const mockTrack = {
  title: 'Blinding Lights',
  artist: 'The Weeknd',
  albumCover: 'https://i.scdn.co/image/ab67616d0000b273e5bfa1a3c7c1b8b8e1e1e1e1',
  duration: 210, // seconds
};

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function App() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [isExploreActive, setIsExploreActive] = useState(false);
  const [isRepeatActive, setIsRepeatActive] = useState(false);
  const [textIndex, setTextIndex] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const phrases = ["is here.", "is enabled.", "is on.", "is ready.", "is live."];

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev < mockTrack.duration) return prev + 1;
          setIsPlaying(false);
          return prev;
        });
      }, 1000);
    } else if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [isPlaying]);

  useEffect(() => {
    const textInterval = setInterval(() => {
      setTextIndex((prev) => (prev + 1) % phrases.length);
    }, 2000);

    return () => clearInterval(textInterval);
  }, []);

  const handlePlayPause = () => {
    if (currentTime >= mockTrack.duration) setCurrentTime(0);
    setIsPlaying((p) => !p);
  };

  const handleScrub = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentTime(Number(e.target.value));
  };

  const handleExploreToggle = () => {
    setIsExploreActive(!isExploreActive);
  };

  const handleRepeatToggle = () => {
    setIsRepeatActive(!isRepeatActive);
  };

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
        
        <div className="flex flex-col lg:flex-row items-center justify-center w-full px-4">
          {/* Animated Text - Hidden on mobile, shown on desktop */}
          <div className="hidden lg:flex flex-col items-start justify-center lg:w-1/2 lg:pr-8 lg:ml-8">
            <div className="text-white text-7xl font-bold text-left flex items-baseline">
              <span className="mr-2">SpotOn </span>
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
          
          <div className="w-full max-w-sm rounded-xl shadow-lg bg-[#282828] p-6 flex flex-col items-center">
            <img
              src={mockTrack.albumCover}
              alt="Album Cover"
              className="w-40 h-40 rounded-lg mb-4 shadow-md object-cover"
            />
            <div className="text-white text-lg font-semibold text-center mb-1">
              {mockTrack.title}
            </div>
            <div className="text-gray-400 text-sm text-center mb-4">{mockTrack.artist}</div>
            <div className="w-full flex items-center gap-2 mb-4">
              <span className="text-xs text-gray-400 w-8 text-right">
                {formatTime(currentTime)}
              </span>
              <input
                type="range"
                min={0}
                max={mockTrack.duration}
                value={currentTime}
                onChange={handleScrub}
                className="flex-1 accent-green-500 h-1 rounded-lg"
              />
              <span className="text-xs text-gray-400 w-8 text-left">
                {formatTime(mockTrack.duration)}
              </span>
            </div>
            <div className="flex items-center justify-center gap-4 mb-4">
              <button
                onClick={handleExploreToggle}
                className="control-button w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors"
                style={{ backgroundColor: '#282828' }}
                aria-label="Explore"
              >
                <ExploreIcon sx={{ 
                  fontSize: 28, 
                  color: isExploreActive ? '#1ed760' : 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                className="control-button w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors"
                style={{ backgroundColor: '#282828' }}
                aria-label="Previous"
              >
                <SkipPreviousIcon sx={{ 
                  fontSize: 28, 
                  color: 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                onClick={handlePlayPause}
                className="w-16 h-16 flex items-center justify-center rounded-full bg-white hover:bg-gray-100 transition-colors shadow-lg focus:outline-none"
                style={{ 
                  backgroundColor: 'white',
                  borderRadius: '50%',
                  border: 'none',
                  padding: 0
                }}
                aria-label={isPlaying ? 'Pause' : 'Play'}
              >
                {isPlaying ? (
                  <svg width="32" height="32" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="10" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                    <rect x="24" y="8" width="6" height="24" rx="2" fill="#4B5563" />
                  </svg>
                ) : (
                  <PlayArrowIcon sx={{ fontSize: 32, color: '#4B5563' }} />
                )}
              </button>
              <button
                className="control-button w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors"
                style={{ backgroundColor: '#282828' }}
                aria-label="Next"
              >
                <SkipNextIcon sx={{ 
                  fontSize: 28, 
                  color: 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
              <button
                onClick={handleRepeatToggle}
                className="control-button w-12 h-12 flex items-center justify-center bg-[#282828] !important border-none focus:outline-none hover:bg-gray-600 transition-colors"
                style={{ backgroundColor: '#282828' }}
                aria-label="Repeat"
              >
                <RepeatIcon sx={{ 
                  fontSize: 28, 
                  color: isRepeatActive ? '#1ed760' : 'white',
                  transition: 'color 0.2s ease'
                }} />
              </button>
            </div>
            <div className="mt-8 text-gray-500 text-xs text-center">SpotOn &mdash; Inspired by Spotify</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
