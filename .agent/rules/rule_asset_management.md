---
trigger: always_on
description: GLOBAL ASSET PROTOCOL: Defines the "Scientific Management" lifecycle for all project assets (Visuals & Audio).
---

# 规则：资产管理协议 (Asset Management Protocol)

**生效范围**: `01_MVP_Demo/`, `02_Visuals/`, `03_Scripts/`

## 1. 核心哲学 (Philosophy)
本项目遵循 **"Spec-First" (定义先行)** 与 **"Scientific Management" (科学管理)** 原则。
*   **No Asset Without Spec**: 任何物理文件（PNG/WAV）出现前，必须先在 SSOT（单一事实来源）中定义。
*   **Decoupled Pipelines**: 艺术创作（Art）与工程实现（Code/Script）必须解耦，通过 **Greyboxing (灰盒)** 机制实现非阻塞并行。

## 2. 单一事实来源 (SSOT)
*   **Visuals**: `02_Visuals/Slide_Database.md`
    *   这是所有视觉内容的唯一真理。
    *   PPT 文字内容 (Text/List) 必须存储于此，而非“烧录”在图片中。
*   **Audio (Tech)**: `01_MVP_Demo/00_Design_Spec_Alice.md`
    *   这是所有音频参数（如 Reverb Decay, Pitch Shift）的唯一真理。
*   **Actions**: `03_Scripts/00_Structure_Map.md`
    *   这是所有课程结构与节奏的唯一真理。

## 3. 命名与目录规范 (Naming & Taxonomy)

### 3.1 视觉资产前缀系统 (Prefix System)
在 `02_Visuals/assets/` 中，文件必须严格遵循以下前缀：

| 前缀 | 全称 | 定义 | 示例 | 处理方式 |
| :--- | :--- | :--- | :--- | :--- |
| **`Sxx_`** | **Slide (Final)** | **[交付物]** 最终出现在屏幕上的画面（或其灰盒占位）。 | `S07_Demonstration.png` | 放入 Timeline |
| **`src_`** | **Source (Raw)** | **[原料]** 原始素材（截图、录屏、实拍）。 | `src_S07_AuditionPanel.png` | 用于合成 Sxx |
| **`ref_`** | **Reference** | **[参考]** 灵感图、网图（无版权）。 | `ref_S11_Balloon_DIY.png` | 仅供美术参考 |
| **`doc_`** | **Document** | **[文档]** 相关的研发笔记、技术说明。 | `doc_S11_Balloon_DIY_Note.md` | 知识库 |

### 3.2 目录结构 (Directory Structure)
严禁使用“状态文件夹”（如 `pending`, `done`, `proxies`）。
必须使用 **“模块卡槽” (Module Slots)**：

```text
02_Visuals/assets/
├── _Global/              (Logo, Watermarks)
├── S01_Intro/            (Module 1)
├── S02_Phase1_Purify/    (Module 2)
│   ├── S06_Ghost_Math.png         (The Dish)
│   └── src_S06_Spectrum.png       (The Ingredient)
└── ...
```

### 3.3 音频资产的基于对象命名 (Object-Based Naming for Audio)
*   **背景 (ADR-006)**: 动态声像资产的位置会随时间变化，因此文件名不应描述其初始位置。
*   **规则**: 命名应描述 **"本质/质感 (Character)"**，而非 **"位置 (Location)"**。
*   **示例**:
    *   ❌ `asset_S05_threat_L.wav` (位置会变)
    *   ✅ `asset_S05_threat_pressure.wav` (质感恒定)

## 4. 生产工作流 (Production Workflow)

### Step 1: Define (意图)
在 `Slide_Database.md` 中创建条目，指定 `Type`（如 `[Concept Art]`, `[UI Graphic]`）。

### Step 2: Greybox (灰盒)
运行自动化脚本生成占位符（Placeholder）：
```bash
python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
```
*   **结果**: 生成带有 ID 和 Type 颜色编码的 1920x1080 PNG。
*   **目的**: 立即打通剪辑管线，确保 `validate_links.py` 通过。

### Step 3: Production (生产)
美术/后期制作最终素材。
*   **成品**: 直接**覆盖** Step 2 生成的 `Sxx_ID.png`。
*   **素材**: 命名为 `src_...` 放入同级目录。

## 5. 质量保证 (Quality Assurance)

### 5.1 结构完整性 (Structural Integrity)
在项目根目录下运行 (Run from Root)：
`python .agent/skills/validation-suite/scripts/validate_links.py`
*   检查：脚本里引用的 ID 是否在 Database 里有定义？
*   检查：Database 里的定义是否在 assets 文件夹里有文件（灰盒或成品）？

### 5.2 创意冒烟测试 (Creative Smoke Test)
**自动化无法检测艺术质量。**
在 Final Review 前，必须进行：
*   **朗读测试**: User 或 Agent 朗读脚本，配合灰盒 PPT 播放。
*   **检查**: 节奏是否拖沓？隐喻是否生硬？“戏感”是否到位？

---
**变更记录**:
*   2026-01-29: 新增 3.3 Object-Based Naming 规范 (Based on ADR-006).
*   2026-01-27: 初始版本 (Based on Research Report & Migration).
