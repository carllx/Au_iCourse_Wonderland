# 00_Structure_Map (课程结构映射表)

> **Document Type**: Source Code (Skeleton)
> **Compiler Target**: 03_Scripts/S0x_Transcript.md
> **Pedagogy**: Visual Essay / Direct Demonstration
> **Total Duration**: 80 Minutes (Allocated)

> **Legend**:
> *   **Role**: A=Artist, L=Lead, D=Director, Q=Question, U=User
> *   **Mode**: N=Narrative, B=Beat, C=Conflict, O=Opening, E=Ending

---

## 模块一：导入 (S01_Intro)
*   **Time**: 00:00 - 05:00
*   **Theme**: 无形(声音)空间秩序的导演的觉醒
*   **Goal**: 建立“技术服务于表达”的观念，修补知识盲区，引出 MVP 任务。

| Timeline | Topic | Key Content/Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **0-1'** | Opening | 我是林昕。承接陈老师(A/L/D/Q/U)。引入本课(N/B/C/O/E)。 | `[SLIDE: S01_Title]` (声音魔术师) | N/A |
| **1-3'** | Bad Case Crash | **【知识修补】** 快速展示"脏音频"。指认：这是电流(Hum)，这是爆音(Click)，这是底噪(Hiss)。今天只杀最大的敌人：底噪。 | `[SLIDE: S02_BadCase]` (波形图上的脏点标记) | `[Spec > Intro > Play Bad]` |
| **3-5'** | Mission Brief | 引入 "Alice Project"。Audition 不止是扫帚（清理工具），更是画笔（创作工具）。提出核心问题：**“听众在哪里？”** | `[SLIDE: S03_Concept_Source_Space_Ear]` (声源-空间-耳朵 核心图) | N/A |

---

## 模块二：净化 (S02_Phase1_Purify)
*   **Time**: 05:00 - 20:00
*   **Theme**: 驱逐现实的尘埃
*   **Tech**: 6.6 降噪 (Noise Reduction Process)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **05-08'** | Theory (N) | 采样降噪原理：抓通缉犯(Sample) -> 全城搜捕(Process)。解释“信噪比”与**1/f 心跳宇宙 (Voss & Clarke, 1975)**。 | `[SLIDE: S05_Visual_Matrix]` **[Visual]**: 极简主义数据艺术。左侧是混乱的粉红噪音粒子（像沙尘暴），右侧是清晰的心跳波形（像发光山脉）。背景是宇宙深空的深蓝色。 | `[Spec > Phase 1 > Intro]` |
| **08-11'** | **Guided Listening** | **深听时刻 (30s)**：闭眼感受“真空的压迫感”。引入 **John Cage (1951) 哈佛消声室** 故事：每个人都有自己的本底噪音。 | `[SLIDE: S05b_Spectrum]` **[Visual]**: 动态频谱图。但不是冷冰冰的线，而是像极光的流动。中央有一个巨大的倒计时数字。Tagline: "The Pulse of Silence". | `[Spec > Phase 1 > Check]` |
| **11-14'** | **Director's Choice** | **决策时刻**：我们要“死寂的真空”还是“真实的房间”？解释 **Musical Noise (Steven Boll, 1979)** 的诅咒。 | `[SLIDE: S06_Ghost_Math]` **[Visual]**: 一个半透明的、充满噪点的幽灵鸟（Birdies/Artifacts）漂浮在纯黑的背景中。隐喻：过度降噪产生的“数字幽灵”。 | N/A |
| **14-20'** | Demonstration | 执行降噪。**关键组合拳**：<br>1. **Reduction**: 75% (比例)<br>2. **Reduce by**: 20-30dB (深度)<br>**技术注释**：解释 FFT 4096 背后的 **Gabor (1946) 测不准原理**。 | `[SLIDE: S07_Demonstration]` **[Visual]**: 分屏设计。左边是 Audition 面板参数截图（高亮 75% + 30dB），右边是 Dennis Gabor 的手绘信息单元图（Information Diagram）。 | `[Spec > Phase 1 > ACT_01/02]` |

---

