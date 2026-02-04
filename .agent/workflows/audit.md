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

2.  **运行基础验证 (Pre-Flight Checks)**
    // turbo
    运行以下命令，确保资产链接和锚点结构正常：
    ```bash
    # 链接完整性
    python .agent/skills/validation-suite/scripts/validate_links.py
    # 锚点有效性 (Ghost Anchor Check)
    python .agent/skills/validation-suite/scripts/validate_anchors.py [Target_File_Path]
    ```

3.  **运行 INI 逻辑校验器 (The Linter)**
    // turbo
    运行以下命令，检查所有的 Visual/Audio 动作是否对齐：
    ```bash
    python3 .agent/skills/validation-suite/scripts/validate_narrative_integrity.py [Target_File_Path]
    # 语法合规性 (No ' > ' or '1. ' lists)
    python3 .agent/skills/validation-suite/scripts/validate_syntax.py [Target_File_Path]
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

    **Part A.5: Localization Check (语言层)**
    *   **Rule Compliance**: 必须阅读并核对 `.agent/rules/rule_localization.md`。
    *   **Chinglish Check**: 检查是否存在违反 "Tier 2: 通用概念" 的情况 (e.g. 使用了通用形容词的英文)。
    *   **Term Consistency**: 检查该模块特定的核心隐喻词汇 (Narrative Terms) 是否已按照协议汉化。


    **Part B: Pedagogy & Cognitive Check (教学层)**
    *   **负空间法则 (Negative Space Rule)**: 任何非 blockquote 的正文都视为 Audio。不要因为缺少 `[AUDIO]` 标签而跳过检查。
    *   **EXCEPTION**: `> [TEACHING MOMENT]` / `> [STORY TIME]` 等 Class A 引用块**也是 Audio**，必须接受同样的检查。
    *   **基于 Rubric**: 评估是否符合 "Director's Voice" 和 "Deep Listening"。
    *   **视觉时序检查 (Visual Sync Check)**: 
        *   [CRITICAL] 检查所有 `> [VISUAL]` / `> [Ref]` 是否在所对应的正文**之前**出现。如果有 "先讲后图" 的情况，记为 **FAIL**。
    *   **指示代词扫描 (Deictic Scan)**:
        *   检查所有 "这/这里/那/那个" (This/That/Here)。
        *   如果该代词之前没有明确的**声音描述** (e.g. "找到频率旋钮...这个旋钮...")，记为 **FAIL (Invisible Mechanics)**。
    *   **颗粒化复述 (Granular Retelling)**: 简述操作链路，检查是否有逻辑断层。
    *   **费曼审查 (Feynman Check)**: 核心隐喻是否通俗易懂？(e.g. 堵车 vs 频率遮蔽)。
    *   **脆弱性提问**: "如果用户**只听不做**，他能获得什么核心启示？"

    **Conclusion**: Pass / Fail / Needs Revision。
