# Design Document: Agent to Power Migration

## Overview

This design describes the migration of an existing `.agent` directory architecture to Kiro Power format. The migration transforms three skills (lab-factory, validation-suite, transcript-compiler) into standalone Kiro Powers while preserving all functionality. The key challenge is that Kiro Powers have limited support for executable files (Python/JSX scripts), which we address through an "external mounting" strategy where scripts remain in their original locations and are referenced via paths in power.md files.

The migration is designed to be "quick and usable" - prioritizing getting the Powers working immediately over perfection. The original `.agent` structure remains untouched to ensure backward compatibility during the transition period.

## Architecture

### High-Level Structure

```
.kiro/powers/
├── lab-factory-power/
│   ├── power.md                    # Main documentation with YAML frontmatter
│   └── steering/
│       └── new-asset-workflow.md   # Converted from workflows/new_asset.md
├── validation-suite-power/
│   └── power.md                    # Main documentation with YAML frontmatter
└── transcript-compiler-power/
    └── power.md                    # Main documentation with YAML frontmatter

.agent/                              # Original structure (preserved, not modified)
├── skills/
│   ├── lab-factory/
│   │   ├── lib/                    # JSX libraries (referenced by power.md)
│   │   └── scripts/                # Scripts (referenced by power.md)
│   ├── validation-suite/
│   │   └── scripts/                # Python scripts (referenced by power.md)
│   └── transcript_compiler/
├── executors/
│   └── build_factory.py            # Referenced by transcript-compiler-power
├── rules/                          # Integrated into power.md files
├── knowledge/                      # Referenced or integrated into power.md files
├── styles/                         # Integrated into power.md files
└── workflows/                      # Converted to steering files
```

### Migration Strategy

The migration follows a "flatten and reference" approach:

1. **Flatten**: Consolidate SKILL.md, relevant rules, knowledge, and styles into a single power.md per Power
2. **Reference**: Keep executable scripts in original locations, document their paths and usage in power.md
3. **Convert**: Transform workflows into steering files within Power directories
4. **Preserve**: Leave original `.agent` structure completely untouched

### External Mounting Pattern

Since Kiro Powers cannot directly execute Python/JSX scripts within the power folder, we use "external mounting":

- Scripts remain at their original paths (e.g., `.agent/skills/lab-factory/lib/Audition.jsx`)
- power.md documents the script location with absolute or relative paths
- power.md includes complete command-line usage examples
- power.md documents prerequisites, dependencies, and execution context

This allows the Power to instruct the Kiro agent to execute scripts via bash commands while keeping the Power directory clean and Markdown-focused.

## Components and Interfaces

### Power.md Structure

Each power.md file follows this structure:

```markdown
---
name: Power Display Name
description: Brief description of the Power's purpose
keywords: [keyword1, keyword2, keyword3]
---

# Power Name

## Overview
Brief introduction to the Power's capabilities

## Core Capabilities
Detailed description of what the Power can do

## Usage Instructions
How to use the Power, including:
- Prerequisites
- Setup steps
- Common workflows

## Script References
For each external script:
- **Purpose**: What the script does
- **Location**: Absolute or relative path
- **Usage**: Command-line example with parameters
- **Dependencies**: Required libraries or tools
- **Execution Context**: Required working directory

## Rules and Protocols
Integrated rules that apply to this Power

## Knowledge Base
Integrated or referenced knowledge relevant to this Power

## Examples
Concrete usage examples

## Troubleshooting
Common issues and solutions
```

### Lab Factory Power

**File**: `.kiro/powers/lab-factory-power/power.md`

**YAML Frontmatter**:
```yaml
name: Lab Factory
description: Adobe Audition automation toolkit for audio asset generation and lab setup
keywords: [audition, automation, audio, jsx, extendscript, asset-generation]
```

