import React from 'react';

// Shared Overlay Component for all slide layouts
export function SlideOverlay({ slide, subtitles, currentTime, children }) {
    return (
        <div className="slide-overlay-layer">
            {/* 类型标签 */}
            <span className="slide-type-tag">{slide.type || 'Slide'}</span>

            {/* Slide ID */}
            <span className="slide-id">{slide.id}</span>

            {/* Demo 元数据徽章 */}
            {slide.type === 'Live Demo' && (
                <div className="demo-meta-badges">
                    {slide.target && <span className="demo-badge target">OBJ: {slide.target}</span>}
                    {slide.duration && <span className="demo-badge duration">DUR: {slide.duration}</span>}
                </div>
            )}

            {/* 允许插入自定义中间内容 (如 Title Layout 的标题) */}
            {children}

            {/* 概念标签 */}
            {slide.concept && <div className="slide-concept">{slide.concept}</div>}

            {/* 固定引用文本 */}
            {slide.caption && <p className="slide-caption">"{slide.caption}"</p>}

            {/* 交互式字幕 (最上层) */}
            {subtitles && (
                <div className="subtitle-display">
                    <p className="subtitle-text">{subtitles.find(s => currentTime >= s.start && currentTime <= s.end)?.text || ''}</p>
                </div>
            )}
        </div>
    );
}
