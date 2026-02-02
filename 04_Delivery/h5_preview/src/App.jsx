import { useState, useEffect, useRef } from 'react'
import './App.css'
import SliderFactory from './components/SliderFactory'
import TimelineBar from './components/TimelineBar'
import GestureLayer from './components/GestureLayer'

function App() {
  const [manifest, setManifest] = useState(null)
  const [currentSectionIdx, setCurrentSectionIdx] = useState(0)
  const [currentSlideIdx, setCurrentSlideIdx] = useState(0)
  const [subtitles, setSubtitles] = useState([])

  // Audio State
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [userSeeking, setUserSeeking] = useState(false) // Track if user is interacting

  const audioRef = useRef(null)

  // 1. Load Initial Data
  useEffect(() => {
    fetch('/slides.json')
      .then(res => res.json())
      .then(data => {
        setManifest(data)
        if (data.sections.length > 0) {
          // Defaults are 0, managed by state
        }
      })
      .catch(err => console.error("Failed to load slides.json", err))
  }, [])

  // 2. Load Subtitles when Section Changes
  useEffect(() => {
    if (!manifest) return
    const section = manifest.sections[currentSectionIdx]
    loadSubtitle(section.id) // Assuming SRT filename matches ID
  }, [currentSectionIdx, manifest])

  const loadSubtitle = (sectionId) => {
    fetch(`/tts/${sectionId}.srt`)
      .then(res => res.text())
      .then(text => {
        const parsed = parseSRT(text)
        setSubtitles(parsed)
      })
      .catch(() => setSubtitles([]))
  }

  // 3. Audio Time Update & Duration
  const handleTimeUpdate = () => {
    if (audioRef.current) {
      setCurrentTime(audioRef.current.currentTime)
    }
  }

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration)
    }
  }

  const handleEnded = () => {
    setIsPlaying(false)
  }

  // Wake Lock API
  useEffect(() => {
    let wakeLock = null;

    const requestWakeLock = async () => {
      if ('wakeLock' in navigator) {
        try {
          wakeLock = await navigator.wakeLock.request('screen');
          // console.log('Wake Lock active');
        } catch (err) {
          console.warn(`Wake Lock Error: ${err.name}, ${err.message}`);
        }
      }
    };

    const releaseWakeLock = () => {
      if (wakeLock) {
        wakeLock.release().then(() => {
          wakeLock = null;
          // console.log('Wake Lock released');
        });
      }
    };

    if (isPlaying) {
      requestWakeLock();
    } else {
      releaseWakeLock();
    }

    // Handle visibility change (tab switch releases lock)
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible' && isPlaying) {
        requestWakeLock();
      }
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      releaseWakeLock();
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [isPlaying]);

  // 4. Auto-Sync Logic: Time -> Slide
  useEffect(() => {
    if (!manifest || userSeeking) return; // Disable auto-switch when seeking
    const section = manifest.sections[currentSectionIdx];
    if (!section || !section.slides) return;

    // Find the latent slide for current time
    // We want the last slide where startTime <= currentTime
    const slides = section.slides;
    let targetIdx = 0;

    // Optimize: Could be binary search, but list is short (<50)
    for (let i = 0; i < slides.length; i++) {
      const s = slides[i];
      if (s.startTime !== undefined && s.startTime <= currentTime + 0.1) { // 0.1s buffer
        targetIdx = i;
      } else if (s.startTime > currentTime) {
        break;
      }
    }

    if (targetIdx !== currentSlideIdx) {
      setCurrentSlideIdx(targetIdx);
    }
  }, [currentTime, manifest, currentSectionIdx, userSeeking]);


  // Actions
  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause()
      } else {
        audioRef.current.play()
      }
      setIsPlaying(!isPlaying)
    }
  }

  const seekTo = (time) => {
    // If NaN or undefined, ignore
    if (!Number.isFinite(time)) return;

    if (audioRef.current) {
      const safeTime = Math.max(0, Math.min(time, duration || 0));
      audioRef.current.currentTime = safeTime;
      setCurrentTime(safeTime);
      // Depending on preference, we might auto-play or stay paused
      if (!isPlaying) {
        // Option: Auto-play on seek? 
        // For drag gestures, usually yes, but let's keep user intent.
        // If user was paused, stay paused. If playing, stay playing.
      }
    }
  }

  const handleGestureStart = () => {
    setUserSeeking(true);
  };

  const handleGestureSeek = (time) => {
    setUserSeeking(false);
    seekTo(time);
    // Optional: Auto-play after drag?
    // togglePlay(true)? 
  };

  const switchSection = (idx) => {
    setCurrentSectionIdx(idx);
    setCurrentSlideIdx(0);
    setCurrentTime(0);
    setIsPlaying(false);
    // Audio src changes automatically via render
  }

  // Helpers
  const parseSRT = (text) => {
    if (!text) return []
    const pattern = /(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n([\s\S]*?)(?=\n\n|\n*$)/g
    const result = []
    let match
    while ((match = pattern.exec(text)) !== null) {
      result.push({
        id: match[1],
        start: srtTimeToSeconds(match[2]),
        end: srtTimeToSeconds(match[3]),
        text: match[4].replace(/\n/g, ' ')
      })
    }
    return result
  }

  const srtTimeToSeconds = (timeStr) => {
    const [h, m, s] = timeStr.replace(',', '.').split(':')
    return parseFloat(h) * 3600 + parseFloat(m) * 60 + parseFloat(s)
  }

  if (!manifest) return <div className="loading">Loading Course Data...</div>

  const currentSection = manifest.sections[currentSectionIdx]
  const currentSlide = currentSection?.slides[currentSlideIdx]

  return (
    <div className="app-container">
      {/* Main Display Area */}
      <div className="slide-area">
        {/* Gesture Layer sits on top of slides */}
        <GestureLayer
          currentTime={currentTime}
          duration={duration}
          onSeek={handleGestureSeek}
          onSeekStart={handleGestureStart}
        />

        {currentSlide ? (
          <SliderFactory
            slide={currentSlide}
            subtitles={subtitles}
            currentTime={currentTime}
          />
        ) : (
          <div className="empty-state">
            <p>Select a Module to Start</p>
          </div>
        )}
      </div>

      {/* Bottom Control Hub */}
      <div className="controls-hub">
        {/* Section Tabs */}
        <div className="section-selector compact">
          {manifest.sections.map((sec, idx) => (
            <button
              key={sec.id}
              className={`section-tab ${idx === currentSectionIdx ? 'active' : ''}`}
              onClick={() => switchSection(idx)}
            >
              {sec.title}
            </button>
          ))}
        </div>

        {/* Core Controls */}
        <div className="playback-row">
          <button className="play-button small" onClick={togglePlay}>
            {isPlaying ? (
              <svg viewBox="0 0 24 24"><path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" /></svg>
            ) : (
              <svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z" /></svg>
            )}
          </button>

          <TimelineBar
            currentTime={currentTime}
            duration={duration}
            slides={currentSection.slides}
            onSeek={seekTo}
          />
        </div>
      </div>

      {/* Hidden Audio Engine */}
      <audio
        ref={audioRef}
        src={currentSection.audio ? `/${currentSection.audio}` : ''}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={handleEnded}
      />
    </div>
  )
}

export default App
