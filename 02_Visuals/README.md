# 📸 视觉素材生产指南 (Visual Production Guide)

> **核心原则**: Spec-First (定义先行), Scientific Management (科学管理)

---

## 🚀 快速开始 (Quick Start)

### 完整流程

```
1️⃣ Define   →   2️⃣ Greybox   →   3️⃣ Collect   →   4️⃣ Produce   →   5️⃣ Replace
在Database     生成灰盒占位     搜索/生成素材     合成成品        覆盖灰盒
中添加条目
```

---

## 📋 Step 1: Define (定义)

在 `Slide_Database.md` 中添加条目:

```markdown
## S06_Ghost_Math
*   **Type**: [Concept Art]
*   **Concept**: 修复的代价 (Musical Noise)
*   **Visual**: 一个半透明幽灵鸟漂浮在纯黑背景中
*   **Search**: `glitch ghost bird digital artifacts, transparent, pure black void`
*   **AI_Prompt**: `A translucent ghost bird made of digital noise artifacts, floating in pure black void, glitch art style, 8K, cinematic lighting`
*   **Caption**: "过度降噪会召唤出'数字幽灵'"
```

### 必填字段

| 字段 | 说明 |
|:---|:---|
| `Type` | `[Concept Art]`, `[UI Graphic]`, `[Motion Graphic]`, `[Stock/Reference]`, `[Diagram]` |
| `Concept` | 概念关键词 (中英文) |
| `Visual` | 视觉描述 (中文,用于理解) |

### 生产字段 (二选一或都填)

| 字段 | 用途 |
|:---|:---|
| `Search` | 网络搜索关键词 (英文) |
| `AI_Prompt` | 文生图 Prompt (英文,含风格词) |

---

## 🔲 Step 2: Greybox (生成灰盒)

```bash
python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
```

**结果**: 自动在 `assets/Sxx_Module/` 下生成 1920x1080 灰盒占位图

**作用**: 让剪辑管线不阻塞,可以先用灰盒拼视频

---

## 🔍 Step 3: Collect (获取素材)

### 方式 A: 网络搜索

