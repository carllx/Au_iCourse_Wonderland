import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Demo({ slide, subtitles, currentTime }) {
    // Live Demo Layout: Needs to show Action/Target clearly overlaying the interface screenshot
    return (
        <div className="slide-container layout-content">
            {/* Reusing Content Layout basics but with specific Demo badges */}
            <div className="slide-visual-layer">
                <div className="layout-grid-content demo-mode">

                    <div className="area-title">
                        {slide.text && <h1 className="slide-text">{slide.text}</h1>}
                        {slide.sub && <p className="slide-sub">{slide.sub}</p>}
                    </div>

                    <div className="area-right full-height">
                        {slide.image ? (
                            <div className="media-wrapper">
                                <img src={`/${slide.image}`} alt={slide.id} />
                            </div>
                        ) : (
                            <div className="visual-placeholder">Demo Screencast</div>
                        )}

                        {/* Action Overlay */}
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
