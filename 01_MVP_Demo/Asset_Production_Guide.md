# 本地音频资产生产指南 (Audio Asset Production Guide)

**更新日期**: 2026-01-30
**架构版本**: 1.3 (Modular + TTS Video Preview)
**参见**: 
- `01_MVP_Demo/ARCHITECTURE_GUIDE.md` (详细命名规范)
- `02_Visuals/README.md` (视觉资产生产与 AI 生成指南)

## 1. 资产清单 (Asset Manifest)

基于新的 **模块化架构** (`_Library/S0x_Module`), 资产分布如下：

### A. S02 净化 (S02_Purify)
| 文件名 | 用途 | 对应脚本 | 版本 |
| :--- | :--- | :--- | :--- |
| **`asset_S02_dirty_heartbeat.wav`** | 真实粉红噪音 + 自然心跳 | `gen_S02_heartbeat.py` | v12 |
| **`asset_S02_heartbeat_subtle.mp4`** | 频谱可视化视频 | `render_S02_spectrum.py` | - |

**v12 更新说明**:
- 使用真实的粉红噪音（宽带，覆盖整个频谱）
- 心跳包含自然的谐波结构（60Hz + 120Hz + 180Hz + 240Hz）
- 能量比例：心跳 : 噪音 = 1.4 : 0.5 ≈ 3 : 1
- 频谱图看起来自然，不再是人工分离的频率

### B. S0X 通用共享 (S0X_Shared)
| 文件名 | 用途 | 描述 |
| :--- | :--- | :--- |
| **`asset_S0X_dry_voice_clean.wav`** | 基准干声 | 干净的人声朗读。 |
| **`asset_S0X_bad_case_demo.wav`** | 问题样本 | 添加了底噪/爆音的脏音频。 |

### C. S03 塑形 (S03_Sculpt)
| 文件名 | 用途 | 对应脚本 |
| :--- | :--- | :--- |
| **`demo_S03_ugly_duckling.wav`** | 丑小鸭演示 (Pitch Up/Chipmunk) | `gen_S03_time_pitch.py` |

### D. S04 空间 (S04_Space)
| 文件名 | 用途 | 对应脚本 |
| :--- | :--- | :--- |
| **`asset_S04_void_ir.wav`** | 虚空IR脉冲 (2.5s) | `gen_S04_void_ir.py` |
| **`contrast_IR_small_closet.wav`** | 对比A: 小衣柜 | `gen_S04_contrast_IRs.py` |
| **`contrast_IR_large_hall.wav`** | 对比B: 大厅 | `gen_S04_contrast_IRs.py` |
| **`contrast_visual_closet.mp4`** | 衣柜可视化 | `render_S04_contrast.py` |
| **`contrast_visual_hall.mp4`** | 大厅可视化 | `render_S04_contrast.py` |
| **`asset_S04_void_visual.mp4`** | 虚空可视化 | `render_S04_decay.py` |
| **`demo_S04_wet_voice.wav`** | 湿声演示 (Mixed) | `gen_S04_wet_demo.py` |

### E. S05 定位 (S05_Position)
| 文件名 | 用途 | 对应脚本 |
| :--- | :--- | :--- |
| **`asset_S05_heartbeat_visceral.wav`** | 内部心跳 (Center) | `gen_S05_panning_assets.py` |
| **`asset_S05_threat_pressure.wav`** | 压迫之墙 (Low/Wall) | `gen_S05_panning_assets.py` |
| **`asset_S05_threat_anxiety.wav`** | 焦虑之刺 (High/Spiral) | `gen_S05_panning_assets.py` |
| **`asset_S05_shadow_self.wav`** | 镜中阴影 (Clean Reverse) | `gen_S05_panning_assets.py` |
| **`demo_S05_spiral_mix.wav`** | 螺旋混音演示 | `gen_S05_panning_assets.py` |
| **`visual_S05_spiral_radar.mp4`** | 动态雷达可视 | `render_S05_panning_visual.py` |

---

## 2. 生产流程 (Pipeline Workflow)

所有生产工具现已移至 `_Pipeline` 目录。

