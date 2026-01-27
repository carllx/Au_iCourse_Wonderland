---
trigger: glob
description: Enforces Smart Course AV Script standards (Visual/Audio split, Pacing, Asset Linking).
globs: 03_Scripts/*.md
---

# 规则：智慧课程脚本标准 (Smart Course AV Script Standards)

**适用范围**: 所有 `03_Scripts/*.md` 教学逐字稿。
**核心原则**: **No Naked Script**. 所有脚本必须是 **音画分镜稿 (AV Script)**。

## 1. 结构标准：AV 双轨制 (Visual-First)

脚本必须按照 **“先画后音”** 的顺序编写。严禁出现没有任何视觉描述的“干讲”。

### ✅ 标准格式 (Standard Syntax)

每个段落 (Segment) 必须包含：

1.  **视觉轨 (Visual Track)**: 使用 `>` 引用块，以 `**[VISUAL]**` 开头。
2.  **音频轨 (Audio Track)**: 使用普通文本，以 `**[AUDIO]**` (或角色名) 开头。

```markdown
### Segment X: [Title]

> **[VISUAL]**
> *   **Scene**: 屏幕显示 Audition 波形视图。
> *   **Asset**: 打开 `asset_01_demo.wav`。
> *   **Action**: [ACT: Select_Range] 鼠标选中 0-5s 区域。

**[AUDIO]**
(温和而坚定)
同学们看，这就是我们今天要处理的“罪证”。
```

## 2. 视觉锚点法则 (Visual Anchors)

*   **Asset Linking**: 视觉描述中涉及素材时，必须使用**行内代码**标注文件名。
    *   ✅ `打开 asset_S02_heartbeat.wav`
    *   ❌ `打开那个心跳文件`
*   **Atomic Actions**: 操作演示必须使用 `[ACT: Action_Name]` 标签。**注意**：这是给**演示机器人/录屏**的指令，不是给学生的指令。由讲师执行。

## 3. 语速与留白 (Pacing & Gaps)

*   **黄金语速**: **180 - 220 字/分 (CN Char)**。
    *   教育类内容必须低于日常语速 (240+)，给大脑留出“认知带宽”。
*   **留白 (Gaps)**:
    *   每 3 分钟必须设计一次 **Visual Gap** (仅有画面动作，无旁白)，时长 3-5秒。
    *   标注方式: `**(Pause: 3s)**`

## 4. 此时此刻检测 (Validation)

运行 `python3 .agent/skills/validation-suite/scripts/validate_script_length.py` 会检测：
1.  **AV结构**: 是否存在“裸奔”的音频段落。
2.  **语速**: 是否超速 (Over-speed) 或 拖沓 (Under-speed)。
3.  **素材完整性**: [VISUAL] 块中是否遗漏了 Asset 引用。