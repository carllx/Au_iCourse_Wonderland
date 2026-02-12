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

## 1.2 广播剧法则 (The Radio Play Protocol)

**核心公理**: *Monitor Broken Axiom* (屏幕损坏公理)。
假设听众的显示器刚刚烧坏了，他们仅凭你的声音能否完成操作？如果不能，这就是**“隐形指令” (Invisible Instruction)**。

### A. 双重记账法 (Double-Entry Bookkeeping)
不要因为在 `> [VISUAL]` 里写了动作，就觉得可以在 `[AUDIO]` 里省略。恰恰相反，**因为它是重要动作，所以必须写两次**。

*   **Visual Ledger**: `> [VISUAL] Action: Drag Threshold to -20dB` (给眼睛/开发看)
*   **Audio Ledger**: `[AUDIO]` "将阈值下拉到 -20dB..." (给耳朵/盲人听)

### B. 盲视测试 (Blindfold Test)
    *   `> [VISUAL] Click Multitrack Button`
    *   `[AUDIO]` "点击左上角的 **Multitrack** 按钮，进入多轨模式..."

## 1.3 拒绝机器人语感 (No Robotic Speech)

**"No Metadata Headers" (禁止元数据头)**。
在 `[AUDIO]` 或需要朗读的 Blockquote 中，严禁出现“键值对”式的列表头。

*   ❌ **机器人**: "Action: 将混响设为 50%。 Reason: 创造空间感。" (听起来像 debug log)
*   ✅ **讲师**: "我们将混响设为 50%，这是为了给它创造一种空间感。" (自然对白)
*   **黑名单关键词**: `Action:`, `Reason:`, `Warning:`, `Step 1:`, `Note:`.

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

## 6. 语义标签协议 (Semantic Tagging Protocol)

为了解决 "Single Source of Truth" 问题，并确保叙事与技术的分层，必须使用以下标签系统：

### 6.1 标签分类学 (Tag Taxonomy)

#### Class A: 叙事锚点 (Narrative Anchors)
*   **用途**: 赋予技术以“意义” (The Why)。此类内容**必须**被 TTS 朗读。
*   **白名单**:
    *   `> [STORY TIME]`: 完整的隐喻故事 (e.g., 爱丽丝变大变小)。
    *   `> [PHILOSOPHY]`: 哲学升华 (e.g., 柏拉图洞穴, 测不准原理)。
    *   `> [CULTURAL REF]`: 外部文化引用 (e.g., 电影、音乐、历史事件)。
    *   `> [TEACHING MOMENT]`: 关键的教学金句 (Lin Xin's Voice)。

#### Class B: 技术桥梁 (Technical Bridges)
*   **用途**: 连接物理世界与心理世界的接口。
*   **白名单**:
    *   `> [TECH NOTE]`: 纯技术解释，包含原理 (e.g., 为什么 80ms 是恐惧?)。
    *   `> [DID YOU KNOW]`: 冷知识/硬核科普。
    *   `> [WARNING]`: **[CRITICAL]** 操作风险警告。

#### Class C: 导演指令 (Director's Cues)
*   **用途**: 仅写给“执行者”看的，**不朗读**。
*   **白名单**:
    *   `> [VISUAL]`: 画面描述 (Slide, Action, Scene)。
    *   `> [PACING]`: 节奏控制 (Silence, Pause, Faster)。
    *   `> [REF]`: 资源索引 (Slide ID)。

## 7. 语言与韵律标准 (Linguistic & Prosodic Standards)

### 7.1 拒绝翻译腔 (Anti-Translationese) - [The Bamboo Check]
*   **竹节结构 (Bamboo Structure)**: 严禁使用嵌套长句。超过 20 字的句子必须按时间/逻辑顺序切断。
*   **话题优先 (Topic-Comment)**: 优先使用“话题+评论”结构，而非“主谓宾”结构。
    *   ✅ `要想做好这一点 (Topic)，全靠 Audition (Comment)。`
*   **禁忌词**: 
    *   ❌ `作为...`, `对于...`, `关于...` (虚词堆砌)。
    *   ❌ `...的...的...` (超过2层的定语堆叠)。
    *   ❌ `进行+动词` (名词化中毒)。
    *   ❌ `是...之一` (英文 One of 遗毒)。

### 7.2 韵律句法 (Prosodic Grammar) - [The Rhythm Check]
*   **标准音步 (Standard Foot)**: 旁白应遵循冯胜利教授的“韵律语法”，构建 `[2+1]` 或 `[2+2]` 的稳定音步。
    *   ❌ 忌: `1+1+1` (e.g., `切-掉-它`) -> ✅ 宜: `2+1` (e.g., `切除-它`)。
*   **四字格 (Quadra-syllabic Phrases)**: 在强调技术概念或情感色彩时，优先使用四字短语。
    *   e.g., `痛下狠手`, `浑浊不清`, `深不见底`。
*   **呼吸测试 (Gasp Test)**: 任何意群必须能在 4-5 秒内读完，否则必须加标点。

### 7.3 语义物理锚定 (Physics Anchor) - [The Semantics Check]
*   **范畴一致性 (Category Consistency)**: 抽象形容词/名词**不得**直接修饰物理单位。
    *   ❌ `下了50dB的重手` (Manner + Quantity = Mismatch)
    *   ✅ `痛下狠手，切掉了50dB` (Manner // Action + Quantity)
*   **名词动化 (Verbalization)**:
    *   ❌ `对噪音进行消除` -> ✅ `消除噪音`。

