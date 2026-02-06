import React, { useRef, useState } from 'react';

export default function TimelineBar({ currentTime, duration, slides, onSeek }) {
    const barRef = useRef(null);
    const [hoverTime, setHoverTime] = useState(null);

    // Calculate progress percentage
    const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

    const handleBarClick = (e) => {
        if (!barRef.current || duration <= 0) return;
        const rect = barRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const width = rect.width;
        const percentage = Math.max(0, Math.min(1, x / width));
        const newTime = percentage * duration;
        onSeek(newTime);
    };

    const handleMarkerClick = (e, time) => {
        e.stopPropagation(); // Prevent bubbling to bar click
        onSeek(time);
    };

    const formatTime = (time) => {
        if (!isFinite(time)) return "0:00";
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    };

    // ...existing imports...

    // ...existing code...
    const getMarkerClass = (slide) => {
        const classes = ['timeline-marker'];

        // 1. Missing Asset Check
        if (!slide.image) {
            classes.push('marker-missing');
        }

        // 2. Type Classification
        const type = slide.type || 'Unknown';
        if (type.includes('Demo') || type.includes('Action')) classes.push('marker-type-demo');
        else if (type.includes('Concept') || type.includes('Art') || type.includes('Metaphor')) classes.push('marker-type-art');
        else if (type.includes('Diagram') || type.includes('Chart')) classes.push('marker-type-diagram');
        else if (type.includes('Video') || type.includes('Motion')) classes.push('marker-type-video');
        else classes.push('marker-type-default');

        return classes.join(' ');
    };

    return (
        <div className="timeline-wrapper">
            <div
                className="timeline-bar"
                ref={barRef}
                onClick={handleBarClick}
                onMouseMove={(e) => {
                    // Optional: Hover preview logic could go here
                }}
                style={{ background: 'var(--color-border)' }}
            >
                {/* Progress Fill */}
                <div className="timeline-fill" style={{ width: `${progress}%` }}></div>

                {/* Slide Markers */}
                {slides.map((slide, idx) => {
                    if (slide.startTime === undefined) return null;
                    const leftPct = (slide.startTime / duration) * 100;
                    // Prevent markers from going off visual bounds if duration is weird, though usually consistent.
                    if (!isFinite(leftPct) || leftPct < 0 || leftPct > 100) return null;

                    return (
                        <div
                            key={slide.id}
                            className={getMarkerClass(slide)}
                            style={{
                                left: `${leftPct}%`,
                            }}
                            onClick={(e) => handleMarkerClick(e, slide.startTime)}
                            title={`${slide.id}: ${slide.text || slide.type} (${formatTime(slide.startTime)})`}
                        >
                            <div className="marker-tooltip" style={{ background: 'var(--color-bg-surface)', border: '1px solid var(--color-border)' }}>
                                <span className="tooltip-time">{formatTime(slide.startTime)}</span>
                                <span className="tooltip-title">{slide.id}</span>
                                {!slide.image && <span className="tooltip-warning">⚠️ No Asset</span>}
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Time Display (Integrated below bar) */}
            <div className="timeline-info">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
            </div>
        </div>
    );
}
