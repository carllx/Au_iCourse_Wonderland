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
*   `01_Scripts/`: 课程逐字稿 (Markdown)
*   `02_Visuals/`: PPT 视觉数据库
*   `03_MVP_Demo/`: 演示操作映射表
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
    python3 .agent/executors/build_factory.py --task auditor --file 01_Scripts/S02.md
    ```

> **Note**: 严禁 AI 凭空生成内容。必须执行上述指令获取 Context。

## 当前状态
*   ✅ **工程升级**: 完成 "Active Agent" 架构改造。
*   ✅ **策略升级**: 引入 "Deep Listening" (深听) 策略，填补时长缺口。
*   🔄 **执行中**: S02-S05 脚本重构中。
