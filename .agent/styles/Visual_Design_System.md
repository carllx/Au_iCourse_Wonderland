# Visual Design System (视觉设计宪法)

> **Status**: Active (v2.0)
> **Theme**: DAW Dark Cinematic (数字音频工作站暗黑电影感)
> **Core Metaphor**: "The Interface is an Instrument" (界面即乐器)

## 1. Color Palette (色彩系统)

| Component | Hex Code | Purpose | Metaphor |
| :--- | :--- | :--- | :--- |
| **Background** | `#1A1A1A` | Canvas Background | 深石墨 (Dark Graphite) - 减少视觉疲劳 |
| **Waveform** | `#40E0D0` | Dynamic Signal | 波谱青 (Spectrum Cyan) - 信号的流动 |
| **Envelope** | `#FF007F` | Control Voltage | 荧光玫红 (Cyber Pink) - 能量的边界 |
| **Grid/Sub** | `#444444` | Structural Guide | 枪灰色 (Gunmetal) - 设备的刻度 |
| **Highlight** | `#FFD700` | Narrative Focus | 叙事金 (Narrative Gold) - 关键的洞察 |

## 2. Typography (排版系统)

> **Primary Font**: `MiSans` (Xiaomi)

*   **Display / Titles**: `MiSans Medium`
    *   Usage: 图表标题, 核心参数 ($T_{60}$)
*   **Body / Data**: `MiSans Regular` / `Normal`
    *   Usage: 坐标轴数值, 辅助标签 ($ms$, $Hz$)
*   **Narrative Layer**: `MiSans Medium` + Glow
    *   Usage: 情感化引导语 (e.g., "时间的遗物")

## 3. Visual Components (组件规范)

### A. Waveform (波形)
*   **Style**: Solid Line + Alpha Fill OR Neon Stroke.
*   **Effect**: 必须带有微弱的外发光 (Neon Glow) 模拟示波器质感。
*   **Opacity**: `alpha=0.8`。

### B. Envelope (包络)
*   **Style**: Dashed or Saturated Solid Line.
*   **Behavior**: 始终位于波形之上，引导视线。

### C. Meter Bar (电平表)
*   **Style**: Vertical Gradient (Green -> Yellow -> Red).
*   **Feedback**: 且必须具备 Peak Hold (峰值保持) 功能。

### D. Narrative Pivot (叙事转场)
*   **Logic**: 当技术指标达到关键阈值 (e.g., $T_{60}$ Point) 时，UI 必须发生物理变化。
    *   *Text Transformation*: "Decay: 2.5s" -> "时间的遗物".
    *   *Visual Marker*: 闪烁 (Flash) + 幽灵残留 (Ghosting).

## 4. Interaction Rules (交互准则)

1.  **No Naked Numbers**: 任何关键数据旁边必须伴随叙事解释。
2.  **Audio-Visual Sync**: 视觉的 Attack 必须与听觉的 Attack 帧级对齐。
3.  **Process over Result**: 动画必须展示“变化的过程”，而不仅仅是“最终的形态”。