### 场景 1: 重新生成心跳素材 (v12 真实粉红噪音)
```bash
# 运行生成器 (自动覆盖 _Library 中的文件)
python 01_MVP_Demo/_Pipeline/generators/gen_S02_heartbeat.py
```

**生成参数** (v12):
- 心跳: 60Hz 基频 + 谐波 (120Hz, 180Hz, 240Hz)
- 噪音: 真实粉红噪音 (宽带)
- 能量: 心跳 +3dB, 噪音 -6dB
- 比例: 3:1

### 场景 2: 验证降噪可行性
```bash
# 运行验证脚本 (使用 Python 实现降噪)
python 01_MVP_Demo/_Pipeline/verify_noise_reduction.py
```

**验证输出**:
- 原始信号频谱分析
- 降噪后信号频谱分析
- 信噪比改善倍数
- 生成 `asset_S02_cleaned_heartbeat.wav` (Python 降噪结果)

### 场景 3: 渲染可视化视频
```bash
# 运行渲染器 (依赖 matplotlib, ffmpeg)
python 01_MVP_Demo/_Pipeline/renderers/render_S02_spectrum.py --render
```

### 场景 4: 生成 S04 虚空 IR 与可视化
```bash
# 1. 生成音频
python 01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py

# 2. 渲染视频 (需先有音频)
python 01_MVP_Demo/_Pipeline/renderers/render_S04_decay.py

# 3. 生成湿声演示 (Convolution)
python 01_MVP_Demo/_Pipeline/generators/gen_S04_wet_demo.py
```

### 场景 5: 生成 S04 空间对比与 S03 演示
```bash
# S04 衣柜 vs 大厅
python 01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py
python 01_MVP_Demo/_Pipeline/renderers/render_S04_contrast.py

# S03 时间-音调演示
python 01_MVP_Demo/_Pipeline/generators/gen_S03_time_pitch.py
```

### 场景 6: 生成 S05 动态心理声像素材
```bash
# 生成所有音频分轨 (Heartbeat, Pressure, Anxiety, Shadow) 及 Spiral Mix
python 01_MVP_Demo/_Pipeline/generators/gen_S05_panning_assets.py

# 生成螺旋雷达可视化 (Video)
python 01_MVP_Demo/_Pipeline/renderers/render_S05_panning_visual.py
```

### 场景 7: 全课程 H5 交互式预览 (Interactive Preview)
这是验证脚本、音频与视觉契合度的 **终极手段**。

```bash
# 1. 切换到预览目录
cd 04_Delivery/h5_preview

# 2. 同步最新数据 (解析 Structure_Map & Slide_Database)
npm run sync

# 3. 启动预览服务器
npm run dev
```

**验证重点**:
- **灰盒匹配**: 检查虚线框是否符合预期的画面占比。
- **声音对齐**: 听 TTS 语音是否与字幕、Slide 切换点步调一致。
- **素材覆盖**: 确保放入 `02_Visuals/assets` 的图片能够正确显示。

### 场景 8: TTS 视频预览生成 (MP4 Output)
将 `03_Scripts/tts` 目录下的音频和字幕合成为预览视频。

**注意**: 自 v1.4 起，推荐使用 **.wav** 格式以获得更好的兼容性。

#### 1. 提取 TTS 文本
```bash
# 从 markdown 脚本中提取纯文本到 03_Scripts/tts/*.txt
python .agent/skills/validation-suite/scripts/validate_script_length.py --dump-text
```

#### 2. 生成预览
```bash
# 批量生成所有章节的预览视频 (快速模式)
python 01_MVP_Demo/_Pipeline/composers/render_preview.py --all --fast

# 生成单个章节
python 01_MVP_Demo/_Pipeline/composers/render_preview.py --section S01_Intro --fast

# 列出可用的 TTS 文件
python 01_MVP_Demo/_Pipeline/composers/render_preview.py --list
```

**功能特性**:
- **自动回退**: 无视觉素材时生成渐变背景 + 标题（非黑屏）
- **字幕嵌入**: 自动读取同名 `.srt` 文件并烧录字幕
- **快速编码**: `--fast` 使用 ultrafast 预设，大幅加速渲染
- **格式支持**: 优先查找 `.wav` > `.mp3` > `.aac`

