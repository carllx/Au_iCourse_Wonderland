import React, { useRef, useEffect } from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Cinema({ slide, subtitles, currentTime, onGlobalControl }) {
    const videoRef = useRef(null);
    const videoDoneRef = useRef(false);

    // Parse Start/End times
    const mediaStart = slide.mediaStart ? parseFloat(slide.mediaStart) : 0;
    const mediaEnd = slide.mediaEnd ? parseFloat(slide.mediaEnd) : null;

    // 1. Reset done state ONLY when the actual media asset changes
    useEffect(() => {
        videoDoneRef.current = false;
        if (videoRef.current && mediaStart > 0) {
            videoRef.current.currentTime = mediaStart;
        }
    }, [slide.image, mediaStart, mediaEnd]);

    // 2. Auto-Play & TTS Mutex Logic
    useEffect(() => {
        if (!slide.image) return;
        const video = videoRef.current;
        if (!video) return;

        const playVideo = async () => {
            // If we already finished this segment, don't auto-replay/pause TTS
            if (videoDoneRef.current) return;

            // Always pause TTS on entry for Cinema (Video) slides
            if (onGlobalControl) onGlobalControl(false);

            try {
                await video.play();
            } catch (err) {
                console.warn("Cinema Video autoplay blocked:", err);
            }
        };

        const onPlay = () => {
            if (onGlobalControl) onGlobalControl(false);
        };

        const onPause = () => {
            // We don't auto-resume TTS on pause to maintain focus
        };

        const onEnded = () => {
            // Signal completion if not already handled by handleTimeUpdate
            if (!mediaEnd && !videoDoneRef.current) {
                videoDoneRef.current = true;
                if (onGlobalControl) onGlobalControl(true);
            }
        };

        video.addEventListener('play', onPlay);
        video.addEventListener('pause', onPause);
        video.addEventListener('ended', onEnded);

        playVideo();

        return () => {
            video.removeEventListener('play', onPlay);
            video.removeEventListener('pause', onPause);
            video.removeEventListener('ended', onEnded);
            // Cleanup: Always allow TTS to resume when leaving the slide
            if (onGlobalControl) onGlobalControl(true);
        };
    }, [slide.image, onGlobalControl, mediaEnd]);

    // 3. Handle Video Time Logic (Segment Loop)
    const handleTimeUpdate = () => {
        const video = videoRef.current;
        if (!video) return;

        // Loop Logic for specific segments:
        if (mediaEnd && video.currentTime >= mediaEnd) {
            if (!video.paused) video.pause();

            // Debounce: Only trigger 'Ended' logic once per playback session
            if (!videoDoneRef.current) {
                console.log("[Cinema] Segment End Reached, resuming TTS...");
                videoDoneRef.current = true;
                if (onGlobalControl) onGlobalControl(true);
            }
        }
        // Reset if user seeks back far enough
        else if (mediaEnd && video.currentTime < (mediaEnd - 1)) {
            if (videoDoneRef.current) {
                console.log("[Cinema] User seeked back, resetting done state");
                videoDoneRef.current = false;
            }
        }
    };

    const handleLoadedMetadata = () => {
        if (videoRef.current && mediaStart > 0) {
            videoRef.current.currentTime = mediaStart;
        }
    };

    return (
        <div className="slide-container layout-cinema">
            <div className="slide-visual-layer cinema">
                {slide.image && (
                    (slide.image.endsWith('.mp4') || slide.image.endsWith('.mov') || slide.image.endsWith('.webm')) ? (
                        <video
                            ref={videoRef}
                            src={`/${slide.image}`}
                            className="cinema-media"
                            controls={true}
                            playsInline
                            onTimeUpdate={handleTimeUpdate}
                            onLoadedMetadata={handleLoadedMetadata}
                            style={{ zIndex: 60, position: 'relative' }}
                        />
                    ) : (
                        <img src={`/${slide.image}`} alt={slide.id} className="cinema-media" />
                    )
                )}
            </div>

            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime}>
                <div className="cinema-overlay">
                    {slide.text && <h2 className="slide-text cinema-title">{slide.text}</h2>}
                </div>
            </SlideOverlay>
        </div>
    );
}
