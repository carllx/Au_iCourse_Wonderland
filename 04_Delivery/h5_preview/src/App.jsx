import { useState, useEffect, useRef, useCallback } from 'react'
import './App.css'

// ============================================================
// 工具函数
// ============================================================

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function parseSRT(srtText) {
  const blocks = srtText.trim().split(/\n\n+/)
  return blocks.map(block => {
    const lines = block.split('\n')
    if (lines.length < 3) return null

    const timeMatch = lines[1].match(/(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})/)
    if (!timeMatch) return null

    const parseTime = (timeStr) => {
      const [h, m, rest] = timeStr.split(':')
      const [s, ms] = rest.split(',')
      return parseInt(h) * 3600 + parseInt(m) * 60 + parseInt(s) + parseInt(ms) / 1000
    }

    return {
      index: parseInt(lines[0]),
      start: parseTime(timeMatch[1]),
      end: parseTime(timeMatch[2]),
      text: lines.slice(2).join(' '),
    }
  }).filter(Boolean)
}

// ============================================================
// SlideRenderer 组件
// ============================================================

function SlideRenderer({ slide, subtitles, currentTime }) {
  if (!slide) {
    return (
      <div className="slide-container empty-state">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
          <path d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        <p>进入纯音频模式</p>

        {/* 字幕仍然显示 */}
        {subtitles && (
          <SubtitleDisplay
            subtitles={subtitles}
            currentTime={currentTime}
          />
        )}
      </div>
    )
  }

  return (
    <div className="slide-container">
      {/* 视觉层 (灰盒布局 + 最终素材) */}
      <div className="slide-visual-layer">
        {/* 如果有最终素材图片/视频，显示 */}
        {slide.image ? (
          <div className="slide-image-container">
            {(slide.image.endsWith('.mp4') || slide.image.endsWith('.mov') || slide.image.endsWith('.webm')) ? (
              <video
                src={`/${slide.image}`}
                className="slide-image"
                autoPlay
                muted
                loop
                playsInline
              />
            ) : (
              <img src={`/${slide.image}`} alt={slide.id} className="slide-image" />
            )}
          </div>
        ) : null}

        {/* 动态占位层 (当没有图片时，或作为底层参考) */}
        {(!slide.image || slide.type === 'Live Demo') && (
          slide.layout?.zones?.map((zone, idx) => (
            <div
              key={idx}
              className="layout-zone"
              data-zone={zone.name}
              style={{
                left: `${zone.x * 100}%`,
                top: `${zone.y * 100}%`,
                width: `${zone.w * 100}%`,
                height: `${zone.h * 100}%`,
              }}
            >
              <span className="layout-zone-label">{zone.name}</span>
              {/* 如果是动作占位区且没有图片，显示动作文字 */}
              {!slide.image && (zone.name === 'ACTION_SCENE' || zone.name === 'STORYBOARD_ACTION') && (
                <div className="demo-action-text">{slide.action}</div>
              )}
            </div>
          ))
        )}
      </div>

      {/* 覆盖层：元数据与文字 */}
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

        <div className="slide-content-v-center">
          {/* 主标题 */}
          {slide.text && <h1 className="slide-text">{slide.text}</h1>}

          {/* 副标题 */}
          {slide.sub && <p className="slide-sub">{slide.sub}</p>}

          {/* 列表 */}
          {slide.list && slide.list.length > 0 && (
            <ul className="slide-list">
              {slide.list.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          )}

          {/* 视觉描述提示 (当没有图片时显示) */}
          {!slide.image && slide.visual && (
            <div className="slide-visual-hint">🎨 {slide.visual}</div>
          )}
        </div>

        {/* 概念标签 */}
        {slide.concept && <div className="slide-concept">{slide.concept}</div>}

        {/* 固定引用文本 */}
        {slide.caption && <p className="slide-caption">"{slide.caption}"</p>}

        {/* 交互式字幕 (最上层) */}
        {subtitles && (
          <SubtitleDisplay
            subtitles={subtitles}
            currentTime={currentTime}
          />
        )}
      </div>
    </div>
  )
}

// ============================================================
// AudioPlayer 组件
// ============================================================

function AudioPlayer({
  src,
  isPlaying,
  onPlayPause,
  onTimeUpdate,
  onEnded,
  audioRef
}) {
  const [duration, setDuration] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)

  const handleTimeUpdate = useCallback(() => {
    if (audioRef.current) {
      const time = audioRef.current.currentTime
      setCurrentTime(time)
      onTimeUpdate?.(time)
    }
  }, [onTimeUpdate, audioRef])

  const handleLoadedMetadata = () => {
    if (audioRef.current) {
      setDuration(audioRef.current.duration)
    }
  }

  const handleProgressClick = (e) => {
    if (audioRef.current && duration > 0) {
      const rect = e.currentTarget.getBoundingClientRect()
      const percent = (e.clientX - rect.left) / rect.width
      audioRef.current.currentTime = percent * duration
    }
  }

  const progress = duration > 0 ? (currentTime / duration) * 100 : 0

  return (
    <div className="controls-area">
      <audio
        ref={audioRef}
        src={src}
        onTimeUpdate={handleTimeUpdate}
        onLoadedMetadata={handleLoadedMetadata}
        onEnded={onEnded}
      />

      {/* 播放按钮 */}
      <button className="play-button" onClick={onPlayPause}>
        {isPlaying ? (
          <svg viewBox="0 0 24 24">
            <rect x="6" y="4" width="4" height="16" />
            <rect x="14" y="4" width="4" height="16" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24">
            <polygon points="5,3 19,12 5,21" />
          </svg>
        )}
      </button>

      {/* 进度条 */}
      <div className="progress-container">
        <div className="progress-bar" onClick={handleProgressClick}>
          <div
            className="progress-bar-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
        <div className="time-display">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>
    </div>
  )
}

