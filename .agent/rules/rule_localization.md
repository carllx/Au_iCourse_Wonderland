---
trigger: glob
description: Ensures consistent English-Chinese localization based on the Tiered Protocol.
globs: 03_Scripts/*.md
---

# 规则：本地化与语言分层协议 (Localization & Tiered Language Protocol)

**生效范围**: 所有涉及中英文混合的脚本、教程、文档。

## 1. 核心哲学 (Core Philosophy)
**"认知的最小阻力" (Path of Least Cognitive Resistance)**。
我们不追求“为了英语而英语”。
*   **Story (叙事)**: 必须是母语的，直击人心的。
*   **Action (操作)**: 必须是精准的，对应软件界面的。

## 2. 三层分级协议 (The Three-Tier Protocol)

所有词汇的使用必须严格遵循以下分级：

| 层级 (Tier) | 定义 (Definition) | 语言策略 (Language Strategy) | 示例 (Examples) |
| :--- | :--- | :--- | :--- |
| **Tier 1: 叙事与逻辑** | 故事背景、通用的形容词、动词、连接词。 | **纯中文 (Native Chinese)**。严禁夹杂英文。 | ✅ "爱丽丝失去了语言"<br>❌ "Alice 失去了 Language" |
| **Tier 2: 通用概念** | 虽属技术范畴但已有通用译名的概念。 | **中文为主**。仅在首次出现时可备注英文，后续全中文。 | ✅ "墙 (Wall)", "内部 (Internal)"<br>❌ "Wall (墙)", "Internal 的声音" |
| **Tier 3: 软件锚点** | 软件界面上的按钮、菜单、参数名。 | **英文锚点 (English Anchor)**。必须保留英文以便用户在软件中找到对应项。 | ✅ "调整 Decay Time"<br>✅ "点击 Multitrack 按钮" |

## 3. 常见错误修正 (Common Pitfalls)

### 3.1 错误的“名词化” (False Nounification)
严禁将形容词当做专有名词使用，除非它是界面上的唯一标识符。
*   ❌ "这是 Internal 的声音。"
*   ✅ "这是**内部 (Internal)** 的声音。" (首次) -> "这是**内部**的声音。" (后续)

### 3.2 悬浮英文 (Floating English)
严禁在没有中文上下文的情况下直接插入英文单词。
*   ❌ "调整这个 Value。"
*   ✅ "调整这个**数值 (Value)**。"

### 3.3 标点与间距 (Punctuation & Spacing)
*   **盘古之白**: 中文与英文/数字之间必须加空格。
    *   ✅ `Audition 的效果`
    *   ❌ `Audition的效果`
*   **标点**: 中文语境下使用**全角标点**。