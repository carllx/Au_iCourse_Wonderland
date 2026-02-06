---
name: Visual Director (Visual System Enforcer)
description: Enforces the CINE-BAUHAUS visual style across H5, Python Renderers, and AI Generation.
---

# 🎨 Visual Director

**Visual Director** 是项目的视觉守护者。它确保所有生成的视觉内容（网页、图表、AI 插画）都严格遵循 `.agent/standards/visual_system.yaml` 定义的宪法。

## 核心能力 (Capabilities)

### 1. 风格同步 (Style Sync)
将 YAML 宪法编译为各个子系统的原生配置代码。

```bash
# 运行同步 (生成 CSS 和 Python Config)
python .agent/skills/visual-director/scripts/sync_style.py
```

*   **Output 1**: `04_Delivery/h5_preview/src/styles/theme.css` (Web UI)
*   **Output 2**: `01_MVP_Demo/_Pipeline/lib/style_config.py` (Matplotlib)

### 2. 素材生成 (Asset Generation)
带有审美自觉的 AI 生成器。

```bash
# 生成素材 (自动读取 YAML 注入 Bauhaus 风格)
python .agent/skills/visual-director/scripts/gen_visual_asset.py S06_Ghost_Math
```

## 维护指南 (Maintenance)

*   **修改配色**: 严禁直接修改 CSS 或 Python 文件。请修改 `.agent/standards/visual_system.yaml`，然后运行 `sync_style.py`。
*   **新增尺寸**: 在 YAML 的 `dimensions` 节点添加新的类别。

## 依赖 (Dependencies)
*   `pyyaml`: 解析 YAML
*   `google-generativeai`: AI 生成
