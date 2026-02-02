import React from 'react';
import Layout_Content from './layouts/Layout_Content';
import Layout_Split from './layouts/Layout_Split';
import Layout_FullBleed from './layouts/Layout_FullBleed';
import Layout_Cinema from './layouts/Layout_Cinema';
import Layout_Demo from './layouts/Layout_Demo';
import Layout_Title from './layouts/Layout_Title';

const COMPONENT_MAP = {
    'Layout_Content': Layout_Content,
    'Layout_Split': Layout_Split,
    'Layout_FullBleed': Layout_FullBleed,
    'Layout_Cinema': Layout_Cinema,
    'Layout_Demo': Layout_Demo,
    'Layout_Title': Layout_Title,
};

// Fallback component
function UnknownLayout({ slide }) {
    return (
        <div className="empty-state">
            <p>Unknown Template: {slide.template}</p>
        </div>
    );
}

export default function SliderFactory({ slide, subtitles, currentTime }) {
    if (!slide) return null;

    const LayoutComponent = COMPONENT_MAP[slide.template] || Layout_Content; // Default to Content

    return (
        <LayoutComponent
            slide={slide}
            subtitles={subtitles}
            currentTime={currentTime}
        />
    );
}
