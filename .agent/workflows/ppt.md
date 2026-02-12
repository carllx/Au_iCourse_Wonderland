---
description: 生成课程 PPT 演示文稿 (从脚本自动生成)
---

# /ppt Workflow (PPT 生成工作流)

> **输入**: 脚本文件名 (如 `S02_Phase1_Purify.md`)
> **输出**: `04_Delivery/ppt_output/[脚本名]_Presentation.pptx`

---

## 关键路径参考 (Key Paths)

在执行本 Workflow 时，确保引用以下路径：

| 资源 | 路径 |
|------|------|
| **pptx Skill 指南** | `.agent/skills/pptx/SKILL.md` |
| **PptxGenJS 教程** | `.agent/skills/pptx/pptxgenjs.md` |
| **PPT 生成脚本** | `04_Delivery/ppt_generator/generate_pptx.js` |
| **PPT 规范验证器** | `.agent/skills/validation-suite/scripts/validate_ppt_spec.py` |
| **链接验证器** | `.agent/skills/validation-suite/scripts/validate_links.py` |
| **Slide 数据库** | `02_Visuals/Slide_Database.md` |
| **视觉资产目录** | `02_Visuals/assets/` |
| **PPT 输出目录** | `04_Delivery/ppt_output/` |
| **LibreOffice 转换脚本** | `.agent/skills/pptx/scripts/office/soffice.py` |

---

## 执行步骤 (Execution Steps)

### Step 1: 预检 (Pre-flight Checks)

在生成 PPT 之前，先验证脚本引用的 Slide ID 是否都已在数据库中定义：

// turbo
```bash
python3 .agent/skills/validation-suite/scripts/validate_ppt_spec.py 03_Scripts/[脚本名].md
```

**检查项**:
- ✅ 所有 `[SLIDE: ID]` 引用都在 `Slide_Database.md` 中有定义
- ✅ 必要的字段 (Type, Text, Caption) 已填写
- ⚠️ 如有缺失，先运行 `/audit` 修复

---

### Step 2: 资产检查 (Asset Verification)

确认视觉资产已就绪：

// turbo
```bash
ls -la 02_Visuals/assets/[模块前缀]_*/
```

**预期结果**:
- 每个 `[SLIDE: Sxx_ID]` 应对应一个 `Sxx_ID*.png/jpg` 资产文件
- **支持 MP4**: 视频文件 `Sxx_ID*.mp4` 也可以被识别并嵌入 (Slide 会自动使用 Video 组件)

---

### Step 3: 生成 PPT (Generate)

运行核心生成脚本：

// turbo
```bash
cd 04_Delivery/ppt_generator && node generate_pptx.js [脚本名].md
```

**输出**:
- 生成 `04_Delivery/ppt_output/[脚本名]_Presentation.pptx`
- Console 会显示每张图片的尺寸调整信息

---

### Step 4: 质量检查 (QA - Required)

根据 pptx Skill 的要求，**必须进行视觉 QA**。

#### 4.1 转换为 PDF

// turbo
```bash
mkdir -p /tmp/ppt_qa
python3 .agent/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf 04_Delivery/ppt_output/[脚本名]_Presentation.pptx --outdir /tmp/ppt_qa
```

#### 4.2 提取幻灯片图片

// turbo
```bash
pdftoppm -jpeg -r 150 /tmp/ppt_qa/[脚本名]_Presentation.pdf /tmp/ppt_qa/slide
```

#### 4.3 视觉检查

使用 `view_file` 查看 `/tmp/ppt_qa/slide-*.jpg` 图片，检查：
- [ ] 文本是否被截断或溢出
- [ ] 图片是否正确显示（无拉伸）
- [ ] 缺失资产是否显示 "MISSING ASSET" 警告
- [ ] 布局是否符合预期 (左文右图)

---

## 布局类型说明 (Layout Types)

生成脚本会根据 `Type` 或 `Layout` 字段自动选择布局：

| Type/Layout 关键词 | 布局效果 |
|-------------------|---------|
| `title` | **标题卡** - 全屏背景 + 居中大标题 |
| `cinematic`, `caption` | **电影字幕** - 图片 + 底部字幕条 |
| *(默认)* | **左右分布** - 左 40% 文字，右 60% 图片 |

---

## 故障排除 (Troubleshooting)

### 问题: "MISSING ASSET" 警告
**原因**: 脚本引用的 Slide ID 在资产目录中找不到对应文件
**解决**: 
1. 检查文件名是否以 `Sxx_` 为前缀
2. 确认文件放在正确的模块子目录内 (`02_Visuals/assets/[模块]_*/`)

### 问题: 视频无法播放
**原因**: 本地视频嵌入依赖于 PPT 播放环境对格式的支持
**解决**: 
1. 确保视频是标准 H.264 MP4
2. PPTXGenJS 使用相对/绝对路径嵌入，确保 PPT 文件移动时视频文件一同移动 (或使用 Embed 模式，默认已尝试 Embed)
3. 视频默认按 16:9 比例居中放置 (Contain 模式)

### 问题: 中文乱码
**解决**: 确保脚本文件使用 UTF-8 编码

---

## 进阶用法

### 批量生成所有章节

```bash
for script in 03_Scripts/S*.md; do
  node 04_Delivery/ppt_generator/generate_pptx.js "$(basename $script)"
done
```

### 自定义配色

修改 `04_Delivery/ppt_generator/generate_pptx.js` 中的 `CONFIG.theme`:
```javascript
theme: {
    bgColor: '000000',      // 背景色 (纯黑)
    textColor: 'FFFFFF',    // 正文颜色 (白)
    accentColor: '00FFFF',  // 强调色 (青)
    warningColor: 'FF3333', // 警告色 (红)
    mutedColor: '888888',   // 次要色 (灰)
}
```

---

**变更日志**:
- 2026-02-09: 初始版本，整合 pptx skill + generate_pptx.js + validate_ppt_spec.py
