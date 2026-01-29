# 架构决策记录 (ADR)

本文档记录关键技术决策背后的“原因”。未来的 Agent **严禁**在未经用户批准的情况下撤销这些更改。

---

## ADR-001: MVP 演示的模块化架构
*   **状态**: Accepted (2026-01-25)
*   **背景**: 项目以前只有平铺的 `tools` 和 `assets` 文件夹，导致“脚本 A”和“资产 B”之间的关系混乱。
*   **决策**: 
    1. 拆分为 `_Pipeline` (代码) 和 `_Library` (数据)。
    2. 强制执行严格的 `[Type]_[Module]_[Name]` 命名规范 (例如 `gen_S02_heartbeat.py` -> `asset_S02_heartbeat.wav`)。
*   **后果**: 
    *   (+) 所有权清晰。
    *   (-) 需要 Agent 遵循正则规则。

---

## ADR-002: 指数级音频淡出 (Exponential Audio Fade)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 线性音量淡出听起来很突兀，因为人类听觉是对数关系 (`dB`)。
*   **决策**: 所有音频生成器脚本必须使用 **指数淡出** (dB 线性) 逻辑进行过渡。
*   **代码模式**: `np.logspace(0, -3, length)` (从 1.0 淡出到 0.001)

---

## ADR-003: 线性频率可视化 (Linear Frequency Visualization)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 对于 S02 中的“迷雾/Fog”隐喻，对数刻度将高频噪声压缩成了一条细线。
*   **决策**: 专门针对 `render_S02_spectrum.py`，我们必须使用 **线性频率刻度** (0-16kHz)，使噪声在视觉上充满屏幕。
*   **限制**: 常规音频分析通常需要对数刻度。这是为了“Fog”隐喻所做的艺术性例外。

---

## ADR-004: 采用智能鉴赏课程模式 (Smart Course)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 原计划包含学生“实验室提交”。然而，用户澄清这是一个“智能课程”，学生专注于 *体验* 和 *决策*，而不是文件导出。
*   **决策**: 
    1.  **无家庭作业**: 从教学大纲中删除所有关于学生提交（如 MP3 导出）的要求。
    2.  **安德森叙事 (Anderson Narrative)**: 所有技术参数必须由叙事隐喻（“灵魂映射”）证明。禁止纯技术解释（例如“为了去噪”）；必须框架化为叙事行动（例如“为了驱逐现实”）。
*   **后果**: 
    *   (+) 更高的参与度，减少学生的阻力。
    *   (-) 验证脚本 (如 `validate_submission.py`) 现已过时，应忽略或删除。

---

## ADR-005: 语境感知的资产合成 ("语义大于信号")
*   **状态**: Accepted (2026-01-25)
*   **背景**: 
    *   最初尝试使用随机噪声生成器生成“坏损案例”音频 (Hum/Click/Hiss) 未能满足教学需求。
    *   随机的 Click 听起来很假；标准语谱图未能显示低频 Hum。
    *   用户反馈强调“噪声必须与信号相关” (例如，Click 发生在爆破音处)。
*   **决策**: 
    *   **放弃随机性**: 所有合成伪影必须是 **语境感知 (Context-Aware)** 的。
        *   *示例*: Click 现在由语音包络上的 `signal.find_peaks` (爆破音) 触发。
    *   **强制视觉语义**: 可视化必须使用 **对数刻度 (Log Scale)** 来显示 50Hz Hum。
    *   **叙事标签**: 所有 UI 标签必须使用 `MetricTranslator` 协议 (中文叙事术语)，禁止使用原始的技术英文。
*   **后果**: 
    *   资产不再只是“技术文件”，而是“叙事道具”。
    *   生成器脚本更加复杂 (需要信号分析，而不仅是合成)。
    *   视觉验证现在是强制性的 (不能仅相信代码正确性；必须验证 *可见性*)。

---

## ADR-006: 基于对象的资产命名 (Object-Based Naming)
*   **状态**: Accepted (2026-01-29)
*   **来源**: S05 动态声像开发会话
*   **背景**: 
    *   S05 的 "Threats" 最初命名为 `_L.wav` (Left) 和 `_R.wav` (Right)。
    *   当需求升级为"动态声像"（Spiral Pan + Approaching Wall）时，L/R 的命名变得具有误导性，因为声音不再静止在特定位置。
*   **决策**: 
    *   **命名应描述"本质/质感 (Character)"，而非"位置 (Location)"**。
    *   `_L.wav` -> `_pressure.wav` (The Wall, 低频逼近)
    *   `_R.wav` -> `_anxiety.wav` (The Needle, 高频螺旋)
    *   **规则**: 位置是一个 *状态 (State)*，本质是一个 *身份 (Identity)*。文件名应反映身份。
*   **后果**: 
    *   (+) 文件名自解释，无论其在混音中的动态位置如何。
    *   (+) 与 "Object-Based Audio" 的行业术语一致。
    *   (-) 需要回溯性地重命名旧资产。

---

## ADR-007: 动态可视化的 Blitting 与值约束
*   **状态**: Accepted (2026-01-29)
*   **来源**: S05 视觉渲染器 Bug 修复
*   **背景**: 
    *   `render_S05_panning_visual.py` 在运行时因 `ValueError: alpha is outside 0-1 range` 崩溃。
    *   原因是 `set_alpha(0.3 + wall_rms * 0.5)` 未对音频 RMS 值进行上限约束。
*   **决策**: 
    1.  **强制性值约束 (Clamping)**: 所有 Matplotlib Artist 属性设置器（`set_alpha`, `set_markersize`）必须使用 `np.clip()` 确保值在有效范围内。
    2.  **Blitting 优先**: 对于帧率敏感的动画渲染，必须使用 `FuncAnimation(blit=True)`。
*   **代码模式**: 
    ```python
    # Anti-Pattern:
    bar.set_alpha(0.3 + rms * 0.5)  # Vulnerable to overflow
    
    # Approved Pattern:
    bar.set_alpha(np.clip(0.3 + rms * 0.3, 0.1, 1.0))
    ```
*   **后果**: 
    *   (+) 渲染脚本健壮性显著提升。
    *   (-) 需要为每个动态属性手动定义合理的上下界。
