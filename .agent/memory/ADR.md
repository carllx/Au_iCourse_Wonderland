# 架构决策记录 (ADR)

本文档记录关键技术决策背后的“原因”。未来的 Agent **严禁**在未经用户批准的情况下撤销这些更改。

---

## ADR-001: MVP 演示的模块化架构
*   **状态**: Accepted (2026-01-25)
*   **背景**: 项目以前只有平铺的 `tools` 和 `assets` 文件夹，导致“脚本 A”和“资产 B”之间的关系混乱。
*   **决策**: 
    1. 拆分为 `_Pipeline` (代码) 和 `_Library` (数据)。
    2. 强制执行严格的 `[Type]_[Module]_[Name]` 命名规范 (例如 `gen_S02_heartbeat.py` -> `asset_S02_heartbeat.wav`)。
*   **后果**: 
    *   (+) 所有权清晰。
    *   (-) 需要 Agent 遵循正则规则。

---

## ADR-002: 指数级音频淡出 (Exponential Audio Fade)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 线性音量淡出听起来很突兀，因为人类听觉是对数关系 (`dB`)。
*   **决策**: 所有音频生成器脚本必须使用 **指数淡出** (dB 线性) 逻辑进行过渡。
*   **代码模式**: `np.logspace(0, -3, length)` (从 1.0 淡出到 0.001)

---

## ADR-003: 线性频率可视化 (Linear Frequency Visualization)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 对于 S02 中的“迷雾/Fog”隐喻，对数刻度将高频噪声压缩成了一条细线。
*   **决策**: 专门针对 `render_S02_spectrum.py`，我们必须使用 **线性频率刻度** (0-16kHz)，使噪声在视觉上充满屏幕。
*   **限制**: 常规音频分析通常需要对数刻度。这是为了“Fog”隐喻所做的艺术性例外。

---

## ADR-004: 采用智能鉴赏课程模式 (Smart Course)
*   **状态**: Accepted (2026-01-25)
*   **背景**: 原计划包含学生“实验室提交”。然而，用户澄清这是一个“智能课程”，学生专注于 *体验* 和 *决策*，而不是文件导出。
*   **决策**: 
    1.  **无家庭作业**: 从教学大纲中删除所有关于学生提交（如 MP3 导出）的要求。
    2.  **安德森叙事 (Anderson Narrative)**: 所有技术参数必须由叙事隐喻（“灵魂映射”）证明。禁止纯技术解释（例如“为了去噪”）；必须框架化为叙事行动（例如“为了驱逐现实”）。
*   **后果**: 
    *   (+) 更高的参与度，减少学生的阻力。
    *   (-) 验证脚本 (如 `validate_submission.py`) 现已过时，应忽略或删除。

---

## ADR-005: 语境感知的资产合成 ("语义大于信号")
*   **状态**: Accepted (2026-01-25)
*   **背景**: 
    *   最初尝试使用随机噪声生成器生成“坏损案例”音频 (Hum/Click/Hiss) 未能满足教学需求。
    *   随机的 Click 听起来很假；标准语谱图未能显示低频 Hum。
    *   用户反馈强调“噪声必须与信号相关” (例如，Click 发生在爆破音处)。
*   **决策**: 
    *   **放弃随机性**: 所有合成伪影必须是 **语境感知 (Context-Aware)** 的。
        *   *示例*: Click 现在由语音包络上的 `signal.find_peaks` (爆破音) 触发。
    *   **强制视觉语义**: 可视化必须使用 **对数刻度 (Log Scale)** 来显示 50Hz Hum。
    *   **叙事标签**: 所有 UI 标签必须使用 `MetricTranslator` 协议 (中文叙事术语)，禁止使用原始的技术英文。
*   **后果**: 
    *   资产不再只是“技术文件”，而是“叙事道具”。
    *   生成器脚本更加复杂 (需要信号分析，而不仅是合成)。
    *   视觉验证现在是强制性的 (不能仅相信代码正确性；必须验证 *可见性*)。

---

## ADR-006: 基于对象的资产命名 (Object-Based Naming)
*   **状态**: Accepted (2026-01-29)
*   **来源**: S05 动态声像开发会话
*   **背景**: 
    *   S05 的 "Threats" 最初命名为 `_L.wav` (Left) 和 `_R.wav` (Right)。
    *   当需求升级为"动态声像"（Spiral Pan + Approaching Wall）时，L/R 的命名变得具有误导性，因为声音不再静止在特定位置。