使用 `Search` 字段中的关键词在以下网站搜索:
- [Unsplash](https://unsplash.com) (免费高清)
- [Pexels](https://pexels.com) (免费商用)
- [Freepik](https://freepik.com) (需标注来源)
- Google Images (注意版权)

### 方式 B: 文生图

使用 `AI_Prompt` 字段中的 Prompt:
- [Midjourney](https://midjourney.com)
- [DALL-E](https://openai.com/dall-e)
- [Stable Diffusion](https://stability.ai)

### 方式 C: 截图/录屏

- Audition 界面截图
- 操作过程录屏

---

## 📁 Step 4: 命名与存放

### 目录结构

```
02_Visuals/assets/
├── _Global/                  (Logo, Watermarks)
├── S01_Intro/                (模块 1)
├── S02_Phase1_Purify/        (模块 2)
│   ├── S06_Ghost_Math.png         ← 最终成品
│   ├── src_S06_ghost_bird_ai.png  ← 文生图原图
│   └── src_S06_diagram_web.jpg    ← 网络搜索
└── ...
```

### 命名规范

| 前缀 | 含义 | 示例 |
|:---|:---|:---|
| `Sxx_` | **最终成品** | `S06_Ghost_Math.png` |
| `src_` | **原始素材** | `src_S06_ghost_bird_ai.png` |
| `ref_` | **参考图** | `ref_S06_inspo.jpg` |

### 来源后缀 (用于 `src_` 文件)

| 后缀 | 含义 |
|:---|:---|
| `_ai` | 文生图 |
| `_web` | 网络搜索 |
| `_cap` | 截图 |
| `_rec` | 录屏 |
| `_photo` | 实拍 |

**完整格式**: `src_Sxx_[描述]_[来源].ext`

---

## ✨ Step 5: 替换灰盒

1. 将成品**直接覆盖**灰盒文件 (保持文件名不变)
2. 例如: 用最终的 `S06_Ghost_Math.png` 替换灰盒的 `S06_Ghost_Math.png`

---

## ✅ 验证

```bash
# 检查链接完整性
python .agent/skills/validation-suite/scripts/validate_links.py

# 重新生成缺失的灰盒
python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
```

---

## 🤖 AI 自动生成工具 (AI Asset Generator)

使用 `gen_visual_asset.py` 可以根据 Slide_Database 中的 AI_Prompt 自动生成图片。

### 1. 环境配置 (Setup)

**A. 安装依赖**:
```bash
pip install google-generativeai
```

**B. 配置 API Key**:
在项目根目录创建 `.env` 文件 (不要上传到 Git):

```ini
# Private Configuration
API_BASE_URL=http://127.0.0.1:8045/v1
API_KEY=sk-your-key-here
API_MODEL=gemini-3-pro-image
```

### 2. 使用方法 (Usage)

脚本位置: `.agent/skills/validation-suite/scripts/gen_visual_asset.py`

```bash
# 列出所有可生成的 Slide
python .agent/skills/validation-suite/scripts/gen_visual_asset.py --list

# 生成单个 Slide (保存为 src_..._ai.png)
python .agent/skills/validation-suite/scripts/gen_visual_asset.py S06_Ghost_Math

# 生成并自动覆盖灰盒 (Deploy Mode)
python .agent/skills/validation-suite/scripts/gen_visual_asset.py S06 --deploy

# 自定义 Prompt 生成
python .agent/skills/validation-suite/scripts/gen_visual_asset.py S06 --prompt "A ghost bird"

# 批量生成所有有 Prompt 的 Slide
python .agent/skills/validation-suite/scripts/gen_visual_asset.py --all
```

**⚠️ 注意**: 
- 需要在 `Slide_Database.md` 中为 Slide 添加 `AI_Prompt` 字段。
- 确保本地 Antigravity API 服务 (端口 8045) 已启动。
- 确保 API 后台 ("External Providers") 已配置 Google API Key。

---

## 🎨 AI_Prompt 模板

```
[主体描述], [风格词], [画质词], [光照词], [构图词]
```

**示例**:
```
A translucent ghost bird made of digital noise artifacts, 
floating in pure black void, 
glitch art style, 
8K, cinematic lighting, 
centered composition
```

**常用风格词**:
- `minimalist`, `cinematic`, `glitch art`, `data visualization`
- `concept art`, `digital painting`, `vector illustration`

**常用画质词**:
- `8K`, `high detail`, `sharp focus`, `professional photography`

---

## 📚 相关文档

- [Slide_Database.md](./Slide_Database.md) - 视觉内容定义 (SSOT)
- [rule_asset_management.md](../.agent/rules/rule_asset_management.md) - 完整命名规范
- [render_preview.py](../01_MVP_Demo/_Pipeline/composers/render_preview.py) - 章节预览生成器

## 🗂️ 目录结构 (2026-01-30 更新)

```
项目根目录/
├── 01_MVP_Demo/
│   ├── _Library/           # 音频资产
│   ├── _Media/             # 视频资产 (录屏)
│   │   ├── recordings/     # 教师操作演示
│   │   └── previews/       # 自动生成的预览
│   └── _Pipeline/
│       ├── generators/     # 音频生成
│       ├── renderers/      # 素材可视化
│       └── composers/      # 章节合成 [NEW]
├── 02_Visuals/
│   ├── Slide_Database.md   # SSOT
│   └── assets/Sxx_Module/  # 模块卡槽
├── 03_Scripts/
│   ├── Sxx_Name.md         # 逐字稿
│   └── tts/                # TTS 输出 [NEW]
│       ├── Sxx_Name.wav
│       └── Sxx_Name.srt
└── .agent/
    └── rules/              # 规范文件
```
