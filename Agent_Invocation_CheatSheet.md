# Agent 调用指南 (Agent Invocation Cheat Sheet)

> **目的**: 指导用户如何正确命令 Agent 执行符合 **INI (综合叙事完整性)** 标准的任务。

## 1. 撰写脚本 (Writing Scripts)
当您希望 Agent 编写某一节课程脚本时：

*   **推荐指令**:
    > "Agent, 请按照标准流程为我撰写 S05 的逐字稿。"
    > "Run the Writer Factory for S05."

*   **Agent 内部执行流 (SOP)**:
    1.  Agent 运行 `build_factory.py --task writer --section S05`。
    2.  获取包含 **"广播剧法则"** 和 **"自我验证链"** 的系统提示词。
    3.  基于该提示词生成内容，确保所有视觉动作都被“说出来”。

## 2. 审查脚本 (Auditing Scripts)
当您希望 Agent 检查现有脚本的质量时：

*   **推荐指令**:
    > "Agent, 请审查 S05 脚本的质量。"
    > "Run a full audit on S05."

*   **Agent 内部执行流 (SOP)**:
    1.  **逻辑层**: Agent 运行 `validate_narrative_integrity.py` 检查是否包含“隐形指令”。
    2.  **教学层**: Agent 运行 `build_factory.py --task auditor` 获取教学评估标准。
    3.  **报告**: 综合输出一份包含 Linter 结果和教学建议的报告。

## 3. 全局一键体检 (Auto Review)
当您想检查整个项目的健康度时：

*   **指令**:
    > "Run auto review."
    > 运行 `sh run_auto_review.command`

*   **功能**:
    *   检查所有链接有效性。
    *   统计字数与节奏。
    *   **[NEW]** 扫描所有脚本的叙事完整性 (INI Check)。