*   **决策**: 
    *   **命名应描述"本质/质感 (Character)"，而非"位置 (Location)"**。
    *   `_L.wav` -> `_pressure.wav` (The Wall, 低频逼近)
    *   `_R.wav` -> `_anxiety.wav` (The Needle, 高频螺旋)
    *   **规则**: 位置是一个 *状态 (State)*，本质是一个 *身份 (Identity)*。文件名应反映身份。
*   **后果**: 
    *   (+) 文件名自解释，无论其在混音中的动态位置如何。
    *   (+) 与 "Object-Based Audio" 的行业术语一致。
    *   (-) 需要回溯性地重命名旧资产。

---

## ADR-007: 动态可视化的 Blitting 与值约束
*   **状态**: Accepted (2026-01-29)
*   **来源**: S05 视觉渲染器 Bug 修复
*   **背景**: 
    *   `render_S05_panning_visual.py` 在运行时因 `ValueError: alpha is outside 0-1 range` 崩溃。
    *   原因是 `set_alpha(0.3 + wall_rms * 0.5)` 未对音频 RMS 值进行上限约束。
*   **决策**: 
    1.  **强制性值约束 (Clamping)**: 所有 Matplotlib Artist 属性设置器（`set_alpha`, `set_markersize`）必须使用 `np.clip()` 确保值在有效范围内。
    2.  **Blitting 优先**: 对于帧率敏感的动画渲染，必须使用 `FuncAnimation(blit=True)`。
*   **代码模式**: 
    ```python
    # Anti-Pattern:
    bar.set_alpha(0.3 + rms * 0.5)  # Vulnerable to overflow
    
    # Approved Pattern:
    bar.set_alpha(np.clip(0.3 + rms * 0.3, 0.1, 1.0))
    ```
*   **后果**: 
    *   (+) 渲染脚本健壮性显著提升。
    *   (-) 需要为每个动态属性手动定义合理的上下界。

---

## ADR-008: 文档职责边界重整 (Document Boundary Refactoring)
*   **状态**: Accepted (2026-01-29)
*   **来源**: 架构审查会话
*   **背景**: 
    *   `00_Structure_Map.md` 中包含大量视觉描述 (如 `**[Visual]**: 极简主义数据艺术...`)
    *   Script 文件与 `01_MVP_Demo/_Library` 之间的资产引用不一致
*   **决策**: 
    1.  **SSOT 原则**: 每种信息只能在一个地方定义
        *   视觉描述 → `Slide_Database.md`
        *   课程结构 → `00_Structure_Map.md` (只引用 Slide ID)
        *   音频资产 → `asset_manifest.json`
    2.  **创建资产清单**: `01_MVP_Demo/asset_manifest.json` 区分"源资产"和"演示中间产物"
    3.  **制度化**: 创建 `rule_document_boundaries.md` 防止未来越界
*   **执行的变更**: 
    *   清理了 `00_Structure_Map.md` 中 4 处视觉描述越界
    *   补全了 `S05_Visual_Matrix` 和 `S05b_Spectrum` 的视觉描述
    *   创建了 `asset_manifest.json` 资产清单
*   **后果**: 
    *   (+) 文档职责清晰,易于维护
    *   (+) 资产引用可验证
    *   (-) 需要团队成员学习新规范

---

## ADR-009: 三层管线分离与 TTS 标准化
*   **状态**: Accepted (2026-01-30)
*   **来源**: 深度架构审查会话
*   **背景**: 
    *   `_Pipeline/renderers/` 混杂素材动效生成器和课程合成工具
    *   TTS 语音无标准存放位置
    *   录屏素材无规范目录
*   **决策**: 
    1.  **三层管线 (Three-Tier Pipeline)**:
        *   `generators/`: 音频资产生成
        *   `renderers/`: 单素材可视化
        *   `composers/`: 课程级合成 (NEW)
    2.  **TTS 标准路径**: `03_Scripts/tts/Sxx_Name.wav|srt`
    3.  **录屏标准路径**: `01_MVP_Demo/_Media/recordings/`
    4.  **Interface vs Implementation**: Edit quotes `Sxx.png` (Interface), always resolves to the latest asset.
*   **执行的变更**: 
    *   创建 `03_Scripts/tts/`
    *   创建 `01_MVP_Demo/_Pipeline/composers/`
    *   创建 `01_MVP_Demo/_Media/recordings/`
    *   删除违规 `02_Visuals/assets/proxies/`
    *   开发 `render_preview.py` (章节预览生成器)
    *   更新 `rule_asset_management.md` (新增 3.5-3.8 节)
