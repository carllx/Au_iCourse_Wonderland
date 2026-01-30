# Slide_Database (PPT 内容数据库)

> **Visual Style**: Cinematic, Minimalist Dark Mode, Waveform decorations.

---

## 📋 字段规范 (Field Specification)

每个 Slide 条目应包含以下字段:

| 字段 | 必填 | 说明 |
|:---|:---|:---|
| `Type` | ✅ | 类型标签: `[Concept Art]`, `[UI Graphic]`, `[Motion Graphic]`, `[Stock/Reference]`, `[Diagram]` |
| `Concept` | ✅ | 概念关键词 (中英文) |
| `Visual` | ✅ | 视觉描述 (中文,用于理解) |
| `Search` | 🔍 | 网络搜索关键词 (英文) |
| `AI_Prompt` | 🎨 | 文生图 Prompt (英文,含风格词) |
| `Caption` | 可选 | PPT 上显示的引用/注释 |
| `Text` | 可选 | PPT 上的主标题 |
| `List` | 可选 | PPT 上的列表内容 |

### 🎨 AI_Prompt 模板

```
[主体描述], [风格词], [画质词], [光照词], [构图词]

示例:
"A translucent ghost bird made of digital noise artifacts, floating in pure black void, 
glitch art style, 8K, cinematic lighting, centered composition"
```

### 🔍 Search 模板

```
[主体] [形容词] [场景/背景] site:unsplash.com OR site:pexels.com

示例:
"sound wave visualization abstract dark background site:unsplash.com"
```

---

## S01_Title
*   **Type**: [Motion Graphic]
*   **Text**: 声音的魔术师：Audition 混响与特效实战
*   **Sub**: 智慧课程《数字音频处理》第五章 (Part 2) | 主讲：林昕
*   **Visual**: Audition Logo + Glowing Soundwave.

