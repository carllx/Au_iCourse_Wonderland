# 知识：Matplotlib 视觉渲染器最佳实践

**来源**: ADR-007 (S05 Blitting & Clamping 修复)
**适用范围**: `01_MVP_Demo/_Pipeline/renderers/*.py`

## 1. 核心问题 (The Problem)

在 S05 视觉渲染器开发中遇到以下问题：

```python
# ❌ Anti-Pattern: 直接使用音频 RMS 驱动视觉属性
bar.set_alpha(0.3 + rms * 0.5)  # rms 可能 > 1.4，导致 alpha > 1.0
```

**错误信息**: `ValueError: alpha (2.36) is outside 0-1 range`

**根本原因**: 音频 RMS 值的范围是无界的，而 Matplotlib Artist 属性（如 `alpha`, `markersize`）有严格的有效范围。

---

## 2. 解决方案 (The Solution)

### 2.1 强制性值约束 (Clamping)

所有动态属性设置必须使用 `np.clip()`：

```python
# ✅ Approved Pattern
import numpy as np

# Alpha: [0.0, 1.0]
bar.set_alpha(np.clip(0.3 + rms * 0.3, 0.1, 0.95))

# Markersize: 根据视觉设计定义合理范围
dot.set_markersize(np.clip(8 + rms * 5, 5, 25))
```

### 2.2 Blitting 优先

对于帧率敏感的动画渲染 (30 FPS, 450+ frames)，必须使用 `blit=True`：

```python
from matplotlib.animation import FuncAnimation

ani = FuncAnimation(fig, update, frames=n_frames, blit=True, interval=1000//fps)
```

**Blitting 工作原理**:
1.  首次渲染时，保存静态背景（坐标轴、网格）。
2.  后续帧只重绘变化的 Artists。
3.  性能提升可达 **10-20 倍** (8 FPS -> 60+ FPS)。

**Blitting 限制**:
*   动态标题/坐标轴标签需要手动处理。
*   如果需要更改 `ylim`/`xlim`，需要清除 `_blit_cache`。

---

## 3. 代码模板 (Template)

以下是符合规范的 `update` 函数模板：

```python
def update(frame):
    idx = frame * samples_per_frame
    chunk = 1000  # 分析窗口大小
    
    # 获取 RMS
    if idx + chunk >= len(audio_data):
        return artists  # Early return for safety
    
    rms = np.sqrt(np.mean(audio_data[idx:idx+chunk]**2))
    
    # 应用到 Artist (带约束)
    my_bar.set_height(np.clip(rms * 3, 0, 1.0))
    my_dot.set_markersize(np.clip(10 + rms * 20, 5, 30))
    my_patch.set_alpha(np.clip(0.2 + rms * 0.5, 0.1, 0.9))
    
    # 必须返回所有更新的 Artists (用于 blitting)
    return my_bar, my_dot, my_patch
```

---

## 4. 检查清单 (Checklist)

在提交任何 `render_*.py` 前，请确认：

- [ ] 所有 `set_alpha()` 调用均已使用 `np.clip(val, 0.0, 1.0)` 包裹。
- [ ] 所有 `set_markersize()` 调用均已定义合理的上下界。
- [ ] `FuncAnimation` 使用了 `blit=True`。
- [ ] `update` 函数返回了所有变化的 Artists (tuple)。
- [ ] 在动画循环前已调用 `ax.set_ylim()` 或 `ax.set_xlim()` 固定边界。

---
**变更记录**:
*   2026-01-29: 初始版本 (Based on ADR-007)
