# 技能：验证套件 (Validation Suite)

---
name: Validation Suite
id: validation-suite
description: 一组用于维护项目健康度、文档一致性和教学质量的自动化工具集合。
trigger: /validate, 检查一致性, 验证链接, 审计脚本
---

> **← 来源**: `.agent/manifest.json` → `skills[id="validation-suite"]`

## 概述

| 属性 | 值 |
|-----|-----|
| **ID** | `validation-suite` |
| **状态** | ✅ Active |
| **触发词** | /validate, 检查一致性, 验证链接, 审计脚本 |
| **描述** | 一组用于维护项目健康度、文档一致性和教学质量的自动化工具集合。 |

## 能力清单 (Capabilities)

### 1. 链接完整性检查
*   **脚本**: `scripts/validate_links.py`
*   **用途**: 扫描 Markdown 文件中的死链、相对路径错误。
*   **用法**: `python3 .agent/skills/validation_suite/scripts/validate_links.py`

### 2. 脚本长度与节奏分析
*   **脚本**: `scripts/validate_script_length.py`
*   **用途**: 估算朗读时长，确保 S0x 脚本不超载。
*   **用法**: `python3 .agent/skills/validation_suite/scripts/validate_script_length.py --file 03_Scripts/S02_Phase1_Purify.md`

### 3. 一致性验证
*   **脚本**: `scripts/validate_consistency.py`
*   **用途**: 检查文件名、标题与 `00_Structure_Map` 的对齐情况。

### 4. 教学法审计 (Pedagogy Auditor)
*   **指南**: `docs/pedagogy_auditor.md`
*   **脚本**: `scripts/validate_pedagogy.py`
*   **用途**: 强制执行“林昕风格”（禁止裸参数，强制留白）。
*   **用法**: `python3 .agent/skills/validation_suite/scripts/validate_pedagogy.py`

### 5. 一键全检 (Master Commander)
*   **脚本**: `scripts/validate_project.py`
*   **用途**: 串行执行所有验证脚本，并在CI/CD前进行自我体检。
*   **用法**: `python3 .agent/skills/validation_suite/scripts/validate_project.py`

## 开发指南

所有新的验证脚本应放置在 `scripts/` 目录下，并在本文件中注册。