**输出位置**: `01_MVP_Demo/_Media/previews/preview_Sxx.mp4`

### 场景 9: Script-to-Timeline 自动化 (Timeline & Placeholders)
这是 **v1.3 新增** 的核心管线，用于自动化处理时间轴和占位符。

```bash
# 1. 自动对齐时间轴 (Force Alignment)
# 解析脚本锚点 -> 听音频 -> 计算精确时间 -> 更新 slides.json
python 04_Delivery/h5_preview/scripts/build_timeline.py S03

# 2. 生成动态占位视频
# 读取时间轴 -> 生成对应时长的倒计时视频 -> 更新 slides.json
python 04_Delivery/h5_preview/scripts/gen_placeholders.py S03
```

**功能特性**:
- **无需人工打点**: 只要在 Markdown 里写好 `[SLIDE: ID]`，时间轴自动生成。
- **动态占位**: 对于暂缺的素材，自动生成 MP4 视频占位，时长精确到毫秒。


---

## 3. S02 心跳素材技术说明

### v12 版本特性

**设计目标**: 生成真实的音频混合，适合 Audition 降噪实验

**技术参数**:
- **心跳信号**:
  - 基频: 60 Hz
  - 谐波: 120 Hz, 180 Hz, 240 Hz
  - BPM: 50
  - 包络: 指数衰减 (exp(-8t))
  - 能量: +3dB (1.4)

- **噪音信号**:
  - 类型: 粉红噪音 (Pink Noise)
  - 频谱: 宽带 (覆盖整个频谱)
  - 能量: -6dB (0.5)

- **混合比例**:
  - 心跳 : 噪音 = 1.4 : 0.5 ≈ 3 : 1

**频谱特征**:
- 低频 (0-200Hz): 心跳主导
- 中高频 (200Hz+): 噪音覆盖
- 整体: 自然混合，无人工分离

**降噪效果** (Python 验证):
- 原始信噪比: ~40-50
- 降噪后信噪比: ~180-200
- 改善倍数: 4-5x

---

## 4. 开发规范 (Development Rules)

1.  **命名即命运**: 
    *   脚本必须是 `gen_Sxx_name.py`。
    *   生成的素材必须是 `asset_Sxx_name.wav`。
2.  **不要手动修改**:
    *   `_Library` 中的 `asset_` 开头的文件通常由脚本生成。如果你手动修改了它，下次运行脚本会被覆盖。
    *   如果是人工录音，请放入 `User_Recordings` 目录。
3.  **版本控制**:
    *   每次重大修改后，在脚本头部更新版本号和说明。
    *   保持 `Asset_Production_Guide.md` 与实际脚本同步。

---

## 5. 快速检查清单 (Checklist)

- [ ] `_Library` 结构清晰，无乱放的文件。
- [ ] 运行 `gen_S02_heartbeat.py` 能成功更新 wav 文件。
- [ ] 运行 `verify_noise_reduction.py` 能验证降噪效果。
- [ ] 运行 `render_S02_spectrum.py` 能成功播放或渲染。
- [ ] 生成的音频在 Audition 中频谱图看起来自然。
- [ ] 运行 `render_preview.py --all --fast` 能批量生成所有章节预览视频。

---

## 6. 故障排除 (Troubleshooting)

### 问题: 降噪后仍有明显噪音
**原因**: 噪音能量太高或频率分离不够
**解决方案**: 
1. 降低噪音能量（修改脚本中的 `noise` 系数）
2. 增加心跳能量（修改脚本中的 `heartbeat` 系数）
3. 重新生成音频

### 问题: 频谱图看起来"假"（完全分离）
**原因**: 使用了带通滤波或高通滤波，导致频率完全分离
**解决方案**: 
1. 使用宽带噪音（粉红噪音或白噪音）
2. 不要对噪音进行过度滤波
3. 确保心跳有自然的谐波结构

### 问题: 心跳声太弱，听不清
**原因**: 心跳能量太低
**解决方案**: 
1. 增加心跳的幅度系数
2. 增加心跳的持续时间
3. 增加心跳的谐波数量
