# Audition 智慧课程实战：Project Wonderland 
## (原名：数字音频编辑 Audition 实用教程-混响篇)

**项目代号**: `Audition_SmartCourse_Wonderland`
**代码仓库**: [GitHub Repo](https://github.com/carllx/Au_iCourse_Wonderland.git)

## 目标
基于 `数字音频编辑Audition实用教程-混响-2md.md`，构建一套完整的 1 小时智慧课程内容方案。

## 用户审查 (User Review Required)
> [!NOTE]
> **课程背景确认**
> - **课程性质**：线上智慧课程（无实时答疑）。
> - **所属章节**：第五章 掌握和使用效果组（第二部分）。
> - **衔接背景**：承接第一部分（陈嘉源老师），本课（林昕老师）主讲 **N/B/C/O/E**。
> - **主讲教师**：林昕。
> - **时长**：1小时。

> [!CAUTION]
> **工程风险应对 (Engineering Mitigation)**
> - **[High] 知识覆盖风险**：因“减法策略”导致的知识盲区，将在 **Intro 后插入 3分钟“工具速览 (Toolbox Flash)”**，快速演示被跳过工具（Doppler/Distortion/Center Channel）的一键效果，确保“虽不精讲，但有认知”。
> - **[High] 素材单点依赖**：MVP 极度依赖干声质量。**强制执行 Plan B**：预置一段由 TTS 生成的高质量/无混响/情感中性的标准干声，以防真实录音不适用。
> - **死链风险**：采用 **validate_links.py** 自动化校验。脚本中**严禁硬编码页码**，必须使用 ID (e.g., `[REF: Slide_05]`)。
> - **时间风险**：脚本字数严格限制在 **6000字** 以内。导演提问 (Director Questions) 限制为“一问一答”模式，避免长篇大论。

> [!IMPORTANT]
> **MVP 演示实验：艺术性升级**
> 原设计 "播客修复" 偏技术流。为增加**艺术性与趣味性**，本方案调整为 **“声音剧场：爱丽丝的奇幻空间”**。
> **概念**：不仅是“修复”，而是“创造”。我们将一段平平无奇的干声朗读，通过五个步骤，变成一段仿佛在“奇幻洞穴”或“太空”中的**沉浸式广播剧片段**。
> - *趣味点*：用变调模拟“巨人”或“精灵”的声音；用混响创造“虚拟舞台”。

> [!IMPORTANT]
> **内容深化策略 (Deep Content Integration)**
> **不再进行大幅减法**。用户反馈指出单纯的“Alice 故事”导致了技术内容的空心化。
> 本方案将重启对 **数字音频编辑Audition实用教程-混响-2md.md** 的深度引用：
> - **S02 降噪**: 必讲 **频谱衰减率 (Spectral Decay)** 与 **平滑 (Smoothing)** (源文件 6.6.2)，解释为何它们能减少“气泡声”。
> - **S03 变调**: 必讲 **精度 (Precision)** 与 **拼接频率 (Splicing Freq)** (源文件 6.10.4)，解释如何避免“隧道音”。
> - **S04 混响**: 必讲 **预延时 (Pre-Delay)** (源文件 6.7.1)，它是人耳判断空间大小的第一要素，不仅仅是 Decay Time。
> - **S05 声像**: 必讲 **相位抵消** 的原理 (源文件 6.9.3)，演示过度扩展的代价。
>
> *目标字数：5500+ (含技术详解)*

## IDE 项目构建架构 (Engineering-Grade Project Architecture)

基于您的反馈，我们将采用 **“模块化开发” + “智能体编排”** 的架构。这不仅为了管理文件，更是为了让 AI Agent 能在有限 Context 下高效处理。

### 1. 目录结构设计 (Modules & Separation)

```text
Project_Root/
├── 00_Planning/                  # [顶层设计]
│   ├── Content_Strategy.md       # 教学策略 (爱丽丝剧场、声音导演理念)
│   ├── Dev_Build_Plan.md         # 工程规范 (本文档拆分后归档于此)
│   └── task.md                   # 进度看板
├── 01_Scripts/                   # [生成产物] 模块化逐字稿 (由 Map 编译生成)
│   ├── 00_Structure_Map.md       # [核心骨架] 结构化映射表 (控制逻辑、甚至包含伪代码)
│   ├── S01_Intro.md              # 导入部分
│   ├── S02_Phase1_Purify.md      # 净化环节
│   ├── S03_Phase2_Sculpt.md      # 塑形环节
│   ├── S04_Phase3_Space.md       # 置景环节
│   ├── S05_Phase4_Position.md    # 定位环节
│   └── S06_Summary.md            # 总结
├── 02_Visuals/                   # [视觉层] PPT 内容以“数据”形式存在
│   └── Slide_Database.md         # 包含 Slide_ID, Visual_Prompt, Text_Content
├── 03_MVP_Demo/                  # [逻辑层] 演示步骤配置
│   ├── Action_Map.md             # 包含 Action_ID, Step_Description, Parameter_Value
│   └── assets/                   # 音频素材
└── .agent/                       # [智能体配置]
    ├── knowledge/                # [知识库] 原始教材的“索引化”版本
    │   └── Textbook_Index.md     # 指向原始 MD 文件的章节知识点映射
    ├── styles/
    │   └── LinXin_Voice.md       # [风格配置] 语言风格指南 (亲切、导演视角)
    └── skills/                   # [技能库] (Ref: Claude Skills)
        ├── compile_transcript.md # [技能] 编写逐字稿 (Input: Structure + Textbook + Style)
        └── validate_links.py     # [工具] 校验锚点一致性

### 2. “课件编译器”工作流 (The Courseware Compiler Pattern)

为了避免内容脱节，我们将**原教材**设定为 Agents 的核心知识源 (Knowledge Base)。

*   **输入端 (Context)**:
    1.  **[Logic]** `00_Structure_Map.md`: 骨架 (时间轴、排写逻辑)。
    2.  **[Knowledge]** `Textbook_Index.md`: **知识源头** (直接引用 `数字音频编辑...md` 的特定段落)。
    3.  **[Persona]** `LinXin_Voice.md`: **皮肤** (口吻)。
*   **技能端 (Skill)**:
    *   **Transcript Generator**: `compile_transcript.md` 定义了如何将上述三者融合的 Prompt Chain。
*   **输出端 (Artifact)**:
    *   `S0x_Transcript.md`: 包含“教材知识点”但用“导演口吻”讲述的最终脚本。
```

### 3. 交叉引用机制 (Cross-Referencing System)

为了让 Script (01), Visuals (02), Demo (03) 能够互相索引，使用 **“锚点标签 (Anchor Tags)”**。

*   **Script 文件中**：
    > "同学们，看这张图..." `[REF: Slide_05_SpaceModel]`
    > "现在我们来调混响..." `[ACTION: ACT_03_Reverb_Set]`
*   **Visual 文件中**：
    > `ID: Slide_05_SpaceModel` | Content: 空间三要素图 | Ref_Script: S04_Phase3_Space.md
*   **Demo 文件中**：
    > `ID: ACT_03_Reverb_Set` | Param: Decay 3000ms | Ref_Script: S04_Phase3_Space.md

**优势**：AI 可以编写脚本来自动验证完整性（例如：检查脚本里引用的 PPT 是否真的存在）。

### 3. AI 智能体介入流程 (Active Agent Architecture)

> **核心变更**: 从“文档驱动”转变为“代码驱动”。

*   **Writer Agent (执行)**:
    *   *Trigger*: `python3 .agent/executors/build_factory.py --task writer`
    *   *Mechanism*: 自动装配 `LinXin_Voice` + `Textbook_Index` + `Action_Map`。
    *   *Output*: 包含 "Deep Listening" 留白的严格脚本。

*   **Auditor Agent (审查)**:
    *   *Trigger*: `python3 .agent/executors/build_factory.py --task auditor`
    *   *Check*: 检查“导演思维”与“深听留白”。

*   **Muse Agent (灵感)**:
    *   *Constraint*: 仅在 `00_Structure_Map` 阶段通过 `rules/creative_muse.md` 介入。

---

## 课程内容策略 (Content Strategy)

### 1. 核心策略：Deep Listening (深听)
针对时长不足的问题，我们**放弃水时长**，转为**增加听觉体验**。
在 S02, S04, S05 环节中，强制植入 **3-5分钟的“深听/导听”环节**。
*   *形式*: 播放音频 -> 留白(Silence) -> 引导学生闭眼感受 -> 揭晓答案。
*   *价值*: 将“技术操作”转化为“听觉审美”。

### 1. 课程结构设计 (1小时 / 60分钟)

| 时间分配 | 环节 | 内容重点 | 涉及章节 |
| :--- | :--- | :--- | :--- |
| **00:00 - 05:00** | **导入 (Intro)** | **我是林昕老师**。不仅仅是修音，我们要当“声音导演”。<br>**【关键修补】坏案例展示**：用30秒快速过一遍“不仅有底噪，还有嗡嗡声、爆音”的音频。<br>**【新增】工具速览 (Toolbox Flash)**：快速扫描跳过的工具（多普勒雷达测速音、吉他失真效果、卡雪机中置提取），只看结果不讲参数，建立全景认知。 | 6.7 引言 / 6.11 / (Ext: 6.6.x/6.8.x) |
| **05:00 - 15:00** | **环节一：净化 (Purify)** | **导演决策 (Key Q)**：*这底噪是脏点还是氛围？*<br>**实操**：对比“过度降噪（死寂/失真）”与“适度保留（真实感）”。 | 6.6 (N) |
| **15:00 - 30:00** | **环节二：塑形 (Sculpt)** | **导演决策**：*是旁白（客观/磁性）还是剧中人（主观/变形）？*<br>**实操**：尝试两种变调方案，选择一种符合剧情的。 | 6.8 (C) / 6.10 (E) |
| **30:00 - 45:00** | **环节三：置景 (Space)** | **导演决策**：*听众是在角色脑子里（干音）还是在山洞里（湿音）？*<br>**实操**：用混响干湿比来定义“距离感”。 | 6.7 (B) |
| **45:00 - 55:00** | **环节四：定位 (Position)** | **导演决策**：*这是回忆（单声道/窄）还是现实（立体声/宽）？*<br>**实操**：用立体声扩展器改变声场的“宽窄”来叙事。 | 6.9 (O) |
| **55:00 - 60:00** | **总结 (Summary)** | 回放作品。强调：**每一个参数调整，都是一次对“听众位置”的重新定义。** | 6.11 |

### 2. MVP 演示实验设计： “声音变形记”

> [!IMPORTANT]
> **MVP 演示实验核：声音导演的“第三条路”**
> 不仅仅教学生“怎么调参数”，而是教学生**“如果不做这个决定，就别动这个参数”**。
> 整个 MVP 贯穿一个核心约束：**“立场决定参数” (Stance drives Parameters)**。
> 在每一步操作前，林老师都会先问：**“现在，听众站在哪里？”**

**场景设定**：我们将一段普通的读书声（**Plan A: 真人录音 / Plan B: TTS 标准干声**），重构为《爱丽丝漫游奇境》的**“坠落时刻”**。

**教学法升级：决策驱动循环 (Decision-Based Loop)**

1.  **阶段一：净化 (Purify)**
    *   **导演问题**：*我们需要绝对的黑背景，还是保留一点房间的‘人气’？*
    *   **决策**：为了表现“梦境的虚无”，我们决定——**彻底降噪**（比常规更狠一点）。
2.  **阶段二：塑形 (Sculpt)**
    *   **导演问题**：*这个声音是爱丽丝自己（正常），还是她眼中的巨人（变调）？*
    *   **决策**：模拟爱丽丝变小后的听感——**音调下移**，让人声显巨大。
3.  **阶段三：置景 (Space)**
    *   **导演问题**：*她是在窄小的兔子洞，还是掉进了无底深渊？*
    *   **决策**：使用**长尾音的卷积混响**，制造“无底洞”的坠落感。
4.  **阶段四：定位 (Position)**
    *   **导演问题**：*声音是从头顶传来（压迫感），还是在耳边低语（亲密感）？*
    *   **决策**：使用**立体声扩展**，将声音推向两侧，制造一种“被声音包围”的眩晕感。

### 3. PPT 内容制作方案 (Content Only)

> [!TIP]
> **视觉策略升级：电影式视觉索引 (Cinematic Visual Index)**
> 采纳 OpenAI 建议，但为避免版权风险与录制复杂度，使用 **“电影静帧/概念图”** 代替视频片段。
> 核心逻辑：**把电影画面作为“声音-空间关系”的视觉锚点**。

*   **P3 知识树**：展示 Part 1 (A/L/D/Q/U) 与 Part 2 (N/B/C/O/E) 的关系 (N-B-C-O-E 对应 净-境-塑-位-变)。
*   **P5 核心图示：空间建模三要素 (The Space Model)**
    *   *画面*：左[人/声源] —— 中[盒子/空间] —— 右[耳朵/听众]。
    *   *文案*：“混响不是加效果，而是定义听众站在哪里。”
*   **P8-P12 MVP 视觉脚本 (配合爱丽丝案例)**
    *   **Phase 1 净化**：画面参考《黑客帝国》白色空间（纯净、无杂质）。
    *   **Phase 2 塑形**：画面参考《爱丽丝》喝下药水变大/变小（对应变调）。
    *   **Phase 3 置景**：画面参考《爱丽丝》掉进无底洞（对应长混响/大空间）。
    *   **Phase 4 定位**：画面参考《盗梦空间》折叠城市或镜像（对应立体声宽场）。

### 4. 逐字稿 (Script) 撰写策略

> [!WARNING]
> **时间与人格一致性控制**
> - **字数核减**：原定 8000 字存在超时风险，现强制下调至 **6000 字**（预留更多操作缓冲）。
> - **人格一致性**：引入 `00_Master_Outline.md` 作为“剧本圣经”，Agent 生成分集脚本时强制读取此文件，确保“林昕”不会在后半程忘记前半程的伏笔。

*   **口吻**：**教师口吻（林昕）**。
*   **标注**：
    *   `(PPT: 提供内容要点)` [REF: Slide_ID]
    *   `(操作: 详细步骤)` [ACTION: Act_ID]
    *   `(趣味互动)`

## 验证计划 (Verification Plan)

## 验证计划 (Verification Plan)

### 1. CI/CD 自动化审查 (GitHub Actions)
我们已部署 **GitHub Action Workflow (`.github/workflows/verify_courseware.yml`)**，每次 Push 代码时自动执行以下检查：

*   **[Quality Gate 1] 链接完整性校验**：运行 `.agent/skills/validate_links.py`。
    *   *检查项*：确保脚本中引用的 `[REF: Slide_ID]` 和 `[ACTION: Act_ID]` 在数据库中存在。
    *   *失败后果*：如果存在死链，Pipeline 标记为 **Failed**。

*   **[Quality Gate 2] 课时与字数测算**：运行 `.agent/skills/validate_script_length.py`。
    *   *检查项*：
        1.  **语音时长**：CNChars / 240 + ENWords / 130。
        2.  **动作时长**：Actions * 15s + Playbacks * 20s。
        3.  **总时长门限**：目标 60分钟 (±5分钟)。
    *   *反馈*：在 Console 输出详细的时长分析报告，指导内容扩充或删减。

### 2. 人工验证
1.  **逻辑自洽性**：检查逐字稿中的操作步骤是否与教程原文（6.6-6.10）的参数描述一致。
2.  **内容完整性**：确认 `Toolbox Flash` (工具速览) 环节已覆盖被跳过的知识点。
