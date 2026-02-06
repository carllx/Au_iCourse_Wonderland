# Audition Smart Course: Project Wonderland 🎧
> **Project Codename**: `Audition_SmartCourse_Wonderland`  
> **Repository**: [Au_iCourse_Wonderland](https://github.com/carllx/Au_iCourse_Wonderland)

## 项目简介 (Project Overview)
本项目旨在基于 Adobe Audition 构建一套深度结合“技术”与“艺术造梦”的智慧课程。
核心案例：《爱丽丝漫游奇境》的声音重构。

## 自动化质量保障 (CI/CD)
本项目采用 **GitHub Actions** 进行自动化课程质量审查。
每当代码提交 (Push) 时，系统会自动运行：

1.  **🔗 链接完整性校验** (`validate_links.py`): 确保脚本引用的 PPT 和 演示操作 真实存在。
2.  **⏱️ 课时与字数测算** (`validate_script_length.py`): 实时估算课程时长，确保贴近 60分钟 标准。

## 目录结构
*   `03_Scripts/`: 课程逐字稿 (Markdown)
*   `02_Visuals/`: PPT 视觉数据库
*   `01_MVP_Demo/`: 演示操作映射表 (架构规范见 `ARCHITECTURE_GUIDE.md`)
*   `04_Delivery/`: H5 交互式预览系统 (React + Vite)
*   `.agent/`: **[核心] 智能体工程**
    *   `executors/`: 提示词装配工厂 (`build_factory.py`)
    *   `rules/`: 行为准则 (`workflow_protocol.md`)
    *   `skills/`: 技能定义与校验脚本

## 🤖 智能体工作流 (Active Agent Workflow)

本项目强制采用 **“工厂模式” (Prompt Factory)** 进行内容生成。

1.  **生成脚本 (Writer Mode)**:
    ```bash
    python3 .agent/executors/build_factory.py --task writer --section S02
    ```
2.  **审查质量 (Auditor Mode)**:
    ```bash
    python3 .agent/executors/build_factory.py --task auditor --file 03_Scripts/S02_Phase1_Purify.md
    ```

> **Note**: 严禁 AI 凭空生成内容。必须执行上述指令获取 Context。

## 🛠️ 协作者指南 (Contributor's Guide)

### 场景 A: 添加新图 (Visuals Workflow)
**原则**: Spec-First (先定义，再生产)
1.  **Define**: 在 `02_Visuals/Slide_Database.md` 里定义 Slide。
2.  **Preview**: 启动 H5 预览 (`npm run dev`)，查看系统生成的 **Live Greybox**（包含布局和指令）。
3.  **Produce**: 制作素材，命名为 `Sxx_...` 放入 `02_Visuals/assets/[Module]/` 目录。
4.  **Verify**: H5 会自动检测并显示新素材，替代动态灰盒。

### 场景 B: 添加新音/资产 (Audio Workflow)
2.  **Generate**: 编写/运行 `01_MVP_Demo/_Pipeline` 下的 Python 脚本生成 `.wav`。

### 场景 C: 交互式预览 (Interactive Preview)
**原则**: H5 是验证脚本、音频与视觉契合度的 **终极手段**。
1.  **Sync**: 运行 `npm run sync` 解析脚本与检测素材。
2.  **Preview**: 运行 `npm run dev` 在浏览器中实时查看课程效果。

## 🧰 常用工具箱 (Project Toolkit)

以下脚本可由用户直接运行，用于辅助课程开发与内容提取：

### 1. 课程时长与文本提取
*   **用途**: 估算课程演示时长（含动作与留白），或提取纯净口播稿。
*   **指令**:
    ```bash
    # ⏱️ 此时长检查
    python .agent/skills/validation-suite/scripts/validate_script_length.py

    # 📝 提取纯文本 (自动保存至 03_Scripts/tts/*.txt)
    python .agent/skills/validation-suite/scripts/validate_script_length.py --dump-text
    ```

### 2. 链接完整性自检 (CI/CD)
*   **用途**: 检查脚本中引用的图片、音频资产是否存在死链。
*   **指令**:
    ```bash
    python .agent/skills/validation-suite/scripts/validate_links.py
    ```

### 3. 🛡️ 教学法审计 (Pedagogy Audit)
*   **用途**: 强制执行 "林昕风格" (Director's Voice)。检查脚本是否包含必要的 "Deep Listening" 留白，以及数字参数旁是否有叙事性描述。
*   **指令**:
    ```bash
    python .agent/skills/validation-suite/scripts/validate_pedagogy.py
    ```

### 4. 🚀 一键全检 (Project Health Check)
*   **用途**: 串行执行上述所有脚本，并在 CI/CD 前进行自我体检。
*   **指令**:
    ```bash
    python .agent/skills/validation-suite/scripts/validate_project.py
    ```

### 5. 📱 H5 预览系统 (Interactive Preview)
*   **用途**: 提供“所见即所得”的课程预览，支持音频/字幕/PPT同步播放，自动回落灰盒布局。
*   **指令**:
    ```bash
    cd 04_Delivery/h5_preview && npm run sync && npm run dev
    ```

### 6. 🎬 Script-to-Timeline 自动化 (New v1.3)
*   **用途**: 自动对齐 TTS 音频与脚本，生成精确时间轴与视频占位符。无需人工打点。
*   **指令**:
    ```bash
    # 1. 注入时间轴
    python 04_Delivery/h5_preview/scripts/build_timeline.py [Section_ID] (e.g. S03)
    
    # 2. 生成占位视频
    python 04_Delivery/h5_preview/scripts/gen_placeholders.py [Section_ID] (e.g. S03)
    ```

## 当前状态
*   ✅ **策略升级**: 引入 "Deep Listening" (深听) 策略，填补时长缺口。
*   ✅ **资产重构**: 视觉资产已完成 "Greybox" 灰盒化与模块化迁移。
*   ✅ **交互升级**: H5 预览系统上线 (React + Vite)，支持物理素材热重载。
*   🔄 **执行中**: S05 Positioning 正在进行验证。

## 常用的prompt

### NotebookLM Technical Review
根据 Adobe Audition 的实际功能逻辑与音频工程原理，对  [[S02....]] 进行审查与修正。

### Deep google Search 
请分析 [[@S04_Phase3_Space.md]]  的 gap, 并制定详尽的计划和任务, 通过深度网络搜索, 对课程中知识面进行拓展,例如相关度较强的艺术家, 著名项目, 普及知识, 拓展更多有趣的故事


### Deep Listen
请作为该文档的“系统构建者”，执行以下**两阶段深度审查**,撰写审查报告. ：

### Phase A: 全链路脑内模拟 (The Dynamic Simulation)
*请在脑海中从头到尾“跑”一遍脚本，执行以下三步闭环：*

1.  **动作 - 颗粒化复述**：
    不使用原文档术语，用极简白话复述整条操作链路。每一步必须回答：“这一步凭什么能推导出下一步？”
2.  **监控 - 断层即时标注**：
    在复述过程中，一旦出现以下卡顿，立即打标：
    *   **逻辑断层**：从 A 到 B 缺乏铺垫。
    *   **情绪断连**：前文还在讲物理，后文突然煽情。
3.  **验收 - 费曼导演视角**：
    检查你的复述：这句话是让观众“如临深渊”（沉浸），还是让他们“出戏去查书”（说教）？

### Phase B: 静态特征扫描 (The Static Scan)
*针对特定标签进行定点排雷：*

1.  **“掉书袋”拦截** (`> [PHILOSOPHY/CULTURAL_REF]`)：
    *   **标准**：禁止“说明书式”背景介绍。
    *   **测试**：如果听众需要去百度“赫拉是谁”才能懂，这就是废话。必须把“知识点”转化为直觉的“体验感”。
2.  **技术-心理桥接** (`> [TECH NOTE/Action]`)：
    *   **标准**：禁止“裸露的物理定义”。
    *   **测试**：如果你只解释了“Haas效应是40ms延迟”，不及格。你必须解释“40ms是自我分裂的边界”。
3.  **盲区扫描 (The Blind Spot Check)**：
    *   **标准**：严禁“隐形参数”。
    *   **测试**：检查脚本中是否有 `隐喻 (参数)` 的结构（如 `调整大小 (Room Size)`）。TTS 解析器会吞噬括号内容，导致听众只听到“调整大小”而不知道调哪个。
    *   **修正**：必须改为显性口语：`利用 **Room Size** 来调整大小`。

4.  **视觉先行原则 (Visual-First Logic)**：
    *   **标准**：原则上遵循“先看后听”，但**交互式动作**例外。
    *   **测试**：静态Slide应在Audio前；动态操作(Action)允许Audio Prompt在Visual Action之前（先提示后执行）。
    *   **原理**：环境需预加载 (Visual First)；动作需语音引导 (Audio First)。