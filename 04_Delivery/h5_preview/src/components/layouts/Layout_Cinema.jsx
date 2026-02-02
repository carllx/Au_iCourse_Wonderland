import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Cinema({ slide, subtitles, currentTime }) {
    // Cinema Mode: Video centric, minimal distractions. 
    // Subtitles are crucial here.
    return (
        <div className="slide-container layout-cinema">
            <div className="slide-visual-layer cinema">
                {slide.image && (
                    (slide.image.endsWith('.mp4') || slide.image.endsWith('.mov')) ? (
                        <video
                            src={`/${slide.image}`}
                            className="cinema-media"
                            autoPlay
                            muted
                            loop
                            playsInline
                        />
                    ) : (
                        <img src={`/${slide.image}`} alt={slide.id} className="cinema-media" />
                    )
                )}
            </div>

            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime}>
                {/* Cinema mode usually hides text unless paused or queried, but for H5 preview we show it minimally */}
                <div className="cinema-overlay">
                    {slide.text && <h2 className="slide-text cinema-title">{slide.text}</h2>}
                </div>
            </SlideOverlay>
        </div>
    );
}
