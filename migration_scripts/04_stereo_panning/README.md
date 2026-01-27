# 04_Stereo_Panning - Visceral Panning (具象化心理声像)

本目录包含 "Stereo Panning (立体声声像)" 课程的所有相关资源。该课程旨在教授学生如何通过声像布局（Panning）构建心理空间，区分"内"（心跳）与"外"（威胁）。

## 📁 目录结构

*   **`assets/`**: 存放本课程专用的练习素材 (心跳、环境威胁音、人声)。
*   **`courseware/`**: 包含教学文档。
    *   `lesson_plan.md`: 教师教案。
    *   `lab_guide.md`: 学生实验指南。
*   **`scripts/`**: 自动化工具。
    *   `jsx_automation/`: Adobe Audition 自动化脚本 (JS)。
*   **`sessions/`**: 存放 Audition 工程文件 (.sesx)。

## 🚀 快速开始

### 教师 (自动化排课)
1.  打开 Adobe Audition。
2.  新建一个多轨会话 (Multitrack Session)。
3.  运行 `scripts/jsx_automation/Setup_Panning_Lab.jsx`。
    *   *脚本会自动导入所有素材，但默认全部居中 (Center)，制造"单声道灾难"以供教学演示。*

### 学生 (手动练习)
1.  阅读 `courseware/lab_guide.md`。
2.  尝试将不同的声音移动到 Left/Right，构建清晰的声场。
