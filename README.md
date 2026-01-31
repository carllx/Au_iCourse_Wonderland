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
    python3 .agent/executors/build_factory.py --task auditor --file 03_Scripts/S02.md
    ```

> **Note**: 严禁 AI 凭空生成内容。必须执行上述指令获取 Context。

## 🛠️ 协作者指南 (Contributor's Guide)

### 场景 A: 添加新图 (Visuals Workflow)
**原则**: Spec-First (先定义，再生成，后覆盖)
1.  **Define**: 在 `02_Visuals/Slide_Database.md` 里新起一行，定义 `ID`, `Type` 和 `Concept`。
2.  **Generate**: 运行自动化脚本生成 **"灰盒占位图"** (Greybox)。
    ```bash
    python .agent/skills/validation-suite/scripts/scaffold_visual_assets.py
    ```
3.  **Produce**: 用 PS 成品覆盖生成的灰盒 PNG。素材(Raw)请加 `src_` 前缀放入同级目录。

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
*   🔄 **执行中**: S02-S05 脚本重构中。

## 常用的prompt

根据 Adobe Audition 的实际功能逻辑与音频工程原理，对  [[S02....]] 进行审查与修正。

请分析 [[@S04_Phase3_Space.md]]  的 gap, 并制定详尽的计划和任务, 通过深度网络搜索, 对课程中知识面进行拓展,例如相关度较强的艺术家, 著名项目, 普及知识, 拓展更多有趣的故事

为了能够构建连贯且相互关联的心理图式。请对 [[ @S01_Intro.md ]] 进行精细复述与自我演练与自我解释, 提出 “为什么” 和 “如何” 的问题，并能费曼技巧式复述与审查Feynman Re-explanation 用自己的话解释概念，审查出现有信息知识结构是否有积极的关联是否存在断层, 操作步骤是否有漏洞.