import { useState, useRef, useEffect } from 'react';

/**
 * GestureLayer
 * Transparent overlay that handles vertical drag-to-seek interaction.
 * Shows a large timecode overlay during interaction.
 */

const SENSITIVITY = 15; // pixels per second of audio

export default function GestureLayer({ currentTime, duration, onSeek, onSeekStart }) {
    const [isDragging, setIsDragging] = useState(false);
    const [seekTime, setSeekTime] = useState(currentTime);
    const startY = useRef(0);
    const startTime = useRef(0);

    // Sync seekTime when not dragging to avoid jump on start
    useEffect(() => {
        if (!isDragging) {
            setSeekTime(currentTime);
        }
    }, [currentTime, isDragging]);

    const handleTouchStart = (e) => {
        // Only handle single touch
        if (e.touches.length > 1) return;

        setIsDragging(true);
        startY.current = e.touches[0].clientY;
        startTime.current = currentTime;

        if (onSeekStart) onSeekStart();
    };

    const handleTouchMove = (e) => {
        if (!isDragging) return;

        const currentY = e.touches[0].clientY;
        // Calculate Delta: Start - Current
        // Drag Up (Current < Start) -> Positive Delta -> Time Forward
        // Drag Down (Current > Start) -> Negative Delta -> Time Backward
        const deltaY = startY.current - currentY;

        // Calculate Time Delta
        const timeDelta = deltaY / SENSITIVITY;

        let newTime = startTime.current + timeDelta;

        // Clamp
        if (newTime < 0) newTime = 0;
        if (newTime > duration) newTime = duration;

        setSeekTime(newTime);
    };

    const handleTouchEnd = () => {
        if (isDragging) {
            setIsDragging(false);
            // specific check to prevent accidental infinite clicks or drags
            if (Math.abs(seekTime - startTime.current) > 0.1) {
                if (onSeek) onSeek(seekTime);
            } else {
                // If drag was very small, maybe treat as click? 
                // For now, if drag is minimal, we still seek but it's effectively a no-op visually
                if (onSeek) onSeek(seekTime);
            }
        }
    };

    // Format helper
    const formatTime = (seconds) => {
        if (!seconds && seconds !== 0) return "--:--";
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        const ms = Math.floor((seconds % 1) * 10);
        return `${m}:${s.toString().padStart(2, '0')}.${ms}`;
    };

    const layerStyle = {
        position: 'absolute',
        inset: 0,
        zIndex: 50, // Above slides, below controls
        touchAction: 'none', // Prevent browser scrolling
        userSelect: 'none',
        WebkitUserSelect: 'none',
    };

    const overlayStyle = {
        ...layerStyle,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'rgba(0,0,0,0.4)',
        backdropFilter: 'blur(4px)',
        transition: 'opacity 0.2s ease',
    };

    const textStyle = {
        color: 'white',
        fontVariantNumeric: 'tabular-nums',
        textShadow: '0 2px 10px rgba(0,0,0,0.5)',
        textAlign: 'center',
    };

    if (!isDragging) {
        return (
            <div
                className="gesture-layer-idle"
                style={layerStyle}
                onTouchStart={handleTouchStart}
                onTouchMove={handleTouchMove}
                onTouchEnd={handleTouchEnd}
            />
        );
    }

    return (
        <div
            className="gesture-layer-active"
            style={overlayStyle}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
        >
            <div style={textStyle}>
                <div style={{ fontSize: '4rem', fontWeight: '700', letterSpacing: '-2px' }}>
                    {formatTime(seekTime)}
                </div>
                <div style={{ fontSize: '1.2rem', opacity: 0.8, marginTop: '-0.5rem' }}>
                    / {formatTime(duration)}
                </div>
                <div style={{ marginTop: '2rem', fontSize: '0.9rem', opacity: 0.6, letterSpacing: '2px', textTransform: 'uppercase' }}>
                    Release to Seek
                </div>
            </div>

            {/* Visual Indicator of Direction */}
            <div style={{
                position: 'absolute',
                right: '20px',
                height: '200px',
                width: '4px',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '2px'
            }}>
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '-8px',
                    right: '-8px',
                    height: '4px',
                    background: 'var(--color-primary, #6366f1)',
                    transform: `translateY(${(startTime.current - seekTime) * SENSITIVITY}px)`,
                    borderRadius: '2px',
                    boxShadow: '0 0 10px var(--color-primary, #6366f1)'
                }} />
            </div>
        </div>
    );
}
