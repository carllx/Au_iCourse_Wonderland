---
description: Workflow for adding new visual assets under Scientific Management
---

# adding_visual_assets (如何添加新视觉素材)

当您在脚本 (`03_Scripts`) 中有了使用新图片的灵感时，**请不要直接去网上找图**。
遵循以下“科学管理”流程，确保自动化管线畅通。

## 1. 意图阶段 (Intent)
首先，在脚本 (`S0x_Transcript.md`) 或大纲 (`Structure_Map.md`) 中写下您的引用 ID。
> "这里我需要一张图，展示多普勒效应..."
> **Draft**: `[SLIDE: S08_Doppler_Effect]`

## 2. 定义阶段 (Spec)
打开 `02_Visuals/Slide_Database.md`，追加定义。没有定义，就没有资产。

```markdown
## S08_Doppler_Effect
*   **Type**: [Diagram]
*   **Concept**: 频率的挤压与拉伸
*   **Visual**: 一辆救护车驶过观察者，声波波前在前方密集，后方稀疏。
```
*(注意：必须指定 `Type`，这也是为了让生成的占位图有正确的颜色)*

## 3. 灰盒阶段 (Greybox)
运行自动化脚本，生成占位符。

```bash
python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
```

*   **Result**: 脚本会自动识别您的新定义 `S08`，并根据结构图将其放入正确的文件夹（如 `02_Visuals/assets/S03_Phase2_Sculpt/S08_Doppler_Effect.png`）。
*   **Color**: 因为 Type 是 `[Diagram]`，生出的图会是 **土黄色** 背景。

## 4. 生产阶段 (Production)
现在整个项目已经“编译通过”了。您可以把这张黄色的 PNG 拖进 Premiere。
当您（或美术）最终画好了这张图，只需：
1.  导出为 `S08_Doppler_Effect.png`
2.  **直接覆盖** 那个黄色的灰盒文件。

## 5. 总结
**Spec -> Code -> Asset**
不要跳过 Spec 直接做 Asset，那是灾难的开始。
