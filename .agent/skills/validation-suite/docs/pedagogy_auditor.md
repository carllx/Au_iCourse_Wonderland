# 技能：教学质量审查 (Pedagogy Auditor)

## 描述 (Description)
此技能定义了 Auditor Agent 的核心职责：不仅仅是检查语法或链接，而是作为“教务处”进行**教育学审计 (Pedagogical Audit)**。

## 审查对象 (Audit Targets)
- `03_Scripts/S0x_Transcript.md` (逐字稿)

## 审查标准 (Audit Criteria)

### 1. 导演思维审查 (The "Director" Check)
*   **规则**: 每一段技术演示 (Demo) 之前，必须有一个 **“导演决策问题 (Director's Question)”** 或 **“安徒生灵魂映射 (Anderson's Soul Mapping)”**。
    *   **必须回答**: "为什么是这个数值？" (e.g. 为什么是 +3 不是 +5?)
*   **Pass**: "为了让爱丽丝保留作为人类的脆弱感，我们只能加 +3。如果加到 +5，她就变成了卡通老鼠。"
*   **Fail**: "接下来我们把 Reverb Time 设为 3000ms。" (缺乏思维引导，只有操作指令)

### 2. 深听留白审查 (The "Deep Listening" Check)
*   **规则**: 依据 `architecture_audit.md`，每个模块必须至少包含一次 **30秒以上的留白 (Silence Gap)** 用于引导倾听。
*   **Pass**: "现在请闭上眼，仔细感受这 30秒 的尾音... (留白 30s) ...大家听到了吗？"
*   **Fail**: 全篇都在说话，没有给学生“听”的时间。

### 3. 技术一致性审查 (Technical Alignment)
*   **规则**: 脚本中提到的参数值，必须与 `01_MVP_Demo/00_Design_Spec_Alice.md` 完全一致。
*   **例如**: 如果 Map 里是 `-2 Semitones`，脚本里不能说 "降低一个八度"。

### 4. 语义清晰度审查 (Semantic Clarity)
*   **规则**: 核心教学隐喻与重要技术警告，必须使用 `> [TEACHING MOMENT]` 或 `> [WARNING]` 显式标记。
*   **Fail**: 将关键的“拉链噪音”警告隐藏在无标签的引用块中（会被系统视为视觉备注而被剥离）。
*   **Fail**: 将 "Bus is Rain" 这种核心隐喻写在普通正文里，没有视觉高亮。

### 5. 数据一致性校验 (Consistency Check)
*   **规则**: 脚本中出现的所有数值与操作 (e.g. +5 Semitones, 75% Reduction) 必须与Prompt中的 `00_Design_Spec_Alice.md` 完全锁定。
*   **Fail**: Design Spec 说 +5，脚本里写 +3。 (这是严重的技术错误，必须 REJECT)。
*   **Fail**: Design Spec 说 "Abyss IR"，脚本里用 "Plate Reverb"。

### 6. 认知压力测试 (Cognitive Stress Test)
*   **A. 颗粒化复述 (Granular Retelling)**:
    *   **要求**: 必须检查脚本中的操作链路是否连续。
    *   **Fail**: 如果某两步之间存在逻辑断层 ("为什么突然要做这一步?")，必须标注 **[Fault Line]**。
*   **B. 费曼审查 (Feynman Check)**:
    *   **要求**: 所有的声学概念必须有通俗的物理隐喻 (e.g. 堵车 vs 频率遮蔽)。
    *   **Fail**: 如果只有术语没有隐喻，标记为 **[Semantics Suspended]** (悬浮)。
*   **C. 脆弱性提问 (Vulnerability Question)**:
    *   **要求**: 每一章必须有一个拷问核心价值的问题。
    *   **Fail**: 如果用户只听不做就没有任何收获，则通过率为 0。

## 执行指令 (Instructions)
作为一个 Auditor，请阅读目标文件，并输出一份 **Audit Report**：

```markdown
## Audit Report for [Filename]

### Part A: Narrative Integrity (INI Check)
* [✅/❌] Invisible Instructions: (引用 Linter 结果)

### Part B: Pedagogy & Cognitive Check
* [✅/❌] Director's Voice: (评语)
* [✅/❌] Deep Listening: (评语，指出留白位置)
* [✅/❌] Technical Accuracy: (评语)
* [✅/❌] Cognitive Stress Test:
    * **Granular Logic**: (是否存在断层?)
    * **Feynman Metaphor**: (隐喻是否通俗?)
    * **Value**: (用户只听不做能学到什么?)

* **Conclusion**: (PASS / REJECT)
```
