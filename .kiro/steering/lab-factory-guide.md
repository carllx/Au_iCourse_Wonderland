# Lab Factory - Adobe Audition Automation Guide

> **来源**: `.agent/skills/lab-factory/` 
> **类型**: JSX 自动化工具包

## 快速开始

Lab Factory 提供 Adobe Audition 自动化工具包，包含：
- **Audition.jsx**: 核心 API 库
- **Universal_Lab_Builder.jsx**: 场景构建器
- **8个 JSX 脚本**: 位于 `.agent/skills/lab-factory/lib/` 和 `scripts/`

## 核心 API (Audition.jsx)

### 命名空间

1. **Audition.IO** - 文件导入
   - `importFile(path)`: 智能导入（支持 Audition 2024+）
   
2. **Audition.Session** - 会话管理
   - `findFirst()`: 查找首个多轨会话
   - `openTemplate(path)`: 打开模板

3. **Audition.Track** - 轨道操作
   - `getOrCreate(session, index)`: 获取或创建轨道
   - `setControls(track, mute, solo)`: 设置轨道状态

4. **Audition.Clip** - 片段操作
   - `addToTrack(track, doc, time)`: 添加片段到时间轴
   - `setColor(clip, colorObj)`: 设置颜色

5. **Audition.Markers** - 标记管理
   - `addCycle(session, name, start, duration)`: 添加循环标记

6. **Audition.State** - 状态管理
   - `getOpenDocuments()`: 获取打开的文档列表
   - `closeAll(force)`: 强制清理工作区

7. **Audition.Log** - 日志输出
   - `sentinel(msg)`: 静默日志（配合 fast_run.sh 使用）

## 使用方式

### 方法 1: 使用 Universal Lab Builder

```javascript
#include "../../../../../.agent/skills/lab-factory/lib/Universal_Lab_Builder.jsx"

var manifest = {
    session: "path/to/template.sesx",
    assets: [
        {path: "assets/audio.wav", track: 1, time: "0:00"}
    ]
};

UniversalLabBuilder.build(manifest);
```

### 方法 2: 直接使用 Audition.jsx API

```javascript
#include "../../../../../.agent/skills/lab-factory/lib/Audition.jsx"

// 导入文件
var doc = Audition.IO.importFile("path/to/audio.wav");

// 获取会话
var session = Audition.Session.findFirst();

// 创建轨道
var track = Audition.Track.getOrCreate(session, 1);

// 添加片段
Audition.Clip.addToTrack(track, doc, "0:00");
```

## 鲁棒性协议 (Traffic Light)

| 状态 | 行为 |
|------|------|
| 🟢 200 | 全自动成功 |
| 🟡 4xx | 生成 MANUAL_GUIDE.md 提示手动操作 |
| 🔴 5xx | 安全退出并记录日志 |

## 快速调试

使用 `fast_run.sh` 避免弹窗和等待：

```bash
./fast_run.sh your_script.jsx
```

在脚本中使用：
```javascript
Audition.Log.sentinel({status: "success", data: result});
```

## 已知限制

❌ **不支持**:
- 视图控制（缩放、滚动）
- 工具交互（鼠标工具切换）
- 交互式效果器（需要用户输入的效果）

## 脚本位置

- **核心库**: `.agent/skills/lab-factory/lib/`
  - Audition.jsx
  - Universal_Lab_Builder.jsx
  - env_context.jsx
  - time_utils.jsx
  - create_template.jsx

- **测试脚本**: `.agent/skills/lab-factory/scripts/`
  - test_toolkit.jsx
  - test_toolkit_logged.jsx
  - probe_api_methods.jsx

## 相关文档

- 完整文档: `.kiro/powers/lab-factory-power/POWER.md`
- MVP 规范: `.agent/rules/rule_mvp_conventions.md`
- 技能地图: `.agent/knowledge/Audition_Skills_Map.md`
