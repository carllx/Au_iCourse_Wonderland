# H5 交互预览系统 (H5 Interactive Preview)

本模块是 Wonderland 项目的交互式课程预览系统，基于 React + Vite 构建。它直接解析项目脚本与资产，提供所见即所得的预览体验。

## 🚀 快速开始

### 1. 快速启动 (推荐)
在项目根目录双击 `start_preview.command`。

### 2. 手动启动
在 `04_Delivery/h5_preview` 目录下运行：
```bash
npm install
npm run sync  # (可选) 强制同步最新脚本与素材
npm run dev
```
打开浏览器访问显示的本地 URL (通常为 `http://localhost:5173`)。

### 3. 同步项目数据
当你修改了 `03_Scripts` 中的脚本、`Slide_Database.md` 或者新增了视觉资产后，运行以下命令刷新 H5 数据：
```bash
npm run sync
```
*(注：该命令执行 `python scripts/parse_slides.py`)*

## 🎨 视觉逻辑 (Visual Logic)

本项目采用 **"Overlay Engine" (叠加引擎)** 逻辑：

1.  **灰盒布局 (Greybox Layout)**: 如果某页 Slide 尚未制作最终美术资产，系统会根据 `Slide_Database.md` 中的 `Type` 自动渲染符合设计规范的 16:9 虚线布局框。
2.  **物理资产覆盖 (Asset Override)**: 
    *   系统会自动检测 `02_Visuals/assets/[SectionID]/[SlideID].png`。
    *   如果文件存在，H5 将自动显示真实图片并隐藏灰盒。
3.  **文字渲染**: 所有 `Text`、`Sub`、`List` 字段由 H5 在顶层渲染，确保内容始终清晰可读。

## 🎧 媒体同步 (Media Sync)

- **音频**: 自动关联 `03_Scripts/tts/` 下的 MP3 文件。
- **字幕**: 解析同名的 SRT 文件，实现毫秒级精准对齐。
- **导航**: 支持章节切换与 Slide 翻页。

## 🛠 维护说明

- **解析逻辑**: 请参考 `scripts/parse_slides.py`。
- **布局定义**: 布局模板硬刻在 `parse_slides.py` 中，与 `scaffold_visual_assets.py` 保持同步。
- **静态资源**: `public/visuals` 是指向项目根目录 `02_Visuals/assets` 的符号链接。

## 🤖 脚本驱动架构 (Script-Driven Architecture) - v1.3

本项目已实现 **"Script-to-Timeline"** 自动化管线。无需人工在 JSON 中手写时间戳。

### 1. 核心组件
| 脚本 | 功能 | 输出 |
| :--- | :--- | :--- |
| **`build_timeline.py`** | **强制对齐引擎**。结合 TTS 音频与脚本锚点，计算 Slide 精确时间。 | 更新 `slides.json` 的 `startTime` |
| **`gen_placeholders.py`** | **占位符生成器**。利用时间信息生成带倒计时的 MP4 占位视频。 | 生成 `visuals/.../*.mp4` |
| **`App.jsx` (Auto-Seek)** | **智能播放器**。监听 `startTime`，实现自动翻页与点击跳转。 | H5 交互行为 |

### 2. 标准工作流 (SOP)
当你修改了脚本 (`.md`) 或重新生成了语音 (`.mp3`) 后，请按顺序运行：

```bash
# 假设你在处理 S03 章节
export SID="S03"

# Step 1: 注入时间轴 (需要 .agent/engine_venv 环境)
../../.agent/engine_venv/bin/python scripts/build_timeline.py $SID

# Step 2: 刷新占位符 (可选，仅当缺乏素材时)
../../.agent/engine_venv/bin/python scripts/gen_placeholders.py $SID
```

### 3. 环境配置
Engine 依赖 Python 库 (`stable-ts`, `openai-whisper`, `ffmpeg-python`)。
环境位于: `../../.agent/engine_venv`