**Content Integration**:
- Merge `.agent/skills/lab-factory/SKILL.md` as the core content
- Integrate `.agent/rules/rule_mvp_conventions.md` into the Rules section
- Integrate `.agent/knowledge/Audition_Skills_Map.md` into the Knowledge Base section
- Reference JSX library locations at `.agent/skills/lab-factory/lib/`
- Document the Audition.jsx API with all namespaces (IO, Session, Track, Clip, Markers, State, Log)
- Document the Universal_Lab_Builder.jsx usage pattern
- Include the "Traffic Light" robustness protocol (200/4xx/5xx status codes)
- Document known API limitations (view control, tool interaction, interactive effects)
- Include fast debug protocol with sentinel logging

**Script References**:
- `Audition.jsx`: Location, API documentation, include pattern for manifest-based usage
- `Universal_Lab_Builder.jsx`: Location, usage pattern, manifest structure
- `env_context.jsx`: Location, purpose
- `time_utils.jsx`: Location, purpose

**Steering File**: Convert `.agent/workflows/new_asset.md` to `.kiro/powers/lab-factory-power/steering/new-asset-workflow.md`

### Validation Suite Power

**File**: `.kiro/powers/validation-suite-power/power.md`

**YAML Frontmatter**:
```yaml
name: Validation Suite
description: Project health checks, link validation, and pedagogy auditing tools
keywords: [validation, testing, quality, links, consistency, pedagogy]
```

**Content Integration**:
- Merge `.agent/skills/validation-suite/SKILL.md` as the core content
- Document all validation capabilities (link integrity, script length, consistency, pedagogy audit)

**Script References**:
- `validate_links.py`: Location `.agent/skills/validation-suite/scripts/`, usage `python3 .agent/skills/validation-suite/scripts/validate_links.py`
- `validate_script_length.py`: Location, usage with `--file` parameter
- `validate_consistency.py`: Location, usage
- Reference to `docs/pedagogy_auditor.md` for manual audit checklist

### Transcript Compiler Power

**File**: `.kiro/powers/transcript-compiler-power/power.md`

**YAML Frontmatter**:
```yaml
name: Transcript Compiler
description: Compile course transcripts from structured outlines using LinXin pedagogical style
keywords: [transcript, compiler, course, content, pedagogy, linxin, courseware]
```

**Content Integration**:
- Merge `.agent/skills/transcript_compiler/SKILL.md` as the core content
- Integrate `.agent/styles/LinXin_Voice.md` into the Style Guide section
- Integrate `.agent/rules/rule_workflow_protocol.md` into the Workflow Protocol section
- Integrate `.agent/rules/rule_pedagogy_scaffolding.md` into the Pedagogy section
- Integrate `.agent/rules/rule_script_standards.md` into the Standards section
- Integrate `.agent/rules/rule_narrative_consistency.md` into the Quality section
- Reference `.agent/knowledge/Textbook_Index.md` location
- Reference `.agent/knowledge/Chapter_Mapping.md` location

**Executor Reference**:
- `build_factory.py`: Location `.agent/executors/build_factory.py`
- Usage for writer mode: `python3 .agent/executors/build_factory.py --task writer --section S02`
- Usage for auditor mode: `python3 .agent/executors/build_factory.py --task auditor --file path/to/file.md`
- Document the prompt assembly process
- Document input requirements (Structure_Map, Performance_Map, Design_Spec, Textbook_Index)

**Quality Check Integration**:
Include the quality checklist from SKILL.md:
- LinXin identity verification
- "Constructing space" pedagogical approach
- Technical parameter accuracy
- Deep listening (留白) markers
- PPT reference preservation

## Data Models

### YAML Frontmatter Schema

```yaml
name: string              # Display name of the Power (required)
description: string       # Brief description (required)
keywords: array<string>   # Search keywords (required, 3-6 recommended)
```

### Script Reference Structure

For each external script documented in power.md:

```markdown
### Script Name

**Purpose**: Brief description of what the script does

**Location**: `relative/or/absolute/path/to/script.ext`

**Usage**:
```bash
command path/to/script.ext [parameters]
```

**Parameters**:
- `--param1`: Description
- `--param2`: Description

**Dependencies**:
- Dependency 1
- Dependency 2

**Execution Context**: Required working directory or environment setup

**Example**:
```bash
python3 .agent/skills/validation-suite/scripts/validate_links.py
```
```

### Migration Mapping

```typescript
interface MigrationMapping {
  skill: {
    id: string;              // Original skill ID from manifest.json
    path: string;            // Original path in .agent/skills/
  };
  power: {
    name: string;            // Power display name
    directory: string;       // Power directory name (kebab-case)
    path: string;            // Full path to power directory
  };
  content: {
    skillMd: string;         // Path to original SKILL.md
    rules: string[];         // Paths to integrated rules
    knowledge: string[];     // Paths to integrated/referenced knowledge
    styles: string[];        // Paths to integrated styles
    workflows: string[];     // Paths to workflows (converted to steering)
  };
  scripts: {
    path: string;            // Original script location
    type: 'python' | 'jsx';  // Script type
    referenced: boolean;     // Whether referenced in power.md
  }[];
}
```

## Correctness Properties

属性（Property）是系统在所有有效执行中应该保持为真的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。

### Property 1: 目录命名规范

*对于任何* 技能名称，生成的 Power 目录名称应该是 kebab-case 格式（小写字母，单词用连字符分隔）

**验证需求: Requirements 1.2**

### Property 2: YAML Frontmatter 有效性

*对于任何* 生成的 power.md 文件，其 YAML frontmatter 应该可以被成功解析，并且包含 name、description 和 keywords 三个必需字段

**验证需求: Requirements 1.4, 11.2**

### Property 3: 内容完整性保留

*对于任何* 技能迁移，原始 SKILL.md 中的所有能力描述、代码示例和使用模式都应该出现在生成的 power.md 中

**验证需求: Requirements 1.5, 2.1, 2.6**

### Property 4: 内容集成正确性

*对于任何* 指定的规则、知识或样式文件，如果它被标记为应该集成到某个 Power 中，那么该文件的内容应该出现在对应的 power.md 中

**验证需求: Requirements 2.2, 2.3, 2.4, 8.1, 8.5, 9.1**

### Property 5: 可执行文件隔离

*对于任何* 生成的 Power 目录，其中不应该包含任何 .py 或 .jsx 文件

**验证需求: Requirements 3.1, 3.2, 11.4**

### Property 6: 脚本文档完整性

*对于任何* 在 power.md 中引用的脚本，文档应该包含：脚本路径、命令行使用示例、参数说明、依赖项列表

**验证需求: Requirements 3.3, 3.4, 3.5, 10.2, 10.3, 10.5**

### Property 7: 工作流内容保留

*对于任何* 转换为 steering 文件的工作流，原始工作流中的所有步骤、触发条件和前置条件都应该出现在生成的 steering 文件中

**验证需求: Requirements 7.1, 7.3, 7.4**

### Property 8: 全局规则分发

*对于任何* 标记为全局的规则，它应该出现在所有相关的 Power 的 power.md 文件中

**验证需求: Requirements 8.2**

### Property 9: 路径引用有效性

*对于任何* power.md 中引用的脚本、知识库或执行器路径，该路径指向的文件应该在文件系统中存在

**验证需求: Requirements 11.3**

### Property 10: 原始结构不变性

*对于任何* 迁移操作，.agent/ 目录中的所有文件和目录在迁移前后应该保持完全相同（内容和位置都不变）

**验证需求: Requirements 12.1, 12.2, 12.3**

## Error Handling

### 文件系统错误

**场景**: 无法创建 Power 目录或文件

**处理策略**:
- 检查 .kiro/powers/ 目录是否存在，如不存在则创建
- 检查文件写入权限
- 如果权限不足，报告错误并提供清晰的错误消息
- 提供回滚机制：如果迁移部分失败，清理已创建的不完整文件