## 模块三：塑形 (S03_Phase2_Sculpt)
*   **Time**: 20:00 - 40:00
*   **Theme**: 身份的重量与脆弱
*   **Tech**: 6.10 伸缩与变调 (Stretch and Pitch)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **20-25'** | **Director's Choice** | **决策时刻**：是做“惊慌的小孩”(急促) 还是 “优雅的灵魂”(沉稳)？<br>*决定：赋予成熟与优雅。* | `[SLIDE: S08_Visual_Alice_Drink]` (爱丽丝喝药水变身静帧) | N/A |
| **25-30'** | **Guided Listening** | **深听时刻 (30s)**：闭眼辨别 **-2 semitones (粗)** 与 **-4 semitones (优雅)** 的质感区别。以及 **135% Stretch** 的舒缓感。 | `[SLIDE: S08_Visual_Alice_Drink]` | N/A |
| **30-40'** | Demonstration | 1. **Stretch**: 135% (成熟)。<br>2. **Pitch**: -4 semitones (优雅)。<br>3. **Key**: 勾选 Preserve Speech Characteristics。 | `[SLIDE: S08_Visual_Alice_Drink]` | `[Spec > Phase 2 > ACT_04]` |

---

## 模块四：置景 (S04_Phase3_Space)
*   **Time**: 40:00 - 65:00
*   **Theme**: 时间的遗物 (深渊)
*   **Tech**: 6.7 卷积混响 (Convolution Reverb)
%%希望引入用气球 DIY 制作 Impulse Responses 的方法%%
| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **40-45'** | Theory (B) | 混响不是回声。它是空间的指纹。卷积混响 = 空间的“克隆技术”。 | `[SLIDE: S11_Visual_RabbitHole]` (脉冲响应示意) | N/A |
| **45-50'** | **Guided Listening** | **深听时刻 (30s)**：试错对比。**Closet (太窄) vs Hall (太假)**。我们寻找的是 "Void" (虚无)。 | `[SLIDE: S11b_Tail_Timer]` (不同空间脉冲对比) | `[Spec > Phase 3 > ACT_05a]` |
| **50-65'** | Demonstration | 加载 `asset_S04_void_ir.wav`。参数物理学：<br>1. **Size 150%** (拉长遗言)<br>2. **Mix 75%** (肉体消融)<br>3. **Pre-Delay 80ms** (灵魂出窍)。 | `[SLIDE: S11_Visual_RabbitHole]` | `[Spec > Phase 3 > ACT_05b]` |

---

## 模块五：定位 (S05_Phase4_Position)
*   **Time**: 65:00 - 75:00
*   **Theme**: 动态的几何学 (Dynamic Geometry)
*   **Tech**: 6.9 自动化 (Automation) & 360° 声像
*   **Note**: 本节超越传统的 L/R，引入 Time (时间) 维度。

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **65-68'** | Theory (O) | 声音是有形状的。**Width** 是宽度，**Pan** 是轨迹。介绍 "Object-Based Audio" 概念：不是把声音放在左边，而是让声音**走**到左边。 | `[SLIDE: S14_Visual_Spiral]` (动态螺旋雷达图示意) | N/A |
| **68-70'** | **Guided Listening** | **深听时刻 (30s)**：戴耳机。闭眼感受两股力量：<br>1. **The Wall**: 从正前方压过来的低频墙。<br>2. **The Needle**: 在头顶盘旋的高频刺。 | `[SLIDE: S14_Visual_Spiral]` | `[Spec > Phase 4 > Listening]` |
| **70-75'** | Demonstration | 执行 Automation。<br>1. **Needle**: 绘制 360° 螺旋线 (Doppler)。<br>2. **Wall**: 绘制 Low Pass Filter 打开曲线 (Approaching)。<br>**高潮时刻**: 当 Needle 刺入眉心时，Width 瞬间炸开至 150%。 | `[SLIDE: S14_Visual_Spiral]` | `[Spec > Phase 4 > ACT_07/08]` |

---

## 模块六：总结 (S06_Summary)
*   **Time**: 75:00 - 80:00
*   **Theme**: 剧场谢幕
*   **Visual**: `[SLIDE: S16_Summary_Loop]` (净化-塑形-置景-定位 闭环图)
