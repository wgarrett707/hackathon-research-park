import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

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

// API functions
export const getPlayerStatus = async (): Promise<PlayerState> => {
  const response = await api.get('/player/status');
  return response.data;
};

export const controlPlayer = async (request: PlaybackRequest): Promise<PlayerState> => {
  const response = await api.post('/player/control', request);
  return response.data;
};

export const getSong = async () => {
  const response = await api.post('/get_song');
  return response.data;
};

// Spotify integration functions
export const refreshSpotifyMetadata = async () => {
  const response = await api.post('/refresh-spotify-metadata');
  return response.data;
};

export const getSpotifyStatus = async () => {
  const response = await api.get('/spotify-status');
  return response.data;
};

// Player control helpers
export const playMusic = () => controlPlayer({ action: 'play' });
export const pauseMusic = () => controlPlayer({ action: 'pause' });
export const nextTrack = () => controlPlayer({ action: 'next' });
export const previousTrack = () => controlPlayer({ action: 'previous' });
export const seekToPosition = (position: number) => controlPlayer({ action: 'seek', position });

export default api;
