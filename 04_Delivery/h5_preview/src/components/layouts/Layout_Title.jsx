import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Title({ slide, subtitles, currentTime }) {
    return (
        <div className="slide-container layout-title">
            <div className="slide-visual-layer">
                {/* Optional Background Image for Title */}
                {slide.image && <img src={`/${slide.image}`} className="title-background" alt="" />}
                <div className="title-overlay-gradient"></div>
            </div>

            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime}>
                <div className="title-center-content">
                    {slide.text && <h1 className="main-title">{slide.text}</h1>}
                    {slide.sub && <p className="sub-title">{slide.sub}</p>}
                    <div className="title-decoration-line"></div>
                </div>
            </SlideOverlay>
        </div>
    );
}
