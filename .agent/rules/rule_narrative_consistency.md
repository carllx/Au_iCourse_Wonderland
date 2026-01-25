---
trigger: always_on
description: Enforces narrative consistency and "Director's Intent" in all generated content.
---

# 规则：叙事一致性协议 (Narrative Consistency Protocol)

**生效范围**: 所有涉及 Audition 操作步骤、脚本编写 (`01_Scripts/*.md`)、演示指南 (`03_MVP_Demo/*.md`) 的生成任务。

## 1. 核心铁律 (The Golden Rule)

**"No Naked Numbers" (禁止裸参数)**。
严禁在没有任何叙事解释的情况下，直接给出技术参数值。

*   ❌ **禁止**: "将 Reverb Decay 设为 3000ms。"
*   ✅ **允许**: "为了营造深渊的无底感 (Story)，我们将 Decay 设为 3000ms (Action)，这代表声音永远无法触底 (Reason)。"

## 2. 结构化范式 (The Triad Structure)

所有教学单元必须遵循 **STA结构**：
1.  **Story (动机)**: 为什么只要这就做？(e.g., 爱丽丝变小了)
2.  **Target (听感)**: 我们想要什么声音？(e.g., 变尖细但保留人性)
3.  **Action (参数)**: 具体怎么调？(e.g., Pitch +3 semitones)

## 3. 来源一致性 (Source of Truth)

`01_Scripts/Experiment_Manual_Alice.md` 是目前的**最高叙事真理**。
*   任何时候生成的 Workshop 步骤，必须与该文件中的参数（如 150% Width, +3 Pitch）保持严格一致。
*   如果发现冲突，**以该文件为准**。

## 4. 语言风格 (Tone Check)

*   **拟人化**: 鼓励使用拟人化比喻（"回声是候鸟", "心跳是钉子"）。
*   **戏剧性**: 在枯燥的技术环节（如降噪），必须强调其对故事破坏性的后果（"底噪会打破梦境"）。
