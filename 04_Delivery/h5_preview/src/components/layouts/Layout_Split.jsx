import React from 'react';
import { SlideOverlay } from '../SlideOverlay';

export default function Layout_Split({ slide, subtitles, currentTime }) {
    return (
        <div className="slide-container layout-split">
            <div className="slide-visual-layer">
                <div className="layout-grid-split">
                    {/* Title Spanning Top */}
                    <div className="area-title-split">
                        {slide.text && <h1 className="slide-text">{slide.text}</h1>}
                    </div>

                    {/* Left Panel */}
                    <div className="area-split-left">
                        {/* For now, we assume implicit content assignment or generic visual split */}
                        {/* Since existing data structure doesn't strictly separate left/right content in 'slides.json' easily without parsing 'visual' text, 
                    we will render the main image here if it exists, or a placeholder. 
                    TODO: Future improvement could split 'visual' description or 'list' into left/right. 
                    For S02_Demonstration, it's a composite image usually pre-baked. 
                    If pre-baked, it behaves like FullBleed or Content but with specific CSS. 
                    Assuming the image provided IS the split composition. 
                */}
                        {slide.image ? (
                            <div className="media-wrapper">
                                <img src={`/${slide.image}`} alt={slide.id} className="split-image-fit" />
                            </div>
                        ) : (
                            <div className="visual-placeholder">Left Panel</div>
                        )}
                    </div>

                    {/* Right Panel - In current data, usually the image is a single composite. 
               If we truly want split DOM, we need separate assets. 
               For this refactor, we'll assume the Image IS the split content for now, 
               OR if we have list items, they go here? 
               Let's make it flexible: Image Left, List Right? No, that's Content Layout.
               "UI Composite" usually implies two visual elements. 
               If only one image is provided, we display it centered or split? 
               Let's treat 'image' as filling the visual area. 
            */}
                    <div className="area-split-right">
                        {/* Placeholder or Secondary Content */}
                        {slide.list && (
                            <ul className="slide-list compact">
                                {slide.list.map((item, i) => <li key={i}>{item}</li>)}
                            </ul>
                        )}
                        {!slide.list && <div className="visual-placeholder">Right Panel / Info</div>}
                    </div>
                </div>
            </div>
            <SlideOverlay slide={slide} subtitles={subtitles} currentTime={currentTime} />
        </div>
    );
}
