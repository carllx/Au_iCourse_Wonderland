# 规则：元学习协议 (Meta-Learning Protocol)

**定义**: 当你（Agent）在执行任务过程中获得了“新知识”或做出了“新决定”，你必须**主动**将其固化到 `.agent/` 目录中。这被称为 **Memory Commit**。

## 1. 触发条件 (Triggers)

| 场景事件 | 对应行动 (Action) | 目标文件 (Target) |
| :--- | :--- | :--- |
| **架构决策** (选中了某个库，废弃了某种写法) | Record Decision | `.agent/memory/ADR.md` |
| **Bug 修复** (发现某个脚本总是报错) | Update Guide | `03_MVP_Demo/Asset_Production_Guide.md` (Failed Cases) |
| **知识发现** (发现了一个新的 Audition 技巧) | Map Knowledge | `.agent/knowledge/Audition_Skills_Map.md` |
| **风格反馈** (用户说“这不像林昕老师”) | Update Style | `.agent/styles/LinXin_Voice.md` |
| **规则漏洞** (用户指出了你没遵守的潜规则) | Patch Rules | `.agent/rules/*.md` |

## 2. 执行步骤 (Commit Process)

你不必等待用户指令。当你意识到由于**缺乏文档**导致你刚才犯错或犹豫时，请立即执行：

1.  **Stop**: 完成当前手头任务。
2.  **Reflect**: "如果我下次还要做这个，我希望哪里有一份说明书？"
3.  **Update**: 
    *   读取目标文档 (`view_file`).
    *   追加或修改内容 (`replace_file_content`).
4.  **Notify**: 告诉用户："顺便说一句，为了防止下次再犯，我已经把这个坑记录在 `xxx.md` 里了。"

## 3. 禁忌 (Anti-Patterns)

*   **DON'T**: 只在 Chat 中道歉 ("对不起我下次注意")。Agent 没有长时记忆，Chat 关闭后你就忘了。**文档是唯一的记忆。**
*   **DON'T**: 创建过于琐碎的规则 ("在第5行必须加空格")。只记录原则性、架构性的知识。

## 4. 规则文件标准 (Rule Standards)

所有新建的 Rule 文件 (`.agent/rules/*.md`) 必须包含符合 Antigravity 标准的 Frontmatter：

```yaml
---
trigger: [glob | user | always_on]
description: A short summary of what this rule does.
globs: [path/to/files/*.ext] # Only required if trigger is glob
---
```

**Correct Example**:
```yaml
---
trigger: glob
description: Enforces syntax for script files.
globs: 01_Scripts/*.md
---
```