## S02_BadCase
*   **Type**: [UI Graphic]
*   **Text**: 常见的声音瑕疵
*   **List**:
    *   Hum (嗡嗡声) -> 6.6.7
    *   Click (爆音) -> 6.6.5
    *   **Hiss (宽频底噪) -> 6.6.2 (Today's Focus)**
*   **Visual**: A waveform with red circles highlighting the "dirty" parts.
    *   **Ref**: ![S02_Purify_75pct_NR](./assets/S02_Phase1_Purify/S02_Purify_75pct_NR.png)


## S02b_Toolbox_Flash
*   **Type**: [UI Graphic]
*   **Text**: 声音特效武器库 (Know-How)
*   **List**:
    *   Doppler Shifter (多普勒) -> 6.8.2: 模拟速度感
    *   Guitar Suite (吉他包) -> 6.8.4: 模拟失真/过载
    *   Center Channel Extractor (中置提取) -> 6.9.1: 消除/保留人声
*   **Visual**: Grid of icons representing these tools.

## S03_Concept_Source_Space_Ear (Core Model)
*   **Type**: [Diagram]
*   **Text**: 空间建模三要素
*   **Visual Diagram**:
    *   `[Sound Source/Actor]` ---> `[Box/Space]` ---> `[Ear/Listener]`
*   **Metaphor**: 声音是演员，混响是舞台，声像的观众席。

## S05_Visual_Matrix (Metaphor)
*   **Type**: [Concept Art]
*   **Concept**: 绝对的纯净 (Purify)
*   **Visual**: 极简主义数据艺术。左侧是混乱的粉红噪音粒子（像沙尘暴），右侧是清晰的心跳波形（像发光山脉）。背景是宇宙深空的深蓝色。
*   **Search**: `pink noise visualization vs clean heartbeat waveform, dark blue cosmic background, data art`
*   **AI_Prompt**: `Split screen digital art: LEFT chaotic pink noise particles like sandstorm, RIGHT clean glowing heartbeat waveform like luminous mountain range, deep cosmic blue background, minimalist data visualization style, 8K, cinematic lighting, symmetrical composition`
*   **Ref Image**: *The Matrix* Construct Scene (Neo in white space).
*   **Caption**: "降噪不仅是修复，更是为声音创造纯白画布。"

## S05b_Spectrum (Visual Aid)
*   **Type**: [Motion Graphic]
*   **Concept**: 听见真空 (Visualizing Silence)
*   **Visual**: 动态频谱图。不是冷冰冰的线条，而是像极光的流动。
*   **Overlay**: A 30s Countdown Timer in the center.
*   **Tagline**: "The Pulse of Silence"
*   **Motion**: The spectrum should be flat (showing silence) or showing specific noise frequencies, keeping user attention during the listening blackout.

## S06_Ghost_Math (Metaphor)
*   **Type**: [Concept Art]
*   **Concept**: 修复的代价 (Musical Noise)
*   **Visual**: 一个半透明的、充满噪点的幽灵鸟（Birdies/Artifacts）漂浮在纯黑的背景中。隐喻：过度降噪产生的“数字幽灵”。
*   **Search**: `glitch ghost bird digital artifacts, transparent, pure black void background`
*   **AI_Prompt**: `A translucent ghost bird made of digital noise artifacts and glitch patterns, floating in pure black void, the bird is semi-transparent with visible pixel distortions and audio waveform textures, ethereal and haunting atmosphere, glitch art style, 8K, soft glow lighting, centered composition`
*   **Ref Image**: A semi-transparent "Ghost Bird" (Artifacts) floating in a void.
*   **Caption**: "过度寻求纯净，会召唤出'数字幽灵' (Musical Noise)。"
*   **Metaphor**: 那些被误删的声音灵魂。

## S07_Demonstration (Action)
*   **Type**: [UI Composite]
*   **Concept**: 降噪参数组合拳 (The Combo)
*   **Visual**: Split Screen Design.
    *   **Left**: Audition Noise Reduction Panel (Highlight: 75% Reduction, 30dB).
    *   **Right**: Dennis Gabor's Information Diagram (Hand-drawn style).
*   **Caption**: "在 4096 个频率切片中，寻找信号与噪声的边界。"

## S08_Visual_Alice_Drink (Metaphor)
*   **Type**: [Concept Art]
*   **Concept**: 塑形与变形 (Sculpt)
*   **Visual**: 爱丽丝喝下药水后身体开始变形的瞬间,音频波形与身体轮廓融合
*   **Search**: `Alice in Wonderland drinking potion transformation, surreal, dark fantasy`
*   **AI_Prompt**: `Alice in Wonderland drinking a glowing potion, her body transforming and stretching, audio waveforms merging with her silhouette, dark fantasy surreal style, Tim Burton aesthetic, deep purple and blue tones, 8K, cinematic dramatic lighting, centered composition`
*   **Ref Image**: *Alice in Wonderland* (1951 or 2010), Alice drinking the potion / Giant Alice.
*   **Caption**: "通过变调 (Pitch)，我们改变的不是声音，是角色的物理形态。"

## S07b_Ugly_Duckling
*   **Type**: [Metaphor]
*   **Concept**: 声音的尸体
*   **Visual**: Tiny waveform in a vast black void.
*   **Caption**: "The Ugly Duckling: High-pitched, No Body, Nervous."

## S08b_Tape_Machine
*   **Type**: [Animation]
*   **Concept**: 克洛诺斯的诅咒 (Time/Pitch)
*   **Visual**: Old Reel-to-Reel Tape machine spinning erratically.
*   **Text**: Speed ↑ = Pitch ↑ = Time ↓

## S08c_Pierre_Schaeffer
*   **Type**: [Photo/Historical]
*   **Concept**: 声音对象 (Sound Object)
*   **Visual**: Photo of Pierre Schaeffer (1948) operating turntables.
*   **Text**: "Acousmatic: The sound one hears without seeing the causes behind it."

## S08d_Chipmunk
*   **Type**: [Photo/Historical]
*   **Concept**: 花栗鼠效应
*   **Visual**: Photo of Ross Bagdasarian (1958) with Alvin and the Chipmunks.
*   **Caption**: "Warning: The Chipmunk Trap."

## S08e_Cello_Body
*   **Type**: [Diagram]
*   **Concept**: 共振峰 (Formant)
*   **Visual**: Split image. Left: Vocal Folds (Strings). Right: Cello Body (Vocal Tract).
*   **Highlight**: The "Body" remains constant while "Strings" stretch.

## S08f_Deep_Listening_Body_Soul
*   **Type**: [Text/Minimalist]
*   **Concept**: 深听时刻
*   **Visual**: Pure Black Screen.
*   **Text**: Body vs Soul.

## S11_Visual_RabbitHole (Metaphor)
*   **Type**: [Concept Art]
*   **Concept**: 空间置景 (Space)
*   **Ref Image**: Alice falling down the deep rabbit hole.
*   **Caption**: "混响定义了‘无底深渊’的深度。"

## S11b_Tail_Timer (Visual Aid)
*   **Type**: [Motion Graphic]
*   **Concept**: 捕捉尾音 (Catching the Tail)
*   **Visual**: A high-contrast "Stopwatch" or Digital Counter.
*   **Action**: Counts up from 0s to 5s... then fades out as the sound disappears.
*   **Goal**: Visualize the decay time for the audience.

## S10_Concept_Dry_Wet
*   **Type**: [Diagram/Comparison]
*   **Concept**: 空间的迷思
*   **Visual**: Split Screen.
    *   Left: "Dry: Proximity" (Alice stuck on screen surface).
    *   Right: "Wet: Infinity" (Alice falling into screen depth).

## S11c_Balloon_Cave
*   **Type**: [Diagram]
*   **Concept**: 脉冲响应 (IR)
*   **Visual**: Hand-drawn diagram of a balloon exploding in a cave, showing reflection paths.
*   **Text**: "Impulse Response: The DNA of Space".

## S12_Damping_Curve
*   **Type**: [Chart]
*   **Concept**: 高频阻尼 (Physics)
*   **Visual**: Frequency Response Curve collapsing at high frequencies (Low Pass).
*   **Metaphor**: Diver diving deep, red light disappearing.

## S13_Automation_Dissolution
*   **Type**: [UI/Screenshot]
*   **Concept**: 灵魂出窍
*   **Visual**: Multitrack Envelope Automation.
*   **Curve**: Blue line rising from 0% to 75%.
*   **Text**: "Dissolution".

## S14_Visual_Inception (Metaphor)
*   **Type**: [Stock/Reference]
*   **Concept**: 空间折叠/定位 (Position)
*   **Ref Image**: *Inception* (City folding up).
*   **Caption**: "立体声扩展 (Stereo Expand) 让现实扭曲，创造包裹感。"
*   **Overlay**: Animated headphone icon + Radial Spectrum extending left/right.

## S16_Summary_Loop
*   **Type**: [Diagram]
*   **Concept**: 剧场谢幕
*   **Diagram**: Circle Flow
    1.  Purify (此在)
    2.  Sculpt (彼在)
    3.  Space (何处)
    4.  Position (何方)
*   **Text**: 每一个参数，都是一种立场。


## S19_Murch_Rule_of_Six
*   **Type**: [Diagram]
*   **Concept**: 剪辑六法则 (Philosophy)
*   **Visual**: A Pyramid Diagram.
    1.  **Emotion (51%)** - Top
    2.  **Story (23%)**
    3.  **Rhythm (10%)**
    4.  **Eye Trace (7%)**
    5.  **2D Plane (5%)**
    6.  **3D Space (4%)**
*   **Highlight**: "Emotion" is the biggest block.

## S17_Homework
*   **Type**: [Task Card]
*   **Title**: 课后挑战：逃离麦克风 (Escape the Mic)
*   **Task**: 录制一段干声，利用四步法（净化-塑形-置景-定位）将其“异化”。
*   **Requirement**: 提交 MP3 + 200字创作说明（解释你的导演决策）。
