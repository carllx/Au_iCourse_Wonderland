---
trigger: always_on
description: Enforces narrative consistency and "Director's Intent" in all generated content.
---

# 规则：叙事一致性协议 (Narrative Consistency Protocol)

**生效范围**: 所有涉及 Audition 操作步骤、脚本编写 (`03_Scripts/*.md`)、演示指南 (`01_MVP_Demo/*.md`) 的生成任务。

## 1. 核心铁律 (The Golden Rule)

**"No Naked Numbers" (禁止裸参数)**。
严禁在没有任何叙事解释的情况下，直接给出技术参数值。

*   ❌ **禁止**: "将 Reverb Decay 设为 3000ms。"
*   ✅ **允许**: "为了营造深渊的无底感 (Story)，我们将 Decay 设为 3000ms (Action)，这代表声音永远无法触底 (Reason)。"

## 1.1 文件名引用规范 (File Reference Protocol)

**"No Naked Filenames" (禁止裸读文件名)**。
在 `[AUDIO]` (口语脚本) 部分，严禁直接朗读带有下划线、扩展名的原始文件名（如 `asset_v1_final.wav`）。

*   **原则**: 旁白必须说人话。
*   **格式**: 自然语言描述 + (技术备注/文件索引)。
*   ❌ **禁止**: "导入 asset_S05_threat_pressure.wav。"
*   ✅ **允许**: "导入名为 'Pressure' (压迫) 的素材 **(文件: asset_S05_threat_pressure.wav)**。"
*   ✅ **允许**: "导入那段代表压迫感的低频音效。 **(Note: Use asset_S05_threat_pressure.wav)**"

## 2. 结构化范式 (The Triad Structure)

所有教学单元必须遵循 **STA结构**：
1.  **Story (动机)**: 为什么只要这就做？(e.g., 爱丽丝变小了)
2.  **Target (听感)**: 我们想要什么声音？(e.g., 变尖细但保留人性)
3.  **Action (参数)**: 具体怎么调？(e.g., Pitch +3 semitones)

## 3. 来源一致性 (Source of Truth)

`01_MVP_Demo/00_Design_Spec_Alice.md` 是目前的**最高叙事真理**。
*   任何时候生成的 Demonstration 步骤，必须与该文件中的参数（如 75% Reduction, +5 Pitch）保持严格一致。
*   如果发现冲突，**以该文件为准**。

## 4. 语言风格 (Tone Check)

*   **拟人化**: 鼓励使用拟人化比喻（"回声是候鸟", "心跳是钉子"）。
*   **戏剧性**: 在枯燥的技术环节（如降噪），必须强调其对声音“角色感”的破坏后果（"底噪会打破梦境"）。

## 5. 语义桥接 (The Semantic Bridge)

**"No Suspended Literature" (禁止悬浮文学)**。
所有文学隐喻（Metaphor）都必须在声学物理层找到明确的对应物（Anchor）。

*   ❌ **悬浮**: "她只剩下了躯壳。" (抽象文学，无听觉指引)
*   ✅ **锚定**: "她只剩下了躯壳 (Metaphor)，因为缩小的药水压扁了她的**共鸣腔体** (Acoustic Anchor)，导致声音失去了**低频重量** (Physics)。"

**公式**: `Metaphor (文学意象) <---> Acoustic Anchor (声学中介) <---> Parameter (技术参数)`。
