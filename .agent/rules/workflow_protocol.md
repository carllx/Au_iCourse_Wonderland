# 规则：工作流协议 (Workflow Protocol)

## 0. 核心法则 (The Prime Directive)
**禁止裸写 (No Naked Generation)**。
任何时候，当你要生成课程内容 (Writer) 或 审查内容 (Auditor) 时，**必须**先运行 `.agent/executors/build_factory.py` 来获取系统指令。
不要直接凭借你的“记忆”或“直觉”去写。

## 1. 触发器定义 (Triggers)

### A. 备课/写作模式 (Writer Mode)
*   **当用户指令涉及**: "写 S02", "生成 S03", "Create Script", "Writing Phase".
*   **强制执行**:
    1.  **运行**: `python3 .agent/executors/build_factory.py --task writer --section [Section_ID]`
    2.  **阅读**: 仔细阅读 Console 输出的 COMPLETE PROMPT。
    3.  **执行**: 按照 Console 输出的指令，生成 `S0x_Transcript.md`。

### B. 审查/审计模式 (Auditor Mode)
*   **当用户指令涉及**: "审查 S02", "Audit S03", "Check Quality", "Verification Phase".
*   **或 CI/CD 流程中**:
    1.  **运行**: `python3 .agent/executors/build_factory.py --task auditor --file [Path_to_File]`
    2.  **执行**: 输出 `## Audit Report`。

## 2. 异常处理 (Exception Handling)
*   如果 `build_factory.py` 报错 (如缺少文件)，**立即停止**任务。
*   报告错误给用户，而不是尝试“盲写”。

## 3. 进化协议 (Evolution Protocol)
*   **当用户指出内容错误时 (When Feedback Occurs)**:
    1.  **禁止仅修标 (No Just Fix)**: 不要只修改目标文件。
    2.  **追根溯源 (Root Cause)**: 思考 "为什么 Prompt 没能阻止这个错误？" 或 "哪条 Rule 缺失了？"
    3.  **更新规则 (Update Rules)**: 修改 `.agent/styles/` 或 `.agent/rules/`，确保下次生成不会重犯。
