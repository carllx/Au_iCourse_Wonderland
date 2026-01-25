# 本地音频资产生产指南 (Audio Asset Production Guide)

**更新日期**: 2026-01-25
**架构版本**: 1.1 (Modular)
**参见**: `03_MVP_Demo/ARCHITECTURE_GUIDE.md` (详细命名规范)

## 1. 资产清单 (Asset Manifest)

基于新的 **模块化架构** (`_Library/S0x_Module`), 资产分布如下：

### A. S02 净化 (S02_Purify)
| 文件名 | 用途 | 对应脚本 |
| :--- | :--- | :--- |
| **`asset_S02_heartbeat_subtle.wav`** | 真空参照音 (16s) | `gen_S02_heartbeat.py` |
| **`asset_S02_heartbeat_subtle.mp4`** | 频谱可视化视频 | `render_S02_spectrum.py` |

### B. S0X 通用共享 (S0X_Shared)
| 文件名 | 用途 | 描述 |
| :--- | :--- | :--- |
| **`asset_S0X_dry_voice_clean.wav`** | 基准干声 | 干净的人声朗读。 |
| **`asset_S0X_bad_case_demo.wav`** | 问题样本 | 添加了底噪/爆音的脏音频。 |

---

## 2. 生产流程 (Pipeline Workflow)

所有生产工具现已移至 `_Pipeline` 目录。

### 场景 1: 重新生成心跳素材
```bash
# 运行生成器 (自动覆盖 _Library 中的文件)
python 03_MVP_Demo/_Pipeline/generators/gen_S02_heartbeat.py
```

### 场景 2: 渲染可视化视频
```bash
# 运行渲染器 (依赖 matplotlib, ffmpeg)
python 03_MVP_Demo/_Pipeline/renderers/render_S02_spectrum.py --render
```

---

## 3. 开发规范 (Development Rules)

1.  **命名即命运**: 
    *   脚本必须是 `gen_Sxx_name.py`。
    *   生成的素材必须是 `asset_Sxx_name.wav`。
2.  **不要手动修改**:
    *   `_Library` 中的 `asset_` 开头的文件通常由脚本生成。如果你手动修改了它，下次运行脚本会被覆盖。
    *   如果是人工录音，请放入 `User_Recordings` 目录。

---

## 4. 快速检查清单 (Checklist)

- [ ] `_Library` 结构清晰，无乱放的文件。
- [ ] 运行 `gen_S02_heartbeat.py` 能成功更新 wav 文件。
- [ ] 运行 `render_S02_spectrum.py` 能成功播放或渲染。
