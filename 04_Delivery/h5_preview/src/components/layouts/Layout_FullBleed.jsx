import React, { useRef, useEffect } from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_FullBleed({ slide, subtitles, currentTime, onGlobalControl }) {
    const videoRef = useRef(null);
    const videoDoneRef = useRef(false);
    const isVideo = slide.image && (slide.image.endsWith('.mp4') || slide.image.endsWith('.mov') || slide.image.endsWith('.webm'));

    // Auto-Play & TTS Mutex Logic for Full Bleed
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
                console.warn("FullBleed Video autoplay blocked:", err);
            }
        };

        const onPlay = () => { if (onGlobalControl) onGlobalControl(false); };
        const onPause = () => { };
        const onEnded = () => {
            if (!videoDoneRef.current) {
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

    return (
        <div className="slide-container layout-full-bleed">
            <div className="slide-visual-layer full-bleed">
                {slide.image ? (
                    (isVideo) ? (
                        <video
                            ref={videoRef}
                            src={`/${slide.image}`}
                            className="full-bleed-media"
                            controls={true}
                            playsInline
                            style={{ zIndex: 60, position: 'relative' }}
                        />
                    ) : (
                        <img src={`/${slide.image}`} alt={slide.id} className="full-bleed-media" />
                    )
                ) : (
                    <div className="visual-placeholder dark">Full Bleed Visual</div>
                )}

                <div className="full-bleed-gradient-overlay"></div>
            </div>

            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime}>
                <div className="full-bleed-text-area">
                    {slide.text && <h1 className="slide-text shadow">{slide.text}</h1>}
                    {slide.sub && <p className="slide-sub shadow">{slide.sub}</p>}
                </div>
            </SlideOverlay>
        </div>
    );
}
