---
name: Transcript Compiler
id: transcript-compiler
description: 编译课程逐字稿，将大纲转化为自然语言讲课稿
trigger: /compile, 生成逐字稿, 编译脚本
---

# 技能：编译课程逐字稿 (Compile Course Transcript)

## 描述 (Description)
此技能将结构化大纲 (`Structure_Map`) 和技术参数 (`Design_Spec`) 转化为自然语言讲课稿，同时严格遵守原始教材 (`Textbook_Index`) 的知识点和林昕老师 (`LinXin_Voice`) 的授课风格。

## 输入环境 (Inputs / Context)
1.  **结构 (Structure)**: `03_Scripts/00_Structure_Map.md` (时间轴与逻辑)
2.  **知识 (Knowledge)**: `../数字音频编辑Audition实用教程-混响-2md.md` (技术定义的唯一真理)
3.  **人设 (Persona)**: `.agent/styles/LinXin_Voice.md` (语气与口吻)
4.  **规范 (Spec)**: `01_MVP_Demo/00_Design_Spec_Alice.md` (技术参数与动作)

## 执行指令 (Instructions for Agent)
1.  **Step 0: 注入上下文 (Inject Context)**
    *   **必须读取**: `.agent/styles/LinXin_Voice.md` (加载“无形造境者”人格).
    *   **必须读取**: `01_MVP_Demo/00_Design_Spec_Alice.md` (获取动作规范).

2.  **Step 1: 格式协议 (Protocol: AV Script)**
    *   **严禁纯文本**: 输出必须严格遵循 "Visual-First" 双轨结构。
    *   **Visual Track**: 使用 `> [VISUAL]` 引用块，描述画面、资产与动作。
    *   **Audio Track**: 使用 `**[AUDIO]**` 标记，书写口语化台词。
    *   **Semantic Tags (语义标签)**:
        *   **Class A**: `> [STORY TIME]`, `> [PHILOSOPHY]`, `> [TEACHING MOMENT]`. (Narrative)
        *   **Class B**: `> [TECH NOTE]`, `> [WARNING]`. (Technical)
        *   **Class C**: `> [VISUAL]`, `> [PACING]`. (Silent)
        *   注意：Class A/B 的内容会被 TTS 引擎提取并朗读。
    *   **Subjectivity**: 所有的动作 (Actions) 都是由 **讲师** 完成的。使用 "我们/我" (We/I)。**严禁**使用 "你/请你" (You) 指令。
    *   **No Interaction Gaps**: 严禁留出“等待学生操作”的空白。任何留白 (`Pause`) 只能用于 **Deep Listening** (感受)，不能用于 **Doing** (操作)。

3.  **Step 2: 视觉动作生成 (Visual Generation)**
    *   当 `Structure_Map` 指示 `[ACTION]` 时，不要只是写 "Step 1: Click X"。
    *   **转化规则**:
        ```markdown
        > [VISUAL]
        > *   **Scene**: [描述当前界面]
        > *   **Ref**: `[SLIDE: Sxx_Name]` (所有 PPT 引用必须包含在 VISUAL 块内部)
        > *   **Asset**: 明确引用的文件名 (e.g. `asset_S02.wav`)
        > *   **Action**: 具体操作描述
        ```
    *   **Anti-Ghosting Rule**: 严禁将 `Ref` 或 `Slide` 引用放在 `> [VISUAL]` 块之外。孤立的引用会导致时间轴锚定失败。

4.  **Step 3: 叙事转化 (Narrative Synthesis)**
    *   将枯燥的技术定义转化为“林昕比喻”。
    *   *Constraint*: 每 3 分钟必须设计一个 **Visual Gap** `**(Pause: 3s)**`，用于留白。

5.  **Step 4: 输出成果 (Output)**
    *   生成中文 `S0x_Transcript.md`，确保它是一个可以直接分发给视频制作团队的**分镜脚本**。

## 质量检查 (Quality Check)
- [ ] 是否在开头/结尾明确体现了“无形造境者”的身份？
- [ ] 是否从“构建空间”的角度进行教学（而非单纯的技术讲解）？
- [ ] 技术参数是否与 `Design_Spec` 和原始教材完全一致？
- [ ] 是否包含了 **(留白)** 标记以支持 Deep Listening？
- [ ] 所有的 PPT 引用 `[REF:...]` 是否保留？
