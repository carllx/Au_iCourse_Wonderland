import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Content({ slide, subtitles, currentTime }) {
    return (
        <div className="slide-container layout-content">
            {/* Background/Visual Layer */}
            <div className="slide-visual-layer">
                <div className="layout-grid-content">
                    {/* Top Title Area */}
                    <div className="area-title">
                        {slide.text && <h1 className="slide-text">{slide.text}</h1>}
                        {slide.sub && <p className="slide-sub">{slide.sub}</p>}
                    </div>

                    {/* Left Content Area */}
                    <div className="area-left">
                        {slide.list && slide.list.length > 0 && (
                            <ul className="slide-list">
                                {slide.list.map((item, i) => (
                                    <li key={i}>{item}</li>
                                ))}
                            </ul>
                        )}
                        {!slide.list && !slide.image && <div className="placeholder-text">No Content</div>}
                    </div>

                    {/* Right Visual Area */}
                    <div className="area-right">
                        {slide.image ? (
                            <div className="media-wrapper">
                                {/* Support both Image and Video in Content Layout */}
                                {(slide.image.endsWith('.mp4') || slide.image.endsWith('.mov')) ? (
                                    <video src={`/${slide.image}`} autoPlay muted loop playsInline />
                                ) : (
                                    <img src={`/${slide.image}`} alt={slide.id} />
                                )}
                            </div>
                        ) : (
                            <div className="visual-placeholder">
                                <span>{slide.visual || "No Visual"}</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Shared Overlay (Subtitles, Badges) */}
            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime} />
        </div>
    );
}
