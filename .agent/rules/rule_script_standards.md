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

1.  **视觉轨 (Visual Track)**: 使用 `>` 引用块，以 `> [VISUAL]` 或 `> [REF]` 开头。
2.  **音频轨 (Audio Track)**: 使用普通文本，以 `**[AUDIO]**` (或角色名) 开头。
    *   **Class A (叙事锚点)**: `> [STORY TIME]`, `> [PHILOSOPHY]`, `> [TEACHING MOMENT]`. (TTS 将朗读)
    *   **Class B (技术桥梁)**: `> [TECH NOTE]`, `> [WARNING]`. (TTS 将朗读)

```markdown
### Segment X: [Title]

> [VISUAL]
> *   **Scene**: 屏幕显示 Audition 波形视图。
> *   **Asset**: 打开 `asset_01_demo.wav`。
> *   **Action**: 鼠标选中 0-5s 区域。

**[AUDIO]**
(温和而坚定)
同学们看，这就是我们今天要处理的“罪证”。

> [TEACHING MOMENT]
> 噪音不是你的敌人，它是信号的影子。我们不是要消灭它，而是要分离它。
```

## 2. 视觉锚点法则 (Visual Anchors)

*   **Asset Linking**: 视觉描述中涉及素材时，必须使用**行内代码**标注文件名。
    *   ✅ `打开 asset_S02_heartbeat.wav`
    *   ❌ `打开那个心跳文件`
*   **Director's Cues**: 操作演示可使用 `> [VISUAL]` 详细描述。**注意**：这是给**演示机器人/录屏**的指令，不是给学生的指令。由讲师执行。

## 3. 语速与留白 (Pacing & Gaps)

*   **术语规范**: 严禁随意翻译。涉及 Audition 专有名词（如 Reverb, Decay, Threshold）时，**必须** 遵循 `.agent/knowledge/Glossary_Audition_CN.md` 中的定义。
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

## 5. 质量保证：朗读测试 (QA: The "Read Aloud" Protocol)

为了消除“机器味”和“枯燥感”，在提交脚本前必须执行 **心理模拟 (Mental Simulation)**：

*   **Trigger (何时触发)**:
    *   当遇到纯技术讲解（如参数说明）时。
    *   当 `validate_script_length` 提示时长 **Underflow** (不足) 时。
*   **Action (如何执行)**:
    *   Agent 必须模拟 **林昕 (LinXin)** 的语气，向用户“朗读”关键段落。
    *   **检查清单**:
        1.  **卡嗓子吗？** (Is it clunky?) -> 如果长句读不顺，拆短句。
        2.  **像人话吗？** (Is it human?) -> 把 "设置参数为 X" 改为 "把手里的笔往下压"。
        3.  **视觉对位吗？** -> 朗读到 "看这里" 时，想象画面是否真的有东西在动。
*   **Fix (如何修正)**:
    *   如果发现枯燥， **必须** 引入 Metaphor (隐喻) 或 Story (故事) 来“稀释”技术密度。
    *   **原则**: "No Naked Numbers" (参数必须有叙事理由)。