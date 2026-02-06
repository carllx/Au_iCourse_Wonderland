import React, { useRef, useEffect } from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Demo({ slide, subtitles, currentTime, onGlobalControl }) {
    const videoRef = useRef(null);
    const videoDoneRef = useRef(false);
    const mediaStart = slide.mediaStart ? parseFloat(slide.mediaStart) : 0;
    const mediaEnd = slide.mediaEnd ? parseFloat(slide.mediaEnd) : null;
    const isVideo = slide.image && (slide.image.endsWith('.mp4') || slide.image.endsWith('.mov') || slide.image.endsWith('.webm'));

    // 1. Auto-Play & TTS Mutex Logic
    useEffect(() => {
        if (!isVideo || !videoRef.current) return;

        const video = videoRef.current;
        videoDoneRef.current = false; // Reset on entry

        const playVideo = async () => {
            if (videoDoneRef.current) return;
            if (onGlobalControl) onGlobalControl(false);
            try {
                await video.play();
            } catch (err) {
                console.warn("Video autoplay blocked:", err);
            }
        };

        const onPlay = () => { if (onGlobalControl) onGlobalControl(false); };
        const onPause = () => { };
        const onEnded = () => {
            if (!videoDoneRef.current && !mediaEnd) {
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
            if (onGlobalControl) onGlobalControl(true);
        };
    }, [isVideo, onGlobalControl, slide.id]);

    const handleTimeUpdate = () => {
        const video = videoRef.current;
        if (!video) return;

        if (mediaEnd && video.currentTime >= mediaEnd) {
            if (!video.paused) video.pause();
            if (!videoDoneRef.current) {
                videoDoneRef.current = true;
                if (onGlobalControl) onGlobalControl(true);
            }
        } else if (mediaEnd && video.currentTime < (mediaEnd - 1)) {
            if (videoDoneRef.current) videoDoneRef.current = false;
        }
    };

    const handleLoadedMetadata = () => {
        if (videoRef.current && mediaStart > 0) {
            videoRef.current.currentTime = mediaStart;
        }
    };

    return (
        <div className="slide-container layout-content">
            <div className="slide-visual-layer">
                <div className="layout-grid-content demo-mode">
                    <div className="area-title">
                        {slide.text && <h1 className="slide-text">{slide.text}</h1>}
                        {slide.sub && <p className="slide-sub">{slide.sub}</p>}
                    </div>

                    <div className="area-right full-height">
                        {isVideo ? (
                            <div className="media-wrapper">
                                <video
                                    ref={videoRef}
                                    src={`/${slide.image}`}
                                    className="demo-media"
                                    controls={true}
                                    playsInline
                                    onTimeUpdate={handleTimeUpdate}
                                    onLoadedMetadata={handleLoadedMetadata}
                                />
                            </div>
                        ) : (
                            slide.image ? (
                                <div className="media-wrapper">
                                    <img src={`/${slide.image}`} alt={slide.id} />
                                </div>
                            ) : (
                                <div className="visual-placeholder">Demo Screencast</div>
                            )
                        )}

                        {slide.action && (
                            <div className="demo-action-overlay">
                                <span className="action-label">ACTION:</span>
                                <span className="action-text">{slide.action}</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime} />
        </div>
    );
}
