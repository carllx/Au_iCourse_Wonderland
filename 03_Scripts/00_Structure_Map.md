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
| **3-4'** | **Toolbox Flash** | **武器库展示**：Audition 的那一排武器。多普勒、吉他包、中置提取... | `[SLIDE: S02b_Toolbox_Flash]` (图标网格) | N/A |
| **4-5'** | Mission Brief | 引入 "Alice Project"。Audition 不止是扫帚（清理工具），更是画笔（创作工具）。提出核心问题：**“听众在哪里？”** | `[SLIDE: S03_Concept_Source_Space_Ear]` (核心图) | N/A |

---

## 模块二：净化 (S02_Phase1_Purify)
*   **Time**: 05:00 - 20:00
*   **Theme**: 驱逐现实的尘埃
*   **Tech**: 6.6 降噪 (Noise Reduction Process)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **05-08'** | Theory (N) | 采样降噪原理：抓通缉犯(Sample) -> 全城搜捕(Process)。解释“信噪比”与**1/f 心跳宇宙 (Voss & Clarke, 1975)**。 | `[SLIDE: S02_Voss_Clarke]` | `[Spec > Phase 1 > Intro]` |
| **08-11'** | **Guided Listening** | **深听时刻 (30s)**：闭眼感受“真空的压迫感”。引入 **John Cage (1951) 哈佛消声室** 故事：每个人都有自己的本底噪音。 | `[SLIDE: S04_Alvin_Lucier]` | `[Spec > Phase 1 > Check]` |
| **11-14'** | **Director's Choice** | **决策时刻**：我们要“死寂的真空”还是“真实的房间”？解释 **Musical Noise (Steven Boll, 1979)** 的诅咒。 | `[SLIDE: S02_Ghost_Math]` | N/A |
| **14-20'** | Demonstration | 执行降噪。**关键组合拳**：<br>1. **Reduction**: 75% (比例)<br>2. **Reduce by**: 20-30dB (深度)<br>**技术注释**：解释 FFT 4096 背后的 **Gabor (1946) 测不准原理**。 | `[SLIDE: S02_Demonstration]` | `[Spec > Phase 1 > ACT_01/02]` |
| **20-21'** | **Result (Closure)** | **审视尸体**：降噪完成后的声音虽然干净，但失去了厚度。 | `[SLIDE: S02_Ugly_Duckling]` (声音的尸体) | N/A |

---

## 模块三：塑形 (S03_Phase2_Sculpt)
*   **Time**: 20:00 - 40:00
*   **Theme**: 身份的重量与脆弱
*   **Tech**: 6.10 伸缩与变调 (Stretch and Pitch)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **18-20'** | **Theory (History)** | **引入声音对象 (Sound Object)**：Pierre Schaeffer 的发现。声音可以脱离物体存在。 | `[SLIDE: S03_Pierre_Schaeffer]` (Schaeffer 操作唱机历史照片) | N/A |
| **20-21'** | **Theory (Physics)** | **克洛诺斯的诅咒**：在数字时代之前，时间与音高是绑定的。加速=变高，减速=变低。 | `[SLIDE: S03_Tape_Machine]` (疯转的磁带机动画) | N/A |
| **21-23'** | **Director's Choice** | **决策时刻**：是做“惊慌的小孩”(急促) 还是 “优雅的灵魂”(沉稳)？<br>*决定：赋予成熟与优雅。* | `[SLIDE: S03_Visual_Alice_Drink]` (爱丽丝喝药水变身静帧) | N/A |
| **23-24'** | **Warning** | **花栗鼠陷阱**：如果直接变调，会发生 Formant Shift（共振峰偏移），变成卡通人物。 | `[SLIDE: S03_Chipmunk]` (花栗鼠警告) | N/A |
| **24-25'** | **Theory (Deep)** | **共振峰 (Formant)**：声带（弦）变了，但琴体（身体）不能变。 | `[SLIDE: S03_Cello_Body]` (声带与琴体对比图) | N/A |
| **25-30'** | **Guided Listening** | **深听时刻 (30s)**：闭眼辨别 **-4 semitones** 时 Body 与 Pitch 的分离感。 | `[SLIDE: S03_Deep_Listening]` (Body vs Soul) | N/A |
| **30-40'** | Demonstration | 1. **Stretch**: 135% (成熟)。<br>2. **Pitch**: -4 semitones (优雅)。<br>3. **Key**: 勾选 Preserve Speech Characteristics。 | `[SLIDE: S03_Visual_Alice_Drink]` | `[Spec > Phase 2 > ACT_04]` |

