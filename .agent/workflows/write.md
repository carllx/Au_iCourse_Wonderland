---
description: 启动 Writer Agent 为指定章节撰写逐字稿 (使用 INI 框架)
---
# Writer Workflow

此工作流用于调用标准化工厂模式，生成符合 **INI (综合叙事完整性)** 标准的课程逐字稿。

**参数**:
*   `$1` (Section ID): 目标章节 ID (例如 `S05`, `S02`)。如果不提供，Agent 将询问。

**步骤**:

1.  **运行 Prompt Factory**
    运行以下命令生成包含 "广播剧法则" 和 "自我验证链" 的系统提示词：
    ```bash
    python3 .agent/executors/build_factory.py --task writer --section $1
    ```

2.  **执行写作**
    *   **阅读**: 仔细阅读上一步 Console 输出的 `SYSTEM PROMPT`。
    *   **思考**: 这里的关键约束是 **"No Invisible Mechanics"** (双重记账)。
    *   **生成**: 创建或覆盖 `03_Scripts/$1_Transcript.md` (或根据上下文判断合适的文件名)。
    *   **检查**: 在输出最后，附上一个简单的 "Self-Verification Checklist"，确认所有 Visual Action 都已在 Audio 中体现。
