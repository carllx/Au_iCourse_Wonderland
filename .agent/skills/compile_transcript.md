# 技能：编译课程逐字稿 (Compile Course Transcript)

## 描述 (Description)
此技能将结构化大纲 (`Structure_Map`) 和技术参数 (`Action_Map`) 转化为自然语言讲课稿，同时严格遵守原始教材 (`Textbook_Index`) 的知识点和林昕老师 (`LinXin_Voice`) 的授课风格。

## 输入环境 (Inputs / Context)
1.  **结构 (Structure)**: `01_Scripts/00_Structure_Map.md` (时间轴与逻辑)
2.  **知识 (Knowledge)**: `../数字音频编辑Audition实用教程-混响-2md.md` (技术定义的唯一真理)
3.  **人设 (Persona)**: `.agent/styles/LinXin_Voice.md` (语气与口吻)
4.  **动作 (Action)**: `03_MVP_Demo/Action_Map.md` (具体操作步骤)

## 执行指令 (Instructions for Agent)
1.  **Step 0: 注入上下文 (Inject Context)**
    *   **必须读取**: `.agent/styles/LinXin_Voice.md` (加载“声音导演”人格).
    *   **必须读取**: `00_Planning/architecture_audit.md` (了解“深听”策略).
    *   **必须读取**: `.agent/knowledge/Textbook_Index.md` (加载原始教材索引).

2.  **Step 1: 识别模块 (Identify Module)**
    *   读取 `Structure_Map` 确定当前要生成的章节（例如 "S02 净化"）。

3.  **Step 2: 检索与对齐 (Retrieve & Align)**
    *   **动作**: 在 **原始教材**或`Textbook_Index`指引的源文件中查阅对应的章节（如 6.6 章）。
    *   **核心约束 (HARD CONSTRAINT)**: **严禁**编造技术参数或重新定义术语。所有技术解释必须严格对齐教材。
    *   *违规示例*: 如果教材说是 "3000ms", 不要写成 "3秒左右"，要精确引用。

4.  **Step 3: 应用人设 (Apply Persona)**
    *   将教材中枯燥的定义用“林昕的导演比喻”重写。
    *   *例子*: 把 "信噪比" 比作 "信号是主角，噪声是群演"。

5.  **Step 4: 植入动作与留白 (Embed Action & Silence)**
    *   当 `Structure_Map` 出现 `[ACTION: ACT_xx]` 时，插入 `Action_Map.md` 中的具体步骤。
    *   **关键**: 当涉及“听辨”时，必须插入 **(留白 10-30秒)** 字样，作为“深听”环节的占位。

6.  **Step 5: 输出成果 (Output)**
    *   生成 `S0x_Transcript.md` 中文内容。
    
## 质量检查 (Quality Check)
- [ ] 是否在开头/结尾明确体现了“声音导演”的身份？
- [ ] 技术参数是否与 `Action_Map` 和原始教材完全一致？
- [ ] 是否包含了 **(留白)** 标记以支持 Deep Listening？
- [ ] 所有的 PPT 引用 `[REF:...]` 是否保留？