**错误消息示例**:
```
错误：无法创建 Power 目录
路径：.kiro/powers/lab-factory-power/
原因：权限不足
建议：请检查目录权限或使用 sudo 运行迁移脚本
```

### 源文件缺失

**场景**: 引用的 SKILL.md、规则文件或知识库文件不存在

**处理策略**:
- 在迁移开始前验证所有必需的源文件是否存在
- 如果关键文件缺失（如 SKILL.md），报告错误并停止迁移
- 如果可选文件缺失（如某些规则文件），记录警告但继续迁移
- 在 power.md 中添加注释说明哪些内容因源文件缺失而未能集成

**错误消息示例**:
```
错误：源文件缺失
文件：.agent/skills/lab-factory/SKILL.md
影响：无法创建 lab-factory-power
建议：请确认 .agent 目录结构完整
```

### YAML 格式错误

**场景**: 生成的 YAML frontmatter 格式不正确

**处理策略**:
- 使用 YAML 解析库验证生成的 frontmatter
- 如果验证失败，记录详细的语法错误信息
- 提供修复建议（如缺少必需字段、缩进错误等）
- 在迁移报告中标记需要手动修复的文件

**错误消息示例**:
```
警告：YAML frontmatter 验证失败
文件：.kiro/powers/lab-factory-power/power.md
问题：缺少必需字段 'keywords'
建议：请手动添加 keywords 字段到 YAML frontmatter
```

### 路径引用错误

**场景**: power.md 中引用的脚本路径不存在

**处理策略**:
- 在生成 power.md 后验证所有引用的路径
- 如果路径不存在，在迁移报告中记录警告
- 提供路径修正建议（如可能的正确路径）
- 不阻止迁移完成，但在报告中明确标记需要修复的引用

**错误消息示例**:
```
警告：脚本路径无效
Power：lab-factory-power
引用路径：.agent/skills/lab-factory/lib/Audition.jsx
状态：文件不存在
建议：请检查脚本是否已移动或重命名
```

### 内容集成冲突

**场景**: 多个源文件包含冲突的信息或重复的章节标题

**处理策略**:
- 使用命名空间或前缀区分来自不同源的内容
- 在 power.md 中使用清晰的章节标题标识内容来源
- 如果检测到重复的章节标题，自动添加后缀（如 "规则：MVP 约定"、"规则：工作流协议"）
- 在迁移报告中记录所有内容合并决策

### 大文件处理

**场景**: 知识库文件过大，不适合完整嵌入 power.md

**处理策略**:
- 设置文件大小阈值（如 50KB）
- 对于超过阈值的文件，使用引用而非嵌入
- 在 power.md 中提供文件路径和简要摘要
- 在迁移报告中记录哪些文件被引用而非嵌入

**处理示例**:
```markdown
## 知识库：教材索引

由于文件较大，完整内容请参考：`.agent/knowledge/Textbook_Index.md`

**摘要**: 该索引包含课程所有章节的映射关系...
```

## Testing Strategy

本迁移项目采用双重测试策略：单元测试验证具体示例和边缘情况，属性测试验证通用正确性属性。

### 单元测试

单元测试专注于具体的迁移场景和边缘情况：

**目录结构测试**:
- 测试三个 Power 目录是否被创建（lab-factory-power, validation-suite-power, transcript-compiler-power）
- 测试每个目录中是否存在 power.md 文件
- 测试 lab-factory-power 中是否存在 steering/ 子目录

**特定内容测试**:
- 测试 lab-factory-power 的 YAML frontmatter 是否包含正确的 keywords
- 测试 validation-suite-power 是否引用了所有验证脚本
- 测试 transcript-compiler-power 是否集成了 LinXin_Voice.md 样式指南
- 测试 build_factory.py 的使用示例是否包含 --task 和 --section 参数

