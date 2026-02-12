---
description: 导出 TTS 逐字稿为 Word 文档（SLIDE 标记红色，朗读内容黑色）
---

# /export_docx - TTS 文本导出为 Word 文档

## 概述
将 `03_Scripts/tts/*.txt` 中的带标记文本导出为格式化的 Word 文档。

## 设计规范
| 元素 | 样式 |
|------|------|
| `[SLIDE #N: xxx]` 标记 | **红色** (#CC0000)、加粗、12pt |
| 朗读内容 | **黑色** (#000000)、常规、12pt |
| 字体 | Microsoft YaHei |
| 纸张 | A4 (11906 x 16838 DXA) |
| 边距 | 1 inch (1440 DXA) |

## 前置依赖
// turbo
1. 确保 txt 文件已生成（如未生成，先运行）：
```bash
python .agent/skills/validation-suite/scripts/validate_script_length.py --dump-text
```

## 执行步骤

// turbo
2. 导出全部章节：
```bash
node .agent/skills/validation-suite/scripts/export_tts_docx.js all
```

或导出单个章节：
```bash
node .agent/skills/validation-suite/scripts/export_tts_docx.js S02_Phase1_Purify.txt
```

## 输出位置
- **目录**: `03_Scripts/tts/docx_exports/`
- **文件**: `S01_Intro.docx`, `S02_Phase1_Purify.docx`, ...

## 相关文件
| 文件 | 用途 |
|------|------|
| `.agent/skills/validation-suite/scripts/validate_script_length.py` | 从脚本提取纯文本 + SLIDE 标记 |
| `.agent/skills/validation-suite/scripts/export_tts_docx.js` | 将 txt 转为带格式的 docx |
| `.agent/skills/docx/SKILL.md` | docx-js 库使用指南 |

## 常见问题

### Q: 没有安装 docx 依赖？
```bash
npm install docx --prefix .agent/skills/validation-suite
```

### Q: 想修改颜色？
编辑 `export_tts_docx.js` 中的常量：
```javascript
const COLOR_RED = 'CC0000';    // 标记颜色
const COLOR_BLACK = '000000';  // 朗读内容
```
