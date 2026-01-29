# S05_Phase4_Position (环节四：定位 - 动态的几何学)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 紧张、精密、物理压迫感
> **Context**: 65:00 - 75:00
> **Story**: 爱丽丝不仅迷失了方向，她还成为了猎物。

---

## 0. 声音的形状

**林昕**: 
“以前我们谈论声像 (Pan)，总是说‘左边’或者‘右边’。
但在电影工业里，声像不是一个点，它是一条**轨迹 (Trajectory)**。

请闭上眼睛。
想象一根针，它不是静止在你的右耳边。
它是从远处飞来，绕着你的头顶盘旋，越来越快，最后——
（拍手声）
扎进你的眉心。

这就是我们今天要做的：**动态声像 (Dynamic Panning)**。”

---

## 1. 猎场布局 (Setup)

**林昕**: 
“切换到 Multitrack 面板。
现在深渊里有了新的客人。
请把这五个轨道看作是一个**力场 (Force Field)**：

*   **Track 1 (Voice)**: 爱丽丝。**Center**。猎物。
*   **Track 2 (Heart)**: 那个生锈的钉子。**0% Width (Mono)**。死寂不动。
*   **Track 3 (Shadow)**: 镜中阴影。**Reverse Voice**。它是你内心的投射，也在 **Center**。

这三个都在中间。
那么，威胁在哪？

*   **Track 4 (The Wall)**: 导入 `asset_S05_threat_pressure.wav`。
    *   这是一堵低频的墙。
*   **Track 5 (The Needle)**: 导入 `asset_S05_threat_anxiety.wav`。
    *   这是一根高频的刺。”


---

## 1.5 意识 vs 潜意识 (Consciousness vs Shadow)

**林昕**:
“等等，只有 Shadow 吗？
如果深渊里只有反向的怪物，那就只是恐怖片。
爱丽丝之所以痛苦，是因为**她还清醒着**。

请增加第六感：
*   **Track 6 (Consciousness)**: 导入 `asset_S05_conscious_voice.wav`。
    *   **听感**: 极干 (Dry) + 温暖 (Warm)。
    *   **原理**: 当你听到自己的心声时，声音是通过**骨头**传导的（Bone Conduction）。它是世界上最亲密的声音。
    *   (Academic Ref: **Internal-Subjective Sound**, Michel Chion)

(Guided Listening: A/B Test)
*   **A (Shadow)**: 听，这是被扔进深渊的你（Reverse, Wet, Distorted）。那是你的恐惧。
*   **B (Consciousness)**: 听，这是还留在你脑海里的你（Dry, Bone EQ）。那是你的理智。

当这两个声音同时在 Center 响起时，
**理智的干声** 被 **恐惧的湿声** 包裹。
这才是真正的‘精神分裂’。”

---


## 2. 动态演示 (Automation)

**林昕**: 
“现在，不要只推推子。我们要画线。打开 **Automation Mode (自动化模式)**。

**第一步：The Wall (压迫之墙)**
*   **Geometry**: **Approaching Wedge (逼近的楔形)**。
*   不仅是音量变大，而是物理属性的改变。
*   **Filter Automation**: 绘制一条曲线，让 Low Pass Filter 的截止频率从 50Hz (Inaudible) 慢慢打开到 5000Hz (Harsh)。
*   **听感**: 声音从远处闷罐般的‘嗡嗡’声，变成了贴在脸上、颗粒毕现的‘轰鸣’。这一刻，墙不再是声音，它是**物体**。

**第二步：The Needle (焦虑之刺)**
*   **Geometry**: **Deep Spiral (深渊螺旋)**。
*   **Pan Automation**: 我们不画直线。我们要画**正弦波 (Sine Wave)**。
    *   左-右-左-右。
    *   并且频率越来越快 (Exponential)。
*   **Doppler Effect**: 配合微小的 Pitch Shift，模拟那种‘咻——咻——’的掠过感。
*   **听感**: 这只高频的苍蝇不仅在转，而且在**钻**。它正顺着你的耳膜钻进大脑皮层。

(Demonstration Action: 鼠标快速绘制包络线，屏幕上的雷达图随之疯狂旋转)

---

## 3. 高潮：几何坍塌

**林昕**: 
“现在，好戏上演。

当那堵墙 (Wall) 压到眼前，那根刺 (Needle) 转到极速的瞬间——
我们将全局混响的 **Width** 瞬间推到 **150%**。

**0% 的心脏** vs **150% 的荒野**。
**静态的濒死** vs **极速的围剿**。

(播放: `demo_S05_spiral_mix.wav`)

(Silence: 10s)

这就是深渊的真实形态。它不是空的，它是活的。它想吃掉你。”

---

## 4. 课程结语

**林昕**: 
“今天我们做的一切：净化、塑形、置景、定位。
不是为了炫技。

是为了让听众戴上耳机的那一刻，
不仅仅听到‘声音’，
而是被卷入那个又冷、又湿、充满了敌意与孤独的**几何体**中。

我是林昕。
我们在下一层梦境见。”
