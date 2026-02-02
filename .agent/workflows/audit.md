---
description: 启动 Auditor Agent 审查脚本质量 (逻辑完整性 + 教学标准 + 认知测试)
---
# Auditor Workflow

此工作流用于对脚本进行“双重审计”：既检查逻辑完整性 (INI Linter)，也检查教学质量 (Pedagogy)。
它合并了原本 `audit_script.md` 中的“认知压力测试”标准。

**参数**:
*   `$1` (Section ID or File Path): 目标章节或文件路径。例如 `S05` 或 `03_Scripts/S05_Phase4_Position.md`。

**步骤**:

1.  **定位文件**
    如果用户只提供了 ID (如 `S05`)，请先找到对应的脚本文件路径 (通常在 `03_Scripts/` 下)。

2.  **运行 INI 逻辑校验器 (The Linter)**
    // turbo
    运行以下命令，检查所有的 Visual/Audio 动作是否对齐：
    ```bash
    python3 .agent/skills/validation-suite/scripts/validate_narrative_integrity.py [Target_File_Path]
    ```

3.  **运行教学评估工厂 (The Rubric)**
    // turbo
    运行以下命令，获取教学评估标准：
    ```bash
    python3 .agent/executors/build_factory.py --task auditor --file [Target_File_Path]
    ```

4.  **生成审计报告**
    基于以上两步的输出，生成一份 `## Audit Report`。
    
    **Part A: Narrative Integrity (逻辑层)**
    *   引用 Linter 的结果。如果有 Fail，必须高亮指出。

    **Part B: Pedagogy & Cognitive Check (教学层)**
    *   **基于 Rubric**: 评估是否符合 "Director's Voice" 和 "Deep Listening"。
    *   **颗粒化复述 (Granular Retelling)**: 简述操作链路，检查是否有逻辑断层。
    *   **费曼审查 (Feynman Check)**: 核心隐喻是否通俗易懂？(e.g. 堵车 vs 频率遮蔽)。
    *   **脆弱性提问**: "如果用户**只听不做**，他能获得什么核心启示？"

    **Conclusion**: Pass / Fail / Needs Revision。
