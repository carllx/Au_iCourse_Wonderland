# 00_Structure_Map (课程结构映射表)

> **Document Type**: Source Code (Skeleton)
> **Compiler Target**: 03_Scripts/S0x_Transcript.md
> **Pedagogy**: Scaffolding Loop + Director's Choice
> **Total Duration**: 80 Minutes (Allocated)

> **Legend**:
> *   **Role**: A=Artist, L=Lead, D=Director, Q=Question, U=User
> *   **Mode**: N=Narrative, B=Beat, C=Conflict, O=Opening, E=Ending

---

## 模块一：导入 (S01_Intro)
*   **Time**: 00:00 - 05:00
*   **Theme**: 无形(声音)空间秩序的导演的觉醒
*   **Goal**: 建立“技术服务于表达”的观念，修补知识盲区，引出 MVP 任务。

| Timeline | Topic | Key Content/Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **0-1'** | Opening | 我是林昕。承接陈老师(A/L/D/Q/U)。引入本课(N/B/C/O/E)。 | `[SLIDE: S01_Title]` (声音魔术师) | N/A |
| **1-3'** | Bad Case Crash | **【知识修补】** 快速展示"脏音频"。指认：这是电流(Hum)，这是爆音(Click)，这是底噪(Hiss)。今天只杀最大的敌人：底噪。 | `[SLIDE: S02_BadCase]` (波形图上的脏点标记) | `[ACTION: ACT_00_Play_Bad_Audio]` |
| **3-5'** | Mission Brief | 引入 "Alice Project"。Audition 不止是扫帚（清理工具），更是画笔（创作工具）。提出核心问题：**“听众在哪里？”** | `[SLIDE: S03_Concept_Source_Space_Ear]` (声源-空间-耳朵 核心图) | N/A |

---

## 模块二：净化 (S02_Phase1_Purify)
*   **Time**: 05:00 - 20:00
*   **Theme**: 驱逐现实的尘埃
*   **Tech**: 6.6 降噪 (Noise Reduction Process)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **05-08'** | Theory (N) | 采样降噪原理：抓通缉犯(Sample) -> 全城搜捕(Process)。解释“信噪比”。 | `[SLIDE: S05_Visual_Matrix]` (采样原理图示意) | N/A |
| **08-11'** | **Guided Listening** | **深听时刻 (45s)**：闭眼感受“真空的压迫感”。<br>**【关键调整】** 屏幕显示动态频谱，避免画面静止。 | `[SLIDE: S05b_Spectrum]` (动态频谱 + 倒计时) | `[ACTION: ACT_Listen_Silence_Heartbeat]` |
| **11-14'** | **Director's Choice** | **决策时刻**：我们要“死寂的真空”(Matrix白空间) 还是 “真实的房间”(带底噪)？<br>*决定：为了做梦境，选真空。* | `[SLIDE: S05_Visual_Matrix]` | N/A |
| **14-20'** | Workshop | 执行降噪。重点演示：Capture Noise Print -> Reduce Noise。**关键检查：Output Noise Only (确保不含心跳)**。 | `[SLIDE: S05_Visual_Matrix]` (操作步骤概览) | `[ACTION: ACT_01_Capture_Print]`<br>`[ACTION: ACT_02_Reduce_Noise]` |

---

## 模块三：塑形 (S03_Phase2_Sculpt)
*   **Time**: 20:00 - 40:00
*   **Theme**: 身份的重量与脆弱
*   **Tech**: 6.10 伸缩与变调 (Stretch and Pitch)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **20-25'** | **Director's Choice** | **决策时刻**：是做“惊慌的小孩”(急促) 还是 “优雅的灵魂”(沉稳)？<br>*决定：赋予成熟与优雅。* | `[SLIDE: S08_Visual_Alice_Drink]` (爱丽丝喝药水变身静帧) | N/A |
| **25-30'** | **Guided Listening** | **深听时刻 (45s)**：闭眼辨别 **-2 semitones (粗)** 与 **-4 semitones (优雅)** 的质感区别。以及 **135% Stretch** 的舒缓感。 | `[SLIDE: S08_Visual_Alice_Drink]` | N/A |
| **30-40'** | Workshop | 1. **Stretch**: 135% (成熟)。<br>2. **Pitch**: -4 semitones (优雅)。<br>3. **Key**: 勾选 Preserve Speech Characteristics。 | `[SLIDE: S08_Visual_Alice_Drink]` | `[ACTION: ACT_04_Stretch_and_Pitch]` |

---

## 模块四：置景 (S04_Phase3_Space)
*   **Time**: 40:00 - 65:00
*   **Theme**: 时间的遗物 (深渊)
*   **Tech**: 6.7 卷积混响 (Convolution Reverb)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **40-45'** | Theory (B) | 混响不是回声。它是空间的指纹。卷积混响 = 空间的“克隆技术”。 | `[SLIDE: S11_Visual_RabbitHole]` (脉冲响应示意) | N/A |
| **45-50'** | **Guided Listening** | **深听时刻 (45s)**：试错对比。**Closet (太窄) vs Hall (太假)**。我们寻找的是 "Void" (虚无)。 | `[SLIDE: S11b_Tail_Timer]` (不同空间脉冲对比) | `[ACTION: ACT_05a_Contrast_Listening]` |
| **50-65'** | Workshop | 加载 `asset_S04_void_ir.wav`。参数物理学：<br>1. **Size 150%** (拉长遗言)<br>2. **Mix 75%** (肉体消融)<br>3. **Pre-Delay 80ms** (灵魂出窍)。 | `[SLIDE: S11_Visual_RabbitHole]` | `[ACTION: ACT_05b_Convolution_Load]` |

---

## 模块五：定位 (S05_Phase4_Position)
*   **Time**: 65:00 - 75:00
*   **Theme**: 孤独的相对论 (150% vs 0%)
*   **Tech**: 6.9 立体声扩展 (Stereo Expander)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **65-68'** | Theory (O) | 立体声宽度(Width)与声像(Pan)。不仅是左右，更是“包围感”。 | `[SLIDE: S14_Visual_Inception]` (声场扇形图) | N/A |
| **68-70'** | **Guided Listening** | **深听时刻 (45s)**：戴耳机。感受声音从脑中跑到脑后的过程。 | `[SLIDE: S14_Visual_Inception]` | `[ACTION: ACT_Listen_Width]` |
| **70-75'** | Workshop | 扩展 Width > 150%。注意相位抵消警告（变红）。<br>**高潮时刻**：对比 150% 混响与 0% 心跳。 | `[SLIDE: S14_Visual_Inception]` | `[ACTION: ACT_07_Multitrack_Setup]`<br>`[ACTION: ACT_08_Contrast_Stereo]` |

---

## 模块六：总结 (S06_Summary)
*   **Time**: 75:00 - 80:00
*   **Theme**: 剧场谢幕
*   **Visual**: `[SLIDE: S16_Summary_Loop]` (净化-塑形-置景-定位 闭环图)