---

## 模块四：置景 (S04_Phase3_Space)
*   **Time**: 40:00 - 65:00
*   **Theme**: 时间的遗物 (深渊)
*   **Tech**: 6.7 卷积混响 (Convolution Reverb)
%%希望引入用气球 DIY 制作 Impulse Responses 的方法%%
| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **40-42'** | Theory (B) | 混响不是回声。它是空间的指纹。卷积混响 = 空间的“克隆技术”。 | `[SLIDE: S04_Visual_RabbitHole]` (脉冲响应示意) | N/A |
| **42-45'** | **Theory (Physics)** | **脉冲响应 (IR) 原理**：如何在山洞里戳破气球，抓到空间的 DNA。 | `[SLIDE: S04_Balloon_Cave]` (气球爆炸图示) | N/A |
| **45-50'** | **Guided Listening** | **深听时刻 (30s)**：试错对比。**Closet (太窄) vs Hall (太假)**。我们寻找的是 "Void" (虚无)。<br>**Dry vs Wet**: 贴脸 vs 深渊。 | `[SLIDE: S04_Tail_Timer]` (不同空间脉冲对比) <br> `[SLIDE: S04_Concept_Dry_Wet]` (干湿对比) | `[Spec > Phase 3 > ACT_05a]` |
| **50-52'** | **Theory (Adv)** | **高频阻尼 (Damping)**：为什么深海听不到高频？ | `[SLIDE: S04_Damping_Curve]` (潜水员与红光消失) | N/A |
| **52-65'** | Demonstration | 加载 `asset_S04_void_ir.wav`。参数物理学：<br>1. **Size 150%** (拉长遗言)<br>2. **Mix 75%** (肉体消融)<br>3. **Pre-Delay 80ms** (灵魂出窍)。<br>4. **Automation**: `[SLIDE: S04_Automation_Dissolution]` | `[SLIDE: S04_Visual_RabbitHole]` | `[Spec > Phase 3 > ACT_05b]` |

---

## 模块五：定位 (S05_Phase4_Position)
*   **Time**: 65:00 - 75:00
*   **Theme**: 动态的几何学 (Dynamic Geometry)
*   **Tech**: 6.9 自动化 (Automation) & 360° 声像
*   **Note**: 本节超越传统的 L/R，引入 Time (时间) 维度。

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Design Spec) |
| :--- | :--- | :--- | :--- | :--- |
| **65-68'** | Theory (History) | **引入 Fantasound (1940)**：从 Blumlein 的脚步到迪士尼的“蝌蚪”控制轨。自动化不仅是技术，是声音的生命线。 | `[SLIDE: S05_Blumlein_Walking]` <br> `[SLIDE: S05_Fantasound_Layout]` | N/A |
| **68-69'** | Practice (Setup) | **建立力场 (Force Field)**: 5.1 环绕声设置。Routing Check.Bus "The Void" (Omnibus). | `[SLIDE: S05_Setup_Surround_NewSession]` <br> `[SLIDE: S05_Setup_Bus_Creation]` | N/A |
| **69-72'** | Practice (The Wall) | **压迫之墙 (ILD)**: 低频绕射 vs 高频遮蔽。画出 Low Pass Filter 曲线，像一扇缓慢关闭的门。 | `[SLIDE: S05_Wall_EQ_Start]` <br> `[SLIDE: S05_Wall_EQ_End]` | `[ACTION: S05_Act_Draw_Filter]` |
| **72-74'** | Practice (The Needle) | **焦虑之刺 (Doppler)**: 声音的螺旋。Confusing the brain. 只有动起来的声音才是可怕的。 | `[SLIDE: S05_Needle_Automation_Setup_cap]` <br> `[SLIDE: S05_Needle_Pan_Random_cap]` | `[ACTION: S05_Act_Perform_Pan]` |


---

## 模块六：总结 (S06_Summary)
| **Time**: 75:00 - 80:00
*   **Theme**: 剧场谢幕
*   **Visual**: `[SLIDE: S06_Summary_Loop]` (净化-塑形-置景-定位 闭环图)

| Timeline | Topic | Key Content | Visual Ref | Action Ref |
| :--- | :--- | :--- | :--- | :--- |
| **75-78'** | Summary | 回顾四步法。引用 **Walter Murch**。 | `[SLIDE: S06_Summary_Loop]` <br> `[SLIDE: S06_Murch_Rule_of_Six]` | N/A |
| **78-80'** | Homework | **逃离麦克风**：录制干声并异化。 | `[SLIDE: S06_Homework]` | N/A |