**边缘情况测试**:
- 测试当源文件缺失时的错误处理
- 测试当 .kiro/powers/ 目录不存在时的自动创建
- 测试大型知识库文件（如 Textbook_Index.md）是否被引用而非嵌入
- 测试需要特定工作目录的脚本是否文档化了执行上下文

**集成测试**:
- 测试完整的迁移流程：从 .agent 到 .kiro/powers
- 测试迁移报告是否生成并包含所有必要信息
- 测试原始 .agent 目录在迁移后保持不变

### 属性测试

属性测试使用属性测试库（如 Python 的 Hypothesis 或 JavaScript 的 fast-check）验证通用属性：

**测试配置**:
- 每个属性测试运行最少 100 次迭代
- 每个测试使用标签引用设计文档中的属性
- 标签格式：**Feature: agent-to-power-migration, Property {number}: {property_text}**

**属性测试用例**:

1. **目录命名规范测试**
   - 生成随机技能名称（包含大写、空格、下划线等）
   - 验证输出目录名称符合 kebab-case 格式
   - 标签：**Feature: agent-to-power-migration, Property 1: 目录命名规范**

2. **YAML Frontmatter 有效性测试**
   - 对于任何生成的 power.md 文件
   - 解析 YAML frontmatter 并验证包含 name、description、keywords
   - 标签：**Feature: agent-to-power-migration, Property 2: YAML Frontmatter 有效性**

3. **内容完整性保留测试**
   - 对于任何 SKILL.md 文件
   - 验证其中的代码块和关键术语出现在生成的 power.md 中
   - 标签：**Feature: agent-to-power-migration, Property 3: 内容完整性保留**

4. **内容集成正确性测试**
   - 对于任何指定要集成的规则/知识/样式文件
   - 验证该文件的内容片段出现在目标 power.md 中
   - 标签：**Feature: agent-to-power-migration, Property 4: 内容集成正确性**

5. **可执行文件隔离测试**
   - 对于任何生成的 Power 目录
   - 递归检查目录中不存在 .py 或 .jsx 文件
   - 标签：**Feature: agent-to-power-migration, Property 5: 可执行文件隔离**

6. **脚本文档完整性测试**
   - 对于 power.md 中的任何脚本引用
   - 验证包含路径、使用示例、参数说明、依赖项
   - 标签：**Feature: agent-to-power-migration, Property 6: 脚本文档完整性**

7. **工作流内容保留测试**
   - 对于任何转换的工作流文件
   - 验证原始步骤和条件出现在 steering 文件中
   - 标签：**Feature: agent-to-power-migration, Property 7: 工作流内容保留**

8. **全局规则分发测试**
   - 对于任何标记为全局的规则
   - 验证它出现在所有相关 Power 的 power.md 中
   - 标签：**Feature: agent-to-power-migration, Property 8: 全局规则分发**

9. **路径引用有效性测试**
   - 对于 power.md 中的任何路径引用
   - 验证该路径在文件系统中存在
   - 标签：**Feature: agent-to-power-migration, Property 9: 路径引用有效性**

10. **原始结构不变性测试**
    - 在迁移前后对 .agent 目录进行哈希计算
    - 验证哈希值完全相同
    - 标签：**Feature: agent-to-power-migration, Property 10: 原始结构不变性**

### 测试工具选择

**Python 实现**:
- 属性测试库：Hypothesis
- YAML 解析：PyYAML
- 文件系统操作：pathlib
- 哈希计算：hashlib

**测试执行**:
```bash
# 运行所有测试
pytest tests/ -v

# 只运行属性测试
pytest tests/ -v -m property

# 只运行单元测试
pytest tests/ -v -m unit
```

### 测试覆盖率目标

- 代码覆盖率：>90%
- 属性测试覆盖所有 10 个正确性属性
- 单元测试覆盖所有 12 个需求的关键验收标准
- 边缘情况测试覆盖所有错误处理场景

