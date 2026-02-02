import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_FullBleed({ slide, subtitles, currentTime }) {
    return (
        <div className="slide-container layout-full-bleed">
            <div className="slide-visual-layer full-bleed">
                {slide.image ? (
                    (slide.image.endsWith('.mp4') || slide.image.endsWith('.mov')) ? (
                        <video
                            src={`/${slide.image}`}
                            className="full-bleed-media"
                            autoPlay
                            muted
                            loop
                            playsInline
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
                {/* Custom positioning for Full Bleed Text */}
                <div className="full-bleed-text-area">
                    {slide.text && <h1 className="slide-text shadow">{slide.text}</h1>}
                    {slide.sub && <p className="slide-sub shadow">{slide.sub}</p>}
                </div>
            </SlideOverlay>
        </div>
    );
}
