# Validation Suite - 项目健康检查工具

> **来源**: `.agent/skills/validation-suite/`
> **类型**: Python 验证脚本集合

## 概述

Validation Suite 提供项目健康检查工具，包括链接验证、脚本长度检查和一致性验证。

## 可用脚本

### 1. validate_links.py
**功能**: 验证 Markdown 文件中的所有内部和外部链接

**使用方法**:
```bash
python3 .agent/skills/validation-suite/scripts/validate_links.py
```

**参数**:
- `--file`: 指定要验证的文件（可选）
- `--verbose`: 启用详细输出

**依赖**:
- Python 3.8+
- requests 库

### 2. validate_script_length.py
**功能**: 检查脚本长度是否符合标准

**使用方法**:
```bash
python3 .agent/skills/validation-suite/scripts/validate_script_length.py --file path/to/script.md
```

**参数**:
- `--file`: 要验证的脚本文件路径（必需）

### 3. validate_consistency.py
**功能**: 验证项目文件之间的一致性

**使用方法**:
```bash
python3 .agent/skills/validation-suite/scripts/validate_consistency.py
```

**执行上下文**: 从项目根目录运行

## 教学审计

参考 `.agent/skills/validation-suite/docs/pedagogy_auditor.md` 获取手动审计清单。

## 脚本位置

所有验证脚本位于: `.agent/skills/validation-suite/scripts/`

## 相关文档

- 完整文档: `.kiro/powers/validation-suite-power/POWER.md`
- 教学审计指南: `.agent/skills/validation-suite/docs/pedagogy_auditor.md`
