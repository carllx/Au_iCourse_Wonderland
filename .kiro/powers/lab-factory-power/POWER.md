---
name: Lab Factory
description: Adobe Audition automation toolkit for audio asset generation and lab
  setup
keywords:
- audition
- automation
- audio
- jsx
- extendscript
- asset-generation
---

# Lab Factory

## Overview

> **← 来源**: `.agent/manifest.json` → `skills[id="audition-automation"]`

## 概述

| 属性 | 值 |
|-----|-----|
| **ID** | `audition-automation` (原 `lab-factory`) |
| **状态** | ✅ Active |
| **触发词** | /setup-lab, 自动化构建, 初始化环境, 导入素材, 创建轨道 |
| **描述** | Adobe Audition 通用自动化工具包。提供一套原子化的 API 库 (`Audition.jsx`) 用于脚本化控制 Audition，以及一个用于快速构建实验场景的通用构建器 (`Universal_Lab_Builder.jsx`)。 |

## 核心架构：工具包 (Toolkit)

本技能的核心不再是脚本，而是 **Lib**。所有的能力都封装在 stateless 的 `.jsx` 库中。

### [Audition.jsx](file:///lib/Audition.jsx)
原子能力库，提供以下命名空间：

*   `Audition.IO`
    *   `importFile(path)`: **智能兼容导入 (Smart Import)**。
        *   **Audition 2024+**: 自动检测并使用 `new DocumentOpenParameter()` 封装路径，解决 `Illegal Parameter` 错误。
        *   **Legacy**: 对旧版本保留 `app.openDocument(string)` 回退。
        *   **Nuclear Fix**: 对 `.sesx` 会话文件，若 API 均失败，尝试 OS 级打开。
        *   对音频素材：如果所有策略失败，**返回 null** 以触发手动导入提示。
*   `Audition.Session`
    *   `findFirst()`: 查找首个多轨会话。
    *   `openTemplate(path)`: 打开模板文件。
*   `Audition.Track`
    *   `getOrCreate(session, index)`: 获取或创建指定索引的轨道。
        *   **Safe-Fail**: 如果 `audioTracks.add()` 崩溃 (Audition 2024 Bug)，捕获异常并返回 `null`。开发逻辑应处理此 `null`。
    *   `setControls(track, mute, solo)`: 设置轨道状态。
*   `Audition.Clip`
    *   `addToTrack(track, doc, time)`: 将素材放置到时间轴。
    *   `setColor(clip, colorObj)`: 设置颜色。
*   `Audition.Markers`
    *   `addCycle(session, name, start, duration)`: 添加循环标记。
*   `Audition.State`
    *   `getOpenDocuments()`: 获取当前所有打开文档的列表（包含 Name, Ref, Path, Type）。
    *   `closeAll(force)`: **强制清理工作区**。
        *   使用多重回退策略（`close`, `closeDocument`, `activeDocument` 切换）清除所有文档。
        *   `force=true` 时不保存更改。
*   `Audition.Log` (New)
    *   `sentinel(msg)`: **静默日志输出**。
        *   将 JSON 或字符串写入标准监控文件 `logs/sentinel_simple.txt`。
        *   配合 `fast_run.sh` 使用，可实现无弹窗 (`no-alert`)、无盲目等待 (`no-sleep`) 的快速执行。

## 场景构建器 (Universal Lab Builder)

*   **定义**: `lib/Universal_Lab_Builder.jsx`
*   **角色**: Toolkit 的消费者 (Consumer)。
*   **用途**: 为课程实验提供一个简便的 JSON 驱动的构建方式。它解析 manifest 对象，然后调用 `Audition.Key` API 执行操作。

## 🚀 高效调试指南 (Fast Debug Protocol)

为了避免 `Alert` 弹窗和 `Sleep` 盲等，请遵循以下开发模式：

1.  **脚本输出**:
    在脚本末尾使用 `Audition.Log.sentinel(resultObject)` 输出结果。
    ```javascript
    try {
        // ... logic ...
        Audition.Log.sentinel({status: "success", data: ...});
    } catch(e) {
        Audition.Log.sentinel({status: "error", msg: e.message});
    }
    ```
