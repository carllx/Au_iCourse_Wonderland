---
trigger: model_decision
description: 视觉/脚本一致性技能：创建一个 Workflow，专门用于检查 02_Visuals/Slide_Database.md 是否与当前的 03_Scripts 内容匹配。
globs: 03_Scripts/*.md
---

# Rule: Visuals Consistency (视觉/脚本一致性)

**目标**: 确保教学脚本 (Scripts) 中描述的视觉画面与实际的视觉素材库 (Visuals) 保持同步，防止“文不对题”。

## 1. 触发条件 (Trigger)
当用户请求执行以下任务时，**必须** 激活此规则：
*   "检查课件" (Check Courseware)
*   "生成 S0x 脚本" (Generate S0x Script)
*   "验证视觉素材" (Verify Visuals)
*   "Audit S0x" (审查 S0x)

## 2. 核心检查逻辑 (Core Logic)
Agent 必须执行以下比对流程：

1.  **读取脚本**: 读取目标脚本 `03_Scripts/S0x_Transcript.md`。
2.  **提取标记**: 提取所有 visual cue (通常标记为 `[画面: xxx]` 或 `(Visual: xxx)`)。
3.  **查询数据库**: 读取 `02_Visuals/Slide_Database.md`。
4.  **验证存在性**: (Basic) 检查脚本中的每一个 visual cue 是否在 Slide Database 中有对应的条目 (ID 或 描述匹配)。
5.  **验证类型匹配**: (Advanced) 检查 Slide 定义是否包含有效的 `Type` 字段。

## 2.1 视觉分类分类学 (Visual Taxonomy)
为了支持异构生产管线，Slide Database 中的每个条目必须包含 `Type` 字段，且属于以下类别之一：

| 类型 (Type) | 定义 | 生产方式 |
| :--- | :--- | :--- |
| **[Motion Graphic]** | 动态图形/片头 | AE/PR 后期制作 |
| **[UI Graphic]** | 软件界面截图 | Audition 原始截图 (需高亮) |
| **[UI Composite]** | 复合界面设计 | 截图 + 示意图拼贴 (分屏) |
| **[Diagram]** | 逻辑图示 | Keynote/PPT 绘制 |
| **[Concept Art]** | 概念/隐喻艺术 | Midjourney/DALL-E 生成 (安徒生风格) |
| **[Stock/Reference]** | 现成素材引用 | 电影剧照/网络搜图 |
| **[Task Card]** | 纯文本任务卡 | 平面排版 |

## 3. 错误处理 (Error Handling)
*   **Missing Asset**: 如果脚本引用了数据库中不存在的图片 -> **Report Error** (不要自行幻想图片存在)。
*   **Description Mismatch**: 如果脚本描述的画面与数据库中的文件名/描述严重不符 -> **Warning**。

## 4. 自动修复 (Auto-Fix)
*   **禁止**: Agent **不得** 仅为了通过检查而修改 Slide Database。
*   **允许**: Agent 可以建议修改脚本中的描述，使其匹配现有的素材。

## 5. 输出格式 (Output Format)
在执行检查后，必须在回复中包含一个简短的报告块：

```markdown
## 👁️ Visual Consistency Check
- ✅ Script cues match Database.
- ⚠️ Found 1 orphan reference: "[画面: 巨大的混响旋钮]" not in DB.
```