// ============================================================
// SubtitleDisplay 组件
// ============================================================

function SubtitleDisplay({ subtitles, currentTime }) {
  const currentSub = subtitles.find(
    sub => currentTime >= sub.start && currentTime <= sub.end
  )

  if (!currentSub) return null

  return (
    <div className="subtitle-display">
      <p className="subtitle-text">{currentSub.text}</p>
    </div>
  )
}

// ============================================================
// App 主组件
// ============================================================

function App() {
  const [manifest, setManifest] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentSectionIdx, setCurrentSectionIdx] = useState(0)
  const [currentSlideIdx, setCurrentSlideIdx] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [subtitles, setSubtitles] = useState([])
  const [currentTime, setCurrentTime] = useState(0)

  const audioRef = useRef(null)

  // 加载 manifest
  useEffect(() => {
    fetch('/slides.json')
      .then(res => res.json())
      .then(data => {
        setManifest(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('加载 slides.json 失败:', err)
        setLoading(false)
      })
  }, [])

  // 当章节变化时，加载 SRT
  useEffect(() => {
    if (!manifest) return

    const section = manifest.sections[currentSectionIdx]
    if (section?.srt) {
      fetch(`/${section.srt}`)
        .then(res => res.text())
        .then(text => setSubtitles(parseSRT(text)))
        .catch(() => setSubtitles([]))
    } else {
      setSubtitles([])
    }

    // 重置播放状态
    setCurrentSlideIdx(0)
    setIsPlaying(false)
    setCurrentTime(0)
    if (audioRef.current) {
      audioRef.current.currentTime = 0
    }
  }, [manifest, currentSectionIdx])

  // 播放/暂停
  const handlePlayPause = useCallback(() => {
    if (!audioRef.current) return

    if (isPlaying) {
      audioRef.current.pause()
    } else {
      audioRef.current.play()
    }
    setIsPlaying(!isPlaying)
  }, [isPlaying])

  // 音频结束
  const handleEnded = useCallback(() => {
    setIsPlaying(false)
  }, [])

  // 导航 (修改为 Seek 模式)
  const handlePrevSlide = () => {
    const section = manifest?.sections[currentSectionIdx]
    if (currentSlideIdx > 0 && section) {
      const prevSlide = section.slides[currentSlideIdx - 1]
      // 如果有 startTime，则跳转音频
      if (prevSlide.startTime !== undefined && audioRef.current) {
        audioRef.current.currentTime = prevSlide.startTime
        // 状态更新会由 timeUpdate 触发，不需要手动 setSlide
      } else {
        // 回退模式
        setCurrentSlideIdx(currentSlideIdx - 1)
      }
    }
  }

  const handleNextSlide = () => {
    const section = manifest?.sections[currentSectionIdx]
    if (section && currentSlideIdx < section.slides.length - 1) {
      const nextSlide = section.slides[currentSlideIdx + 1]
      // 如果有 startTime，则跳转音频
      if (nextSlide.startTime !== undefined && audioRef.current) {
        audioRef.current.currentTime = nextSlide.startTime
      } else {
        setCurrentSlideIdx(currentSlideIdx + 1)
      }
    }
  }

  // 核心特性: Script-to-Timeline 自动同步
  // 监听 currentTime，自动切换 Slide
  useEffect(() => {
    if (!manifest) return
    const section = manifest.sections[currentSectionIdx]
    if (!section) return

    const slides = section.slides
    // 只有当存在 startTime 数据时才启用自动同步
    // 优化: 避免每帧都遍历，可以假设是顺序播放，从 currentSlideIdx 开始找
    // 但为了支持 Seek Back，还是做一次完整的查找 (slide数不多，性能OK)

    // 找到当前时间点应该显示的最后一张 Slide
    let targetIdx = 0
    let found = false

    for (let i = 0; i < slides.length; i++) {
      if (slides[i].startTime !== undefined) {
        if (currentTime >= slides[i].startTime) {
          targetIdx = i
          found = true
        } else {
          // 已经超过当前时间，后面的不用看了
          break
        }
      }
    }

    // 只有在找到了基于时间的 Slide，并且索引发生变化时才更新
    // 这样不影响没有 startTime 的旧章节的手动翻页
    if (found && targetIdx !== currentSlideIdx) {
      setCurrentSlideIdx(targetIdx)
    }
  }, [currentTime, manifest, currentSectionIdx, currentSlideIdx])

  // 渲染
  if (loading) {
    return <div className="loading">加载中...</div>
  }

  if (!manifest) {
    return <div className="loading">无法加载数据</div>
  }

  const currentSection = manifest.sections[currentSectionIdx]
  const currentSlide = currentSection?.slides[currentSlideIdx]
  const audioSrc = currentSection?.audio ? `/${currentSection.audio}` : null

  return (
    <div className="app-container">
      {/* 章节选择器 */}
      <div className="section-selector">
        {manifest.sections.map((section, idx) => (
          <button
            key={section.id}
            className={`section-tab ${idx === currentSectionIdx ? 'active' : ''}`}
            onClick={() => setCurrentSectionIdx(idx)}
          >
            {section.title}
          </button>
        ))}
      </div>

      {/* 主内容区 */}
      <div className="main-content">
        <div className="slide-area">
          <SlideRenderer
            slide={currentSlide}
            subtitles={subtitles}
            currentTime={currentTime}
          />
        </div>
      </div>

      {/* 播放控制 */}
      {audioSrc && (
        <AudioPlayer
          src={audioSrc}
          isPlaying={isPlaying}
          onPlayPause={handlePlayPause}
          onTimeUpdate={setCurrentTime}
          onEnded={handleEnded}
          audioRef={audioRef}
        />
      )}

      {/* 导航按钮 */}
      {currentSection?.slides.length > 0 && (
        <div className="controls-area" style={{ justifyContent: 'center' }}>
          <button
            className="nav-button"
            onClick={handlePrevSlide}
            disabled={currentSlideIdx === 0}
          >
            ← 上一页
          </button>
          <span style={{ color: 'var(--text-muted)', padding: '0 1rem' }}>
            {currentSlideIdx + 1} / {currentSection.slides.length}
          </span>
          <button
            className="nav-button"
            onClick={handleNextSlide}
            disabled={currentSlideIdx === currentSection.slides.length - 1}
          >
            下一页 →
          </button>
        </div>
      )}
    </div>
  )
}

export default App
