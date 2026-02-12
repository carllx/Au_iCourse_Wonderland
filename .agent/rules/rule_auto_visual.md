---
trigger: always_on
description: 控制 Agent 何时可以自动生成视觉资产，以及何时需要用户确认。
---

# 规则：自动配图协议 (Auto-Visual Protocol)

**生效范围**: `/audit`, `/write` 工作流，以及任何涉及 `Slide_Database.md` 校验的任务。

## 1. 核心原则 (Philosophy)

Agent 可以主动为项目生成视觉资产，但必须在「可控」范围内，避免过度生产。

## 2. 触发条件 (Triggers)

### A. 审计修复模式 (Audit Repair)
**场景**: 执行 `/audit` 时，`validate_links.py` 检测到 **Orphan References** (脚本引用了数据库中不存在的 Slide ID)。

| 条件 | 行为 |
|:---|:---|
| 缺失 ≤ **3** 个且类型可生成 | ✅ Agent **可直接修复**：补全 `Slide_Database.md` 定义 + 调用 `gen_visual_asset.py` |
| 缺失 > **3** 个 | ⚠️ Agent **必须先用 `notify_user` 请求用户确认**，再执行批量生成 |

### B. 写作模式 (Writer Mode)
**场景**: 执行 `/write` 时，脚本中新增了 `[SLIDE: SXX_NewID]` 引用。

*   **强制行为**: 在 `Slide_Database.md` 中创建该 ID 的 **最小化 Stub (骨架)**：
    ```markdown
    ## SXX_NewID
    *   **Type**: [Concept Art] <!-- 根据上下文推断 -->
    *   **Concept**: [关键词]
    *   **Visual**: [从脚本上下文提炼的简述]
    ```
*   **禁止行为**: 在 Writer 模式下调用 `gen_visual_asset.py`。仅定义，不生产（留给 Greybox 或后续审计生成）。

## 3. 黑名单 (Blacklist)

以下类型的 Slide **永远不可**通过 AI 自动生成，必须由人类手动采集：

| Type | 原因 |
|:---|:---|
| `[UI/Screenshot]` | 需要真实的软件截图 |
| `[Live Demo]` | 需要屏幕录制 |
| `[Photo/Historical]` | 需要网络搜索或版权素材 |
| `[Photo/Band]` | 需要网络搜索或版权素材 |

## 4. 工具链 (Tooling)

*   **生成脚本**: `.agent/skills/visual-director/scripts/gen_visual_asset.py`
*   **校验脚本**: `.agent/skills/validation-suite/scripts/validate_links.py`

---

**变更记录**:
*   2026-02-07: 初始版本 (Based on S04 Audit Findings)。