*   **后果**: 
    *   (+) 工具职责清晰
    *   (+) TTS 工作流有章可循
    *   (+) 预览视频可自动化生成
    *   (-) 需适应新目录结构

---

## ADR-010: H5 交互预览系统与灰盒渲染逻辑
*   **状态**: Accepted (2026-01-30)
*   **来源**: H5 预览系统开发会话
*   **背景**: 
    *   最初的灰盒流程依赖 Python 生成成千上万张临时 PNG 图片，导致版本库膨胀且难以热更新。
    *   用户需要一种更直观、支持音频/字幕同步且能实时反映脚本变化的预览方式。
*   **决策**: 
    1.  **React 原生渲染**: 放弃 Python 生成静态灰盒图片，改为在 H5 页面中直接使用 React + CSS 渲染 16:9 比例的虚线布局框。
    2.  **资产叠加逻辑 (Layering)**: 
        *   底层：原生灰盒布局区域。
        *   顶层：物理资产（PNG）自动检测。如果 `02_Visuals/assets/` 下存在对应的 `Sxx.png`，则自动隐藏灰盒并显示真实素材。
    3.  **单向数据流 (Manifest-Driven)**: 由 `parse_slides.py` 作为 SSOT 解析器，将 `Structure_Map`、`Slide_Database` 和物理文件路径整合为唯一的 `slides.json`。
*   **后果**: 
    *   (+) 即时预览：修改脚本后运行 `npm run sync` 即可刷新 H5 看到最新布局。
    *   (+) 真实感：支持音频播放与 SRT 字幕同步，接近最终课程形态。
    *   (-) 增加了 Node.js/Vite 环境依赖。

---

## ADR-011: 手术刀协议与隐形指令悖论 (The Scalpel Protocol)
*   **状态**: Accepted (2026-02-02)
*   **来源**: S05 脚本认知压力测试
*   **背景**: 
    *   为了维护“造境者”的高级感，Writer 曾倾向于将所有“机械操作”（点击、菜单、参数设置）隐藏在 Markdown 的元数据标签中（如 `(Action: ...)`）。
    *   这种做法导致了 **“隐形指令悖论”**：视觉读者能看懂，但纯听觉用户（Audio-Only）完全不知道应该在什么时候点击什么。
*   **决策**: 
    1.  **新公理**: **"If it moves the mouse, it must be spoken." (只要动鼠标，就得说出来)**。
    2.  **手术刀协议 (The Scalpel Protocol)**: 将技术指令重新定义为“外科手术仪式”，使其在林昕的“物理/临床”人设中合法化。
    3.  **三要素**: 指令必须包含 Anchor (工具名) -> Action (动作) -> Reason (隐喻)。
*   **后果**: 
    *   (+) **听觉完整性 (Audio-Completeness)**: 听众不再需要看屏幕也能完成基本操作。
    *   (+) **风格统一**: 消除“机械指令”与“诗意叙事”的对立。
    *   (-) 脚本字数略微增加。

---

## ADR-012: 语义标签分类学 (Semantic Tag Taxonomy)
*   **状态**: Accepted (2026-02-02)
*   **来源**: S05 协议升级 (Protocol Upgrade)
*   **背景**: 
    *   脚本中混杂了 `> [TIP]`, `(Action: ...)`, `### [TEACHING MOMENT]` 等多种标记风格。
    *   "Instructional" (教学) 标记与 "Narrative" (叙事) 标记边界模糊，导致 TTS 引擎无法区分哪些该读，哪些是元数据。
*   **决策**: 
    1.  **废弃**: `(Action: ...)` (隐形机制), `> [TIP]` (工具书语气)。
    2.  **采用**: 三级分类学 (Class A/B/C)。
        *   **Class A (Narrative Anchors)**: `[STORY TIME]`, `[PHILOSOPHY]`, `[TEACHING MOMENT]`. (必须朗读)
        *   **Class B (Technical Bridges)**: `[TECH NOTE]`, `[WARNING]`. (必须朗读)
        *   **Class C (Director's Cues)**: `[VISUAL]`, `[PACING]`. (静默)
    3.  **技术实现**: 修补 `parse_anchors.py` 以支持提取引用块中的语音内容。
*   **后果**: 
    *   (+) **机器可读性**: 明确的白名单使自动化审计和 H5 生成成为可能。
    *   (+) **风格一致性**: 强制 Writer 思考每条指令是属于 "林昕" (Narrator) 还是 "导演" (Director)。

