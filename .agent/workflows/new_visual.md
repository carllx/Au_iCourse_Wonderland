---
description: Workflow for adding new visual assets using the unified Visual Director pipeline
---

# adding_visual_assets (如何添加新视觉素材)

当您在脚本 (`03_Scripts`) 中有了使用新图片的灵感时，请遵循以下 **CINE-BAUHAUS 统一工作流**。

## 1. 意图阶段 (Intent)
首先，在脚本 (`S0x_Transcript.md`) 中写下您的引用 ID。

> "这里我需要一张图，展示多普勒效应..."
> **Draft**: `[SLIDE: S08_Doppler_Effect]`

## 2. 定义阶段 (Define)
打开 `02_Visuals/Slide_Database.md`，追加定义。

```markdown
## S08_Doppler_Effect
*   **Type**: [Diagram]
*   **Concept**: 频率的挤压与拉伸
*   **Visual**: Top-down view of an ambulance passing an observer. Wavefronts compressed in front, stretched behind.
*   **AI_Prompt**: `minimalist scientific diagram, doppler effect visualization, bauhaus geometry`
```
*(注意：`AI_Prompt` 是可选的，可以在生成时自动注入风格词，但建议提供主体描述)*

## 3. 生产阶段 (Produce)
使用 **Visual Director** 技能生成素材。它会自动读取 YAML 宪法注入 "Bauhaus" 风格。

```bash
python .agent/skills/visual-director/scripts/gen_visual_asset.py S08_Doppler_Effect
```

*   **Result**: 
    *   脚本会自动读取 `Slide_Database.md` 获取定义。
    *   自动注入 `visual_system.yaml` 中的风格词。
    *   生成的图片保存在 `02_Visuals/assets/Sxx_Module/` 下。

## 4. 预览阶段 (Preview)
一键启动 H5 预览，验证素材与音频的配合。

```bash
./start_preview.command
```
*(或 `npm run dev`)*

## 5. 总结
**Spec (Database) -> Style (YAML) -> Asset (AI)**
不要直接下载网图，那会破坏视觉一致性。
