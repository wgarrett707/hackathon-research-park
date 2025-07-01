import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8080';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Global variable to store the current Nango connection ID
let currentConnectionId: string | null = null;

// Function to set the connection ID (to be called from the main app)
export const setConnectionId = (connectionId: string | null) => {
  currentConnectionId = connectionId;
};

// Function to get headers with connection ID if available
const getHeaders = () => {
  const headers: Record<string, string> = {};
  if (currentConnectionId) {
    headers['X-Connection-Id'] = currentConnectionId;
  }
  return headers;
};

export interface Song {
  id: string;
  title: string;
  artist: string;
  album: string;
  album_cover: string;
  spotify_id?: string; // Spotify track ID
}

export interface PlayerState {
  is_playing: boolean;
  current_song: Song | null;
  current_time: number;
  duration?: number;
  device?: string;
  message?: string;
}

export interface PlaybackRequest {
  action: 'play' | 'pause' | 'next' | 'previous' | 'seek';
  position?: number;
}

// Add health check function to test backend connectivity
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// API functions
export const getPlayerStatus = async (): Promise<PlayerState> => {
  const response = await api.get('/player/status', { headers: getHeaders() });
  return response.data;
};

export const controlPlayer = async (request: PlaybackRequest): Promise<PlayerState> => {
  const response = await api.post('/player/control', request, { headers: getHeaders() });
  return response.data;
};

export const getSong = async () => {
  const response = await api.post('/get_song', {}, { headers: getHeaders() });
  return response.data;
};

// Spotify integration functions
export const refreshSpotifyMetadata = async () => {
  const response = await api.post('/refresh-spotify-metadata', {}, { headers: getHeaders() });
  return response.data;
};

export const getSpotifyStatus = async () => {
  const response = await api.get('/spotify-status', { headers: getHeaders() });
  return response.data;
};

// Player control helpers
export const playMusic = () => controlPlayer({ action: 'play' });
export const pauseMusic = () => controlPlayer({ action: 'pause' });
export const nextTrack = () => controlPlayer({ action: 'next' });
export const previousTrack = () => controlPlayer({ action: 'previous' });
export const seekToPosition = (position: number) => controlPlayer({ action: 'seek', position });

export default api;
