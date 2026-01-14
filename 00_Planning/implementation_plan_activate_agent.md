# Implementation Plan: Activating the ".agent" Directory

## 1. 审计结论 (Audit Verdict)

**用户你是对的。** (You are correct.)

经过严谨的调查，目前 `.agent/` 目录下的文档存在“虚实分离”的现象：

*   **实 (Active)**: `validate_links.py`, `validate_script_length.py`
    *   **证据**: 被 `.github/workflows/verify_courseware.yml` 明确调用。它们是真正的“可执行代码”。
*   **虚 (Passive)**: `compile_transcript.md`, `pedagogy_auditor.md`, `LinXin_Voice.md`, `creative_muse.md`
    *   **证据**: **没有任何** 脚本、Workflow 或 API 调用这些文件。它们目前仅仅是“写给我（AI）看的备忘录”。如果我不主动去读，它们就是废纸。在工程上，这确实属于“摆设 (Shelfware)”。

## 2. 核心问题 (The Problem)

目前的架构依赖 **"AI 的自觉性" (Agent Voluntarism)**：
> *期望 AI 自主读取 `compile_transcript.md` -> 然后自主执行 -> 然后自主自我审查。*

这在工程上是**不可靠的**。真正的 "Agentic Workflow" 应该是由代码驱动的，**强制**将这些 Markdown 作为 Prompt 注入给 LLM。

## 3. 解决方案：从“文档”到“元编程” (From Docs to Meta-Programming)

我们需要创建一个**执行器 (Executor)**，将这些“死”的 Markdown 变成“活”的系统指令。

### 3.1 新增工具: `build_course.py` (The Orchestrator)
创建一个 Python 脚本，作为“总导演”的代理。

*   **功能**:
    1.  **加载人格**: 读取 `LinXin_Voice.md` 内容。
    2.  **加载技能**: 读取 `compile_transcript.md` 内容。
    3.  **加载数据**: 读取 `00_Structure_Map.md` 和 `Textbook_Index.md`。
    4.  **构建 Prompt**: 将上述内容拼接成一个 **Structured System Prompt**。
    5.  **输出指令**: (对于当前 IDE 环境) 它将输出一段**经过组装的、不可违抗的 Prompt**，供我（AgentIDE）直接执行。

### 3.2 架构变更 (Architecture Change)

```text
Project_Root/
├── .agent/
│   ├── executors/                     # [New] Python 驱动层
│   │   └── build_factory.py           # 读取 .md 并在 Console 输出完整 Prompt
│   ├── skills/
│   │   ├── compile_transcript.md      # [Source] 现在的“摆设”
│   │   └── pedagogy_auditor.md        # [Source] 现在的“摆设”
```

## 4. 实施计划 (Execution Plan)

### Step 1: 创建 `build_factory.py`
编写一个脚本，它接受 `--task [writer|auditor]` 参数。
*   `python .agent/executors/build_factory.py --task writer --section S02`
*   **Output**: 打印出一份完整的、包含所有 Context 的 Prompt。
*   **意义**: 以后我生成脚本时，**必须**先运行这个命令，然后执行它生成的 Prompt。这就把“依靠自觉”变成了“依靠工具”。

### Step 2: 验证
运行脚本，检查生成的 Prompt 是否包含了 `LinXin_Voice` 的具体句子和 `pedagogy_auditor` 的检查清单。

## 5. 预期结果
`.agent` 目录下的 Markdown 文件将从“摆设”变为“源代码 (Source Code)”，`build_factory.py` 是它们的“编译器”。
