# Audition 自动化工具包使用指南 (Toolkit User Guide)

## 核心变更
我们已将原有的 "Lab Factory" 升级为原子化的 **Audition Automation Toolkit**。
针对 **Audition 2024** 的兼容性问题 (`Illegal Parameter Type` 错误)，工具包已切换至 **Safe-Fail (安全失败)** 模式。

---

## 🟢 正常工作流 (Audition 2024)

由于 Audition 2024 存在 API 限制，自动化脚本现在采用 **"辅助构建"** 模式，而不是 **"全自动"** 模式。

1.  **运行脚本**: 在 VS Code 中运行 `Setup_Restoration_Lab.jsx` (或使用 `/setup-lab` 指令)。
2.  **自动执行**:
    *   ✅ 创建/打开多轨会话 (Template)。
    *   ✅ 尝试创建轨道 (如失败则跳过)。
    *   ❌ **跳过自动导入**: 为防止崩溃或误开 Music App，工具包会自动跳过 wav 文件导入。
3.  **最终报告**:
    *   脚本运行结束后会弹出提示框：
        > "Lab Setup Complete with Issues: ... Manual Import Required ..."
    *   这表示环境已就绪，但素材需要您手动放入。

## ⚠️ 常见问题修复

### Q: 为什么脚本运行完没有素材？
**A:** 这是预期的 **Safe-Fail** 行为。
Audition 2024 的导入 API 目前不可用。脚本为您准备好了 Session，请直接将 `.agent/docs/course_materials/.../assets/` 下的文件拖入对应轨道即可。

### Q: 为什么之前会打开 Music App？
**A:** 之前的脚本尝试使用操作系统强行打开文件，被 macOS 默认关联到了 Music App。该功能已被 **禁用**。

### Q: 可以在脚本里修复这个问题吗？
**A:** 目前不可以。我们需要等待 Adobe 修复 Audition 2024 的 ExtendScript API Bug。当前的 "Safe-Fail" 模式是保证不崩溃、不卡死的唯一方案。

---

## 开发者指南 (编写新脚本)

如果您要编写新的自动化脚本，请遵循以下模式：

```javascript
#include "(path)/lib/Universal_Lab_Builder.jsx"

UniversalLabBuilder.build({
    sessionName: "My_New_Lab",
    templatePath: "(path)/docs/templates/Blank_48k.sesx",
    assets: [
        {
            name: "Voiceover",
            path: "/docs/.../voice.wav",
            trackIndex: 0,
            // 如果导入失败，Builder 会在报告中提示您手动处理此文件
        }
    ]
});
```
