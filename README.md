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

根据 Adobe Audition 的实际功能逻辑与音频工程原理，对  [[S02....]] 进行审查与修正。

请分析 [[@S04_Phase3_Space.md]]  的 gap, 并制定详尽的计划和任务, 通过深度网络搜索, 对课程中知识面进行拓展,例如相关度较强的艺术家, 著名项目, 普及知识, 拓展更多有趣的故事

请作为该文档的“系统构建者”，尝试在脑中还原其逻辑全貌，并执行以下认知压力测试：
- 颗粒化复述： 不使用原文档术语，用极简白话复述 [[@S05_Phase4_Position.md]] 的操作链路。每一步必须回答：“这一步凭什么能推导出下一步？”
- 断层即时标注： 在复述过程中，一旦遇到以下情况，请立刻用 【此处有断层】 标出并详细描述：
    - 逻辑跳跃（从 A 到 B 缺乏中间支撑）。
    - 隐性前提（文档没说，但操作时必须默认存在的条件）。
    - 模糊黑盒（虽然有术语，但实际操作步骤不透明的地方）。
- 费曼审查： 检查你刚才的复述，如果发现自己仍在依赖高大上的抽象词汇（如“优化”、“对齐”、“定位”等），请对其进行二次暴力拆解，直到即使是外行也能听懂。
- 脆弱性提问： 针对你认为最核心的一个环节，提出一个“如何”和“为什么”的问题，尝试挑战该逻辑的稳定性。