# 00_Structure_Map (课程结构映射表)

> **Document Type**: Source Code (Skeleton)
> **Compiler Target**: 01_Scripts/S0x_Transcript.md
> **Pedagogy**: Scaffolding Loop + Director's Choice
> **Total Duration**: 55 Minutes (Allocated) / 60 Minutes (Max)

---

## 模块一：导入 (S01_Intro)
*   **Time**: 00:00 - 05:00
*   **Theme**: 声音导演的觉醒
*   **Goal**: 建立“技术服务于表达”的观念，修补知识盲区，引出 MVP 任务。

| Timeline | Topic | Key Content/Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **0-1'** | Opening | 我是林昕。承接陈老师(A/L/D/Q/U)。引入本课(N/B/C/O/E)。 | `[SLIDE: S01_Title]` (声音魔术师) | N/A |
| **1-3'** | Bad Case Crash | **【知识修补】** 快速展示"脏音频"。指认：这是电流(Hum)，这是爆音(Click)，这是底噪(Hiss)。今天只杀最大的敌人：底噪。 | `[SLIDE: S02_BadCase]` (波形图上的脏点标记) | `[ACTION: ACT_00_Play_Bad_Audio]` |
| **3-5'** | Mission Brief | 引入 "Alice Project"。Audition 不止是扫帚（清理工具），更是画笔（创作工具）。提出核心问题：**“听众在哪里？”** | `[SLIDE: S03_Concept_Source_Space_Ear]` (声源-空间-耳朵 核心图) | N/A |

---

## 模块二：净化 (S02_Phase1_Purify)
*   **Time**: 05:00 - 11:00
*   **Theme**: 还原纯净画布
*   **Tech**: 6.6 降噪 (Noise Reduction Process)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **05-08'** | Theory (N) | 采样降噪原理：抓通缉犯(Sample) -> 全城搜捕(Process)。解释“信噪比”。 | `[SLIDE: S05_Visual_Matrix]` (采样原理图示意) | N/A |
| **08-09'** | **Guided Listening** | **深听时刻 (45s)**：闭眼感受“真空的压迫感”。<br>**【关键调整】** 屏幕显示动态频谱，避免画面静止。 | `[SLIDE: S05b_Spectrum]` (动态频谱 + 倒计时) | `[ACTION: ACT_Listen_Silence_Heartbeat]` |
| **09-11'** | **Director's Choice** | **决策时刻**：我们要“死寂的真空”(Matrix白空间) 还是 “真实的房间”(带底噪)？<br>*决定：为了做梦境，选真空。* | `[SLIDE: S05_Visual_Matrix]` | N/A |
| **11-15'** | Workshop | 执行降噪。重点演示：Capture Noise Print -> Reduce Noise。**故意演示过度降噪的水下音(Artifacts)**。 | `[SLIDE: S05_Visual_Matrix]` (操作步骤概览) | `[ACTION: ACT_01_Capture_Print]`<br>`[ACTION: ACT_02_Reduce_Noise]` |

---

## 模块三：塑形 (S03_Phase2_Sculpt)
| **15-20'** | Theory (C/E) | 声音的“易容术”。变调(Pitch)改变骨相，增强(Enhance)改变皮相。 | `[SLIDE: S08_Visual_Alice_Drink]` (共振峰示意图) | N/A |
| **20-22'** | **Director's Choice** | **决策时刻**：爱丽丝是“变大了”(巨人/低沉) 还是 “变小了”(花栗鼠/尖细)？<br>*决定：变小了...* | `[SLIDE: S08_Visual_Alice_Drink]` (爱丽丝喝药水变身静帧) | N/A |
| **22-24'** | **Guided Listening** | **深听时刻 (45s)**：闭眼辨别 **+3 semitones (人)** 与 **+5 semitones (卡通)** 的重量区别。 | `[SLIDE: S08_Visual_Alice_Drink]` | N/A |
| **24-29'** | Workshop | 1. 手动整容(Pitch Shifter)：定调 +3。 <br>2. 一键美颜(Vocal Enhancer)：增加 Formant 厚度。 | `[SLIDE: S08_Visual_Alice_Drink]` | `[ACTION: ACT_04_Pitch_Shift]`<br>`[ACTION: ACT_03_Vocal_Enhancer]` |

---

## 模块四：置景 (S04_Phase3_Space)
*   **Time**: 29:00 - 43:00
*   **Theme**: 构建虚拟空间
*   **Tech**: 6.7 卷积混响 (Convolution Reverb)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **29-34'** | Theory (B) | 混响不是回声。它是空间的指纹。卷积混响 = 空间的“克隆技术”。 | `[SLIDE: S11_Visual_RabbitHole]` (脉冲响应示意) | N/A |
| **34-35'** | **Guided Listening** | **深听时刻 (45s)**：加载 "Cathedral" 脉冲。数秒尾音消失的时间。 | `[SLIDE: S11b_Tail_Timer]` (尾音消失倒计时动画) | `[ACTION: ACT_Listen_Tail]` |
| **35-43'** | Workshop | 加载 IR (Impulse Response)。调整 Wet/Dry。**对比：100% Wet (幽灵模式) vs 50% Wet (在场模式)。** | `[SLIDE: S11_Visual_RabbitHole]` | `[ACTION: ACT_05_Convolution_Load]`<br>`[ACTION: ACT_06_Mix_WetDry]` |

---

## 模块五：定位 (S05_Phase4_Position)
*   **Time**: 43:00 - 53:00
*   **Theme**: 导演舞台调度
*   **Tech**: 6.9 立体声扩展 (Stereo Expander)

| Timeline | Topic | Key Content / Director's Note | Visual Ref (PPT) | Action Ref (Demo) |
| :--- | :--- | :--- | :--- | :--- |
| **43-46'** | Theory (O) | 立体声宽度(Width)与声像(Pan)。不仅是左右，更是“包围感”。 | `[SLIDE: S14_Visual_Inception]` (声场扇形图) | N/A |
| **46-47'** | **Guided Listening** | **深听时刻 (45s)**：戴耳机。感受声音从脑中跑到脑后的过程。 | `[SLIDE: S14_Visual_Inception]` | `[ACTION: ACT_Listen_Width]` |
| **47-53'** | Workshop | 扩展 Width > 150%。注意相位抵消警告（变红）。 | `[SLIDE: S14_Visual_Inception]` | `[ACTION: ACT_07_Stereo_Expand]` |

---

## 模块六：总结 (S06_Summary)
*   **Time**: 53:00 - 58:00
*   **Theme**: 剧场谢幕
*   **Visual**: `[SLIDE: S16_Summary_Loop]` (净化-塑形-置景-定位 闭环图)
