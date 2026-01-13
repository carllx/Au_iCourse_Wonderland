# 技能：编译课程逐字稿 (Compile Course Transcript)

## 描述 (Description)
此技能将结构化大纲 (`Structure_Map`) 和技术参数 (`Action_Map`) 转化为自然语言讲课稿，同时严格遵守原始教材 (`Textbook_Index`) 的知识点和林昕老师 (`LinXin_Voice`) 的授课风格。

## 输入环境 (Inputs / Context)
1.  **结构 (Structure)**: `01_Scripts/00_Structure_Map.md` (时间轴与逻辑)
2.  **知识 (Knowledge)**: `../数字音频编辑Audition实用教程-混响-2md.md` (技术定义的唯一真理)
3.  **人设 (Persona)**: `.agent/styles/LinXin_Voice.md` (语气与口吻)
4.  **动作 (Action)**: `03_MVP_Demo/Action_Map.md` (具体操作步骤)

## 执行指令 (Instructions for Agent)
1.  **识别模块**: 读取 `Structure_Map` 确定当前要生成的章节（例如 "S02 净化"）。
2.  **检索知识**: 在 **原始教材** 中查阅对应的章节（如 6.6 章）。
    *   *约束*: 不要编造定义。术语解释必须基于教材。
3.  **应用人设**: 将教材中枯燥的定义用“林昕的导演比喻”重写。
    *   *例子*: 把 "信噪比" 比作 "信号是主角，噪声是群演"。
4.  **植入动作**: 当 `Structure_Map` 出现 `[ACTION: ACT_xx]` 时，插入 `Action_Map.md` 中的具体步骤，并格式化为 `(操作: ...)`。
5.  **输出成果**: 生成 `S0x_Transcript.md` 中文内容。

## 质量检查 (Quality Check)
- 语气是否亲切且具有导演感？
- 所有的 PPT 引用标签 `[REF:...]` 是否保留？
- 是否包含了“导演决策”的思维过程？
