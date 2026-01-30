---
trigger: glob
description: 强制执行文档职责边界,防止越界
globs: 
  - 03_Scripts/*.md
  - 02_Visuals/Slide_Database.md
  - 03_Scripts/00_Structure_Map.md
---

# 规则:文档职责边界协议 (Document Boundary Protocol)

**生效范围**: 所有涉及课程内容、视觉资产、音频资产的文档

## 1. 核心原则 (SSOT - Single Source of Truth)

> **每种信息只能在一个地方定义,其他地方只能引用。**

## 2. 职责划分表

| 文档 | 唯一职责 | 允许引用 | 禁止包含 |
|:---|:---|:---|:---|
| `00_Structure_Map.md` | 课程结构、时间轴、教学节奏 | Slide ID, Action ID | ❌ 视觉设计细节 |
| `Slide_Database.md` | PPT 视觉内容、文字、类型 | - | ❌ 课程结构 |
| `S0x_*.md` (Scripts) | 讲课逐字稿、演示动作 | Slide ID, Audio Asset ID | ❌ 视觉设计细节 |
| `00_Design_Spec_Alice.md` | 音频参数、技术规格 | - | ❌ 课程结构、视觉设计 |
| `asset_manifest.json` | 音频资产索引 | - | ❌ 任何其他内容 |

## 3. 引用规范

### 3.1 Slide 引用格式 (在 Structure Map 和 Scripts 中)
```markdown
✅ 正确: `[SLIDE: S05_Visual_Matrix]`
✅ 正确: `[SLIDE: S08c_Pierre_Schaeffer]` (Schaeffer 操作唱机历史照片)

❌ 错误: `[SLIDE: S05_Visual_Matrix]` **[Visual]**: 极简主义数据艺术...
```

### 3.2 音频资产引用格式 (在 Scripts 中)
```markdown
✅ 正确: > **Asset**: `asset_S02_dirty_heartbeat.wav`
✅ 正确: 加载 `asset_S04_void_ir.wav`

❌ 错误: 加载 `_Library/S04_Space/contrast_IR_small_closet.wav` (硬编码路径)
```

## 4. 禁止行为

1. ❌ **视觉描述越界**: 在 Structure Map 中写 `**[Visual]**: ...` 后跟详细描述
2. ❌ **重复定义**: 在 Slide Database 中定义同一个 Slide ID 两次
3. ❌ **路径硬编码**: 在 Script 中写完整的 `_Library/...` 路径

## 5. 验证方法

运行以下脚本检查合规性:
```bash
python .agent/skills/validation-suite/scripts/validate_links.py
```

---
**变更记录**:
- 2026-01-29: 初始版本,基于架构重整计划 (ADR-007)
