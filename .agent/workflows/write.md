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
    *   **Localization**: 确保严格遵守 `rule_localization.md` (叙事纯中文，术语留锚点)。
    *   **Natural Language Protocol**: 严禁在 `[AUDIO]` 部分使用元数据列表头（如 `Action:`, `Reason:`, `Warning:`, `Step 1:`）。所有操作步骤必须融化为自然的口语叙述。
    *   **Parenthesis Protocol**: 严禁将关键教学术语仅放在括号内，例如 `调整大小 (Room Size)`。TTS 解析器会自动丢弃括号内容。必须改写为显性口语：`调整 **Room Size** 大小`。
        *   ❌ **Fail**: "Action: 打开混响。 Reason: 为了增加空间感。"
        *   ✅ **Pass**: "接下来，我们需要打开混响，这是为了给声音一点空间感。"

    **Step 2.5: The Blindfold Simulation (由 Agent 自主执行)**
    *   **负空间法则 (Negative Space Rule)**: 忽略所有 `[AUDIO]` 标签的存在与否。任何**不是**引用块 (`>`) 且**不是**标题 (`#`) 的正文，全部视为**旁白**。
    *   **EXCEPTION**: 以 Class A 标签 (如 `> [TEACHING MOMENT]`) 开头的引用块，**必须**视为旁白处理。
    *   **盲视测试**: 暂时“甚至”掉所有的 `> [VISUAL]` 块。仅阅读正文。
        *   ❌ **Fail**: "看这里" (哪里?) / "把这个参数拉大" (哪个?)
        *   ✅ **Pass**: "找到频率旋钮 (What)，把它拉大 (Action)..."
    *   **修正**: 如果发现依赖视觉的“隐形指令”，立即重写为“双重记账”格式。

    **Step 2.6: The Sync Check (视觉时序检查)**
    *   **时序法则**: 任何 `> [VISUAL]` 或 `> [Ref]` 块，必须出现在描述它的正文**之前** (Pre-load)，严禁出现在之后 (Lag)。
        *   ❌ **Fail**: "这是一只猫。 > [Slide: Cat]" (听众先听到猫，才看到图)
        *   ✅ **Pass**: "> [Slide: Cat] ... 请看屏幕，这是一只猫。" (画面先就绪)
    *   **EXCEPTION (交互例外)**: 对于 **动态演示 (Interactive Actions)** (e.g. 播放视频、点击按钮)，允许 Audio Prompt (提示语) 出现在 Visual Action 之前。
        *   ✅ **Pass**: "大家请听... (Audio) -> [ACT: Play_Video] (Visual)"。这符合 "先提示后执行" 的自然逻辑。

    **Step 2.7: The IAA Protocol (演示三明治)**
    *   **强制执行**: 所有 Interactive Action 必须遵守 **Intro -> Action -> Analysis** 结构。
    *   **Ghost Anchor**: 严禁 Action 后面不跟任何文字。Action 之后必须紧跟一句 "Analysis" (e.g. "听到了吗？")，否则 `validate_anchors.py` 会报错。❗❗❗

    **Step 2.8: Spec-First Hook (自动定义)**
    *   **触发**: 如果写作过程中新增了 `[SLIDE: SXX_NewID]` 引用。
    *   **行为**: 检查 `Slide_Database.md` 中是否存在 `SXX_NewID`。如果不存在，立即创建一个 **最小化 Stub**：
        ```markdown
        ## SXX_NewID
        *   **Type**: [Concept Art] <!-- 根据上下文推断 -->
        *   **Concept**: [关键词]
        *   **Visual**: [从脚本上下文提炼的简述]
        ```
    *   **禁止**: 在 Writer 模式下调用 `gen_visual_asset.py`。仅定义，不生产（留给 Greybox 或后续 `/audit` 时自动生成）。

    *   **检查**: 在输出最后，附上一个简单的 "Self-Verification Checklist"，确认所有 Visual Action 都已在 Audio 中体现。

3.  **Automated Verification Gate (自动化校验门禁)**
    // turbo
    在提交给用户之前，**必须**运行以下命令进行自我审计。如果报错，必须修正直到通过。
    ```bash
    python .agent/skills/validation-suite/scripts/validate_narrative_integrity.py 03_Scripts/$1_Transcript.md
    ```
    
    *   **Fail Condition**: 如果 Linter 返回 `❌ Failed`，禁止提交给用户。
    *   **Fix Loop**: 阅读错误日志 -> 修改脚本 -> 重新运行 Linter。

    // turbo
    同时运行以下命令，确保没有使用 " > " 导航路径或 "1." 序号列表（需改为口语化连接词）：
    ```bash
    python .agent/skills/validation-suite/scripts/validate_syntax.py 03_Scripts/$1_Transcript.md
    ```

4.  **Final Polish (自检)**
    // turbo
    运行以下命令确保没有 "Ghost Anchors" (幻影锚点) 且结构有效：
    ```bash
    python .agent/skills/validation-suite/scripts/validate_anchors.py 03_Scripts/$1_Transcript.md
    ```
