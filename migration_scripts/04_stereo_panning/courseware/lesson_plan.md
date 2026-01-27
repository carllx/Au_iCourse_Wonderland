# 课程教案 04：具象化心理声像 (Visceral Panning)

> **教师笔记 (Teacher Notes)**:
> 本节课不再使用传统的"乐队排练"案例，而是升级为**"心理惊悚"**这一更高级的电影音效案例。
> 教学核心在于**"双重方案 (Dual Scheme)"**：让学生理解声音不仅是"听"出来的，更是"算"出来的 (Python) 和"摆"出来的 (Audition)。

---

## 1. 教学目标 (Objectives)

1.  **概念**: 理解 **Stereo Panning** 如何构建心理空间 (Internal vs External)。
2.  **技能**: 掌握 Audition 的 Pan Pot 操作与自动化。
3.  **思维**: 建立 **"编程生成 (Generative)"** 与 **"后期混音 (Mixing)"** 的全栈音频思维。

---

## 2. 教学双重奏 (The Dual Pedagogy)

本实验采用两种互补的方案来实现同一个目标：**"身处险境的自我"**。

| 维度 | **Python 方案 (The Source)** | **Audition 方案 (The Mix)** |
| :--- | :--- | :--- |
| **角色** | **造物主 (Creator)** | **导演 (Director)** |
| **任务** | 从无到有生成声音的**物理质感**。 | 将素材摆放在**空间位置**上。 |
| **核心算法** | 物理建模 (Physical Modeling)。<br>例如：`generate_heart_transient()` 模拟瓣膜闭合。 | 声像电位器 (Pan Pot)。<br>例如：`Left 100` 将能量集中于左声道。 |
| **听感控制** | 频率 (Frequency) 与包络 (Envelope)。<br>例如：低通滤波制造"体内感"。 | 宽度 (Width) 与分离度 (Separation)。<br>例如：拉开两侧以突出中间。 |

---

## 3. 实验内容 (Lab Content)

### 3.1 Python 环节：解构声音 DNA
在进入 Audition 之前，先向学生展示 `../scripts/py_generation/generate_panning_assets.py` 的核心逻辑：
*   **心跳的秘密**: 我们没有录制真实心跳，而是用代码写了一个公式：
    *   `S1 (Lub) = Sine Sweep (Low) + Filtered Noise`
    *   这教会学生：**真实感来自于对物理机制的模拟**。
*   **焦虑的数学**: 右声道的尖锐噪音并非随机，而是使用了 `surge ** 8` (8次幂) 的包络曲线，模拟神经痛的突发与消退。

### 3.2 Audition 环节：构建心理空间
引导学生打开 `.jsx` 生成的工程，进行手动混音：
1.  **确立本我 (Center)**: 独奏 `Heartbeat` 和 `Opponent`。注意它们在只有 Center 时是冲突的。
2.  **建立围墙 (Left)**: 将 `The Wall` 拧到极左。感受心跳声低频的浮现。
3.  **神经穿刺 (Right)**: 将 `The Needle` 拧到极右。感受头皮发麻的包围感。

---

## 4. 课后思考 (Assignment)

**"如果是单声道 (Mono) 会怎样？"**
请学生将 Master 总线的 Stereo Mode 切换为 Mono。
*   **预期结果**: 惊悚感瞬间消失。Environment (Wall/Needle) 会掩盖掉 Heartbeat 的细节，Opponent 的清晰度也会下降。
*   **结论**: 立体声 (Stereo) 不这也是这一课的终极奥义：**空间即清晰度 (Space is Clarity)**。
