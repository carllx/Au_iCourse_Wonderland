# 📸 视觉素材生产指南 (Visual Production Guide)

> **核心原则**: Spec-First (定义先行), Scientific Management (科学管理)

---

## 🚀 快速开始 (Quick Start)

### 完整流程

```
1️⃣ Define  →  2️⃣ Sync Style  →  3️⃣ Produce  →  4️⃣ Replace  →  5️⃣ Preview
在Database    同步视觉定义的    生成符合Bauhaus    合成成品       H5交互验证
中添加条目    CSS和配置         风格的素材
(Yaml SSOT)   (Visual Director)  (AI Gen)
```

---

## 📋 Step 1: Define (定义)

### 1-A. 滑块与素材定义
在 `02_Visuals/Slide_Database.md` 中添加条目。

### 1-B. 风格与配色定义 (SSOT)
在 `.agent/standards/visual_system.yaml` 中定义全局风格。

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

## 🎨 Step 2: Visual Director (风格同步)

**这是确保 H5 和 Python 渲染器风格统一的关键步骤。**

```bash
# 同步 CSS 和 Matplotlib 配置
python .agent/skills/visual-director/scripts/sync_style.py
```

---

## 🤖 Step 3: Produce (AI 素材生成)

使用 **Visual Director** 的增强生成器，它会自动读取 YAML 宪法注入 "Bauhaus/Minimalist" 风格。

```bash
# 生成素材 (自动应用 CINE-BAUHAUS 风格)
python .agent/skills/visual-director/scripts/gen_visual_asset.py S06_Ghost_Math
```

**⚠️ 旧版注意**: 请勿再使用 `validation-suite` 下的旧生成脚本。

---

## 📁 Step 4: 命名与存放

### 目录结构

```
02_Visuals/assets/
├── _Global/                  (Logo, Watermarks)
├── S01_Intro/                (模块 1)
├── S02_Phase1_Purify/        (模块 2)
│   ├── S06_Ghost_Math.png         ← 最终成品

└── ...
```

### 命名规范

| 前缀 | 含义 | 示例 |
|:---|:---|:---|
| `Sxx_` | **最终成品** | `S06_Ghost_Math.png` |
| `ref_` | **参考图** | `ref_S06_inspo.jpg` |

---

## ✨ Step 5: 替换灰盒

1. 将成品**直接覆盖**灰盒文件 (保持文件名不变)
2. 例如: 用最终的 `S06_Ghost_Math.png` 替换灰盒的 `S06_Ghost_Math.png`

---

## 📱 Step 6: Interactive Preview (交互式预览)

静态图片只是第一步，**必须**在 H5 系统中验证素材与音频、字幕的契合度。

### 方式 A: 一键启动 (推荐)
双击项目根目录下的 **`start_preview.command`**。
它会自动同步数据并打开浏览器。

### 方式 B: 命令行启动
```bash
cd 04_Delivery/h5_preview
npm run sync && npm run dev
```

**验证清单**:
1.  **布局 (Layout)**: 图片主体是否被字幕遮挡？
2.  **起止 (Timing)**: 画面出现和消失的时机是否配合语音节奏？
3.  **色彩 (Color)**: 在暗色 UI 背景下，图片是否过于刺眼或融入看不清？

---

## ✅ 验证 (Validation)

```bash
# 检查链接完整性
python .agent/skills/validation-suite/scripts/validate_links.py

# 重新生成缺失的灰盒 (仅当 H5 显示空白时使用)
python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
```

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
