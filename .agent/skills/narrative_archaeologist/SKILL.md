---
name: Narrative Archaeologist
id: narrative-archaeologist
description: 专门用于挖掘技术概念背后的哲学隐喻、历史起源与科学奇闻。
trigger: /archeology, 挖掘隐喻, 寻找故事, deep research
---

# 技能：叙事考古学 (Narrative Archaeologist)

## 描述 (Description)
此技能并不直接生成脚本，而是作为**“前期概念开发”**工具。它将枯燥的技术术语（如 FFT, Noise Reduction）转化为具有哲学深度或历史厚度的叙事资产。
核心理念：**Every technical parameter has a biography (每一个参数都有它的传记)。**

## 能力 (Capabilities)

### 1. 桥接搜索 (Bridge Searching)
将技术词汇与人文领域建立强制连接。
*   **输入**: Technical Term (e.g., "Room Tone")
*   **输出**: Metaphors, Philosophical Concepts (e.g., "Ghost of a room")

### 2. 技术锚点 (Technical Anchoring)
**Critical Safety Check**: 防止“故事过剩，技术缺失”。
*   **规则**: 每一个挖掘出来的故事，必须绑定一个具体的 **Technical Parameter**。
*   *Fail*: "讲一个关于噪音的故事" (Too vague).
*   *Pass*: "讲一个关于为了解决 Musical Noise (Story) 而必须将 Reduction 设为 75% (Anchor) 的故事"。

### 3. 起源考据 (Origin Verification)
验证那些“听起来太好以至于不像真的”的故事，确保引用严谨。

## 执行流程 (Workflow)

1.  **Step 1: 锚点锁定 (Anchor Lock)**
    *   明确当前要解释的**具体参数**是什么（e.g., Smoothing, FFT Size）。
2.  **Step 2: 跨界桥接 (Bridge Search)**
    *   使用 `prompts/search_patterns.md` 搜索该参数背后的原理或历史。
3.  **Step 3: 故事验证 (Fact Check)**
    *   验证真实性。
4.  **Step 4: 锚点回归 (Return to Anchor)**
    *   在叙事结束后，必须用一句话回到技术参数："正是因为 Gabor 的原理 (Story)，所以我们要把 FFT 设为 4096 (Anchor)。"

## 资源 (Resources)
*   **Search Patterns**: `prompts/search_patterns.md` (搜索模板库)
