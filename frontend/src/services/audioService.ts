/**
 * Audio Service for handling real audio playback
 * Uses HTML5 Audio API to play music files
 */

export class AudioService {
  private audio: HTMLAudioElement | null = null;
  private onTimeUpdateCallback: ((currentTime: number) => void) | null = null;
  private onEndedCallback: (() => void) | null = null;
  private onLoadedCallback: (() => void) | null = null;
  private onErrorCallback: ((error: string) => void) | null = null;

  constructor() {
    // Initialize audio element
    this.audio = new Audio();
    this.setupEventListeners();
  }

  private setupEventListeners() {
    if (!this.audio) return;

    this.audio.addEventListener('timeupdate', () => {
      if (this.onTimeUpdateCallback && this.audio) {
        this.onTimeUpdateCallback(this.audio.currentTime);
      }
    });

    this.audio.addEventListener('ended', () => {
      if (this.onEndedCallback) {
        this.onEndedCallback();
      }
    });

    this.audio.addEventListener('loadeddata', () => {
      if (this.onLoadedCallback) {
        this.onLoadedCallback();
      }
    });

    this.audio.addEventListener('error', (e) => {
      console.error('Audio error:', e);
      if (this.onErrorCallback) {
        this.onErrorCallback('Failed to load audio file');
      }
    });

    this.audio.addEventListener('canplay', () => {
      console.log('Audio can play');
    });
  }

  // Load a new song
  loadSong(audioUrl: string): Promise<void> {
    return new Promise((resolve, reject) => {
      if (!this.audio) {
        reject(new Error('Audio not initialized'));
        return;
      }

      console.log('Loading song:', audioUrl);
      
      const handleCanPlay = () => {
        this.audio?.removeEventListener('canplay', handleCanPlay);
        this.audio?.removeEventListener('error', handleError);
        resolve();
      };

      const handleError = (e: Event) => {
        this.audio?.removeEventListener('canplay', handleCanPlay);
        this.audio?.removeEventListener('error', handleError);
        reject(new Error('Failed to load audio'));
      };

      this.audio.addEventListener('canplay', handleCanPlay);
      this.audio.addEventListener('error', handleError);
      
      this.audio.src = audioUrl;
      this.audio.load();
    });
  }

  // Play the current song
  async play(): Promise<void> {
    if (!this.audio) throw new Error('Audio not initialized');
    
    try {
      await this.audio.play();
      console.log('Audio playing');
    } catch (error) {
      console.error('Play failed:', error);
      throw new Error('Failed to play audio');
    }
  }

  // Pause the current song
  pause(): void {
    if (!this.audio) return;
    this.audio.pause();
    console.log('Audio paused');
  }

  // Seek to a specific time
  seekTo(time: number): void {
    if (!this.audio) return;
    this.audio.currentTime = time;
  }

  // Get current time
  getCurrentTime(): number {
    return this.audio?.currentTime || 0;
  }

  // Get duration
  getDuration(): number {
    return this.audio?.duration || 0;
  }

  // Get if audio is playing
  isPlaying(): boolean {
    return this.audio ? !this.audio.paused : false;
  }

  // Set volume (0 to 1)
  setVolume(volume: number): void {
    if (!this.audio) return;
    this.audio.volume = Math.max(0, Math.min(1, volume));
  }

  // Event listeners
  onTimeUpdate(callback: (currentTime: number) => void): void {
    this.onTimeUpdateCallback = callback;
  }

  onSongEnded(callback: () => void): void {
    this.onEndedCallback = callback;
  }

  onLoaded(callback: () => void): void {
    this.onLoadedCallback = callback;
  }

  onError(callback: (error: string) => void): void {
    this.onErrorCallback = callback;
  }

  // Cleanup
  destroy(): void {
    if (this.audio) {
      this.audio.pause();
      this.audio.src = '';
      this.audio = null;
    }
  }
}

// Create a singleton instance
export const audioService = new AudioService();
