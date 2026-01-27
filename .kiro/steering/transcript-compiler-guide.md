# Transcript Compiler - 课程讲稿编译器

> **来源**: `.agent/skills/transcript_compiler/` 和 `.agent/executors/`
> **类型**: 讲稿生成和质量审计工具

## 概述

Transcript Compiler 使用 LinXin 教学风格从结构化大纲编译课程讲稿。

## 核心工具: build_factory.py

**位置**: `.agent/executors/build_factory.py`

### Writer 模式（生成讲稿）

```bash
python3 .agent/executors/build_factory.py --task writer --section S02
```

**参数**:
- `--task writer`: 指定为写作模式
- `--section`: 章节标识符（如 S02, S03）

**依赖**:
- Python 3.8+
- OpenAI API key（环境变量）
- 项目结构文件（Structure_Map, Performance_Map）

### Auditor 模式（质量审计）

```bash
python3 .agent/executors/build_factory.py --task auditor --file path/to/script.md
```

**参数**:
- `--task auditor`: 指定为审计模式
- `--file`: 要审计的讲稿文件路径

## LinXin 教学风格

参考 `.agent/styles/LinXin_Voice.md` 了解：
- 语言风格特点
- 教学方法
- 叙事技巧

## 工作流程协议

参考 `.agent/rules/rule_workflow_protocol.md` 了解：
- 讲稿开发流程
- 质量检查标准
- 审核要点

## 质量检查清单

1. **LinXin 身份验证**: 确保使用第一人称"我"
2. **"构建空间"教学法**: 验证教学方法
3. **技术参数准确性**: 检查技术细节
4. **深度聆听标记**: 确保有"留白"时刻
5. **PPT 引用保留**: 保持 PPT 参考完整

## 输入要求

- **Structure_Map**: 章节结构映射
- **Performance_Map**: 表演指导
- **Design_Spec**: 设计规范
- **Textbook_Index**: 教材索引（`.agent/knowledge/Textbook_Index.md`）
- **Chapter_Mapping**: 章节映射（`.agent/knowledge/Chapter_Mapping.md`）

## 执行上下文

从项目根目录运行，确保：
- 环境变量已设置（OpenAI API key）
- 项目结构文件存在
- 有写入权限

## 相关文档

- 完整文档: `.kiro/powers/transcript-compiler-power/POWER.md`
- LinXin 风格: `.agent/styles/LinXin_Voice.md`
- 工作流程: `.agent/rules/rule_workflow_protocol.md`
- 教学脚手架: `.agent/rules/rule_pedagogy_scaffolding.md`
- 脚本标准: `.agent/rules/rule_script_standards.md`
- 叙事一致性: `.agent/rules/rule_narrative_consistency.md`
- 教材索引: `.agent/knowledge/Textbook_Index.md`
- 章节映射: `.agent/knowledge/Chapter_Mapping.md`