2.  **快速执行**:
    使用 `fast_run.sh` 启动脚本。它会监控日志文件并在写入完成时立即返回。
    ```bash
    ./fast_run.sh your_script.jsx
    ```

## 使用策略 (Manifest-Include)

**不要直接运行此目录下的脚本。** 这里的代码是库 (Library)，不是可执行文件。

### 正确的开发流程：
1.  **在 `docs/course_materials/` 下创建脚本** (例如 `Setup_MyLab.jsx`)。
2.  **引用工具包**:
    ```javascript
    #include "../../../../../.agent/skills/lab-factory/lib/Universal_Lab_Builder.jsx" // 引用构建器
    // 或者
    #include "../../../../../.agent/skills/lab-factory/lib/Audition.jsx" // 直接引用库
    ```
3.  **编写逻辑**:
    *   **方式 A (推荐)**: 定义 manifest 对象并调用 `UniversalLabBuilder.build(manifest)`.
    *   **方式 B (高级)**: 直接调用 `Audition.IO.importFile(...)` 等 API 编写自定义逻辑。

## 📌 依赖文件

- [lib/Audition.jsx](file://lib/Audition.jsx) - **核心原子库**
- [lib/Universal_Lab_Builder.jsx](file://lib/Universal_Lab_Builder.jsx) - 通用场景构建器
- [lib/env_context.jsx](file://lib/env_context.jsx) - 环境上下文解析
- [lib/time_utils.jsx](file://lib/time_utils.jsx) - 时间单位转换工具

## ⚠️ 已知局限 (Known Limitations)

基于 Adobe Audition ExtendScript API 的底层特性，本技能包**不支持**以下操作。请勿尝试编写相关脚本，以免浪费时间。

1.  **视图控制 (View Control)**
    *   ❌ **不支持**: 切换波形视图 (Waveform) / 频谱视图 (Spectral Display)。
    *   ❌ **不支持**: 缩放 (Zoom) 或滚动 (Scroll) 视图。
    *   *原因*: API 未暴露 View 对象或属性。

2.  **工具交互 (Tool Interaction)**
    *   ❌ **不支持**: 切换鼠标工具 (如 Spot Healing Brush, Razor Tool)。
    *   ❌ **不支持**: 模拟鼠标点击或涂抹操作。
    *   *原因*: ExtendScript 仅支持数据层 (Data Layer) 操作，不支持 GUI 模拟。

3.  **效果器交互 (Interactive Effects)**
    *   ❌ **不支持**: 打开效果器面板并等待用户输入 (如 "Output Noise Only")。
    *   *原因*: 脚本调用 Effect 时为阻塞式直接执行，无法暂停脚本等待 UI 交互。

## 🛡️ 鲁棒性协议 (Robustness Protocol)

为了应对 Audition API 的不稳定性，本技能采用 **"红绿灯 (Traffic Light)"** 降级策略：

| 状态码 | 颜色 | 含义 | 行为模式 |
|-------|-----|-----|---------|
| **200** | 🟢 Green | 全自动成功 | 脚本静默完成所有操作。 |
| **4xx** | 🟡 Yellow | **半自动降级** | 脚本**不报错**，而是生成 `MANUAL_GUIDE.md` 弹窗。例如："导入失败，请手动拖入 assets/bgm.wav"。 |
| **5xx** | 🔴 Red | 致命阻断 | 宿主崩溃或 API 彻底不可用。脚本安全退出并记录日志。 |

> **最佳实践**: 将脚本定位为 **"Hybrid Navigator" (混合导航者)**。
> - 能自动做的（如建轨道、打标记），脚本自动做。
> - 做不到的（如复杂 Effect 设置、不稳定的导入），脚本生成"操作指引"，让用户来做。
> - **永远不要让脚本在报错中崩溃**。

## Script References

The Lab Factory Power uses external JSX libraries that remain in their original locations. These scripts are referenced here with complete usage instructions.

### create_template.jsx

**Purpose**: create_template.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/create_template.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/create_template.jsx

```

### time_utils.jsx

**Purpose**: JSX script

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/time_utils.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/time_utils.jsx

```

**Dependencies**:
- time_utils.jsx

### Universal_Lab_Builder.jsx

**Purpose**: Universal_Lab_Builder.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/Universal_Lab_Builder.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/Universal_Lab_Builder.jsx

```

**Dependencies**:
- env_context.jsx
- Audition.jsx

### env_context.jsx

**Purpose**: EnvContext - 环境上下文解析器

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/env_context.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/env_context.jsx

```

**Dependencies**:
- lib/env_context.jsx

### Audition.jsx

**Purpose**: Audition.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/Audition.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/lib/Audition.jsx

```

**Dependencies**:
- Audition.jsx

### test_toolkit_logged.jsx

**Purpose**: test_toolkit_logged.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/test_toolkit_logged.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/test_toolkit_logged.jsx

```

**Dependencies**:
- ../lib/env_context.jsx
- ../lib/Audition.jsx

### test_toolkit.jsx

**Purpose**: test_toolkit.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/test_toolkit.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/test_toolkit.jsx

```

**Dependencies**:
- ../lib/env_context.jsx
- ../lib/Audition.jsx

### probe_api_methods.jsx

**Purpose**: probe_api_methods.jsx

**Location**: `/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/probe_api_methods.jsx`

**Usage**:

```bash

# Run via Adobe Audition or include in manifest

# Location: /Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/.agent/skills/lab-factory/scripts/probe_api_methods.jsx

```

## Rules and Conventions

### MVP Demo Architecture Guidelines

# MVP Demo Architecture Guidelines

When working within `01_MVP_Demo`, you **MUST** follow the architecture and naming conventions defined in:
`01_MVP_Demo/ARCHITECTURE_GUIDE.md`

Key highlights:
- **Scripts**: `_Pipeline/generators/` (e.g. `gen_S02_heartbeat.py`)
- **Assets**: `_Library/S0x_ModuleName/` (e.g. `asset_S02_heartbeat.wav`)
- **No generic names**: Avoid `utils.py`, `assets/`, `tools/`.

## Knowledge Base

### Audition Technical Skills Index

# Audition Technical Skills Index

This knowledge base maps "Director's Intent" to "Technical Operations" based on the project's textbook.

## 1. Noise Reduction & Restoration (净化)
*   **Concept**: Removing Hiss, Hum, Clicks.
*   **Reference**: `数字音频编辑Audition实用教程-混响-2md/6.6 降噪_恢复类效果器.md`
    *   *Key Tech*: Capture Noise Print (捕捉噪声样本), Noise Reduction Process (降噪处理).
    *   *Case Study*: `数字音频编辑Audition实用教程-混响-2md/6.11 综合案例——降噪处理.md`

## 2. Reverb & Space (空间)
*   **Concept**: Simulating physical environments.
*   **Reference**: `数字音频编辑Audition实用教程-混响-2md/6.7 混响类效果器.md`
    *   *Key Tech*: Convolution Reverb (卷积混响).

## 3. Time & Pitch (塑形)
*   **Concept**: Altering voice character (Monster vs Elf).
*   **Reference**: `数字音频编辑Audition实用教程-混响-2md/6.10 时间与变调类效果器.md`
    *   *Key Tech*: Pitch Shifter (变调器).

## 4. Stereo Imagery (定位)
*   **Concept**: Width and Placement.
*   **Reference**: `数字音频编辑Audition实用教程-混响-2md/6.9 立体声声像类效果器.md`
    *   *Key Tech*: Stereo Expander (立体声扩展).

## Troubleshooting

### Common Issues

1. **Import failures**: If `Audition.IO.importFile()` fails, the script will generate a `MANUAL_GUIDE.md` with instructions for manual import. This is part of the Traffic Light protocol (4xx status).

2. **Track creation failures**: If `Audition.Track.getOrCreate()` returns null, this indicates an Audition 2024 API bug. Handle this gracefully in your scripts.

3. **Fast debug**: Use `fast_run.sh` with `Audition.Log.sentinel()` to avoid alert popups and blind sleep waits during development.