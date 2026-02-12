# S02_Phase1_Purify (环节一：净化 - 驱逐现实尘埃)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 像洁癖一样严苛、神圣感。在此刻他不是技术员，而是声音的考古学家。
> **Context**: 05:00 - 20:00 (15 min)
> **Asset**: `asset_S02_dirty_heartbeat.wav` (v12)
> **Ref**: [SLIDE: S02_Cover]

---

### Segment 0: 观念重塑 (驱逐)

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Cover]`
> *   **Scene**: 黑暗中的光束驱逐尘埃 (Expulsion).
> *   **Text**: 模块二：净化 (S02_Cover)

**[AUDIO]**
(严肃地，声音压低)
假如我们站在手术台前。

摆在面前的，是一段并不完美的录音。
很多人拿到它的第一反应是：“老师，这声音太脏了，我要降噪。”
就像回家要扫地、做饭要洗菜一样，把它当成了一项枯燥的家务，对吗？
(指引性语气)
首先，请戴上耳机，仔细听这段原始素材。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Preview_NoiseOnly]`
> *   **Action**: [ACT: Play_Audio] 播放原始带噪音频，展示其杂乱不堪。
> *   **Note**: "先听一下这个带有噪声心跳的声音。"

**[AUDIO]**
你听到什么？
第一感觉，是**巨大的、嘈杂的背景底噪**，像沙尘暴一样扑面而来，几乎淹没了一切。
而在这层厚厚的尘埃之下，掩埋着一个**极其微弱、胆怯的律动**——那是爱丽丝的心跳，正在被现实世界的杂音所吞噬。

(停顿)
我们的任务，不是简单的“降噪”，而是把这个微弱的生命，从沙尘暴里抢救出来。



> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_Dust_cap]`
> *   **Scene**: Audition 波形编辑器视图。显示为混乱的初始波形。
> *   **Asset**: 已加载 `asset_S02_dirty_heartbeat.wav`。
> *   **Action**: [ACT: Zoom_In] 鼠标滚轮极度放大，寻找心跳波峰之间的杂乱锯齿（底噪）。
> *   **Callout**: 高亮选区，标注 "现实的尘埃 (The Dust of Reality)"。

> [PACING]
> *   停顿 2秒。给观众反思的时间。


(停顿，语气加重)
屏幕上这些雾霾一样的噪点。
每一分贝的底噪——那些嘶嘶的电流声、窗外隐约的车流声、甚至是麦克风线材的轻微颤动——它们都是**现实世界的尘埃**。
如果要构建一个纯粹的梦境，我们必须先把这些“现实的引力”，统统赶出去。

**(Pause: 3s)**

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Voss_Clarke]`
> *   **Visual**: 引用 Voss & Clarke (1975). Pink Noise vs Bach.
> *   **Graphic**: 屏幕中央浮现 "1/f" 公式与星云图。

**[AUDIO]**
(温和转折，带有哲学意味)
但在动手之前，请保持敬畏。
> [TECH NOTE] (注 1/f 读作 One over F) 
1975年，物理学家 Voss 和 Clarke 提出了一种诗意的类比：
他们发现自然界最舒适的背景声（粉红噪音）和巴赫的协奏曲，都遵循着相似的 **1/f (One over F) 规律**。

这意味着，这层我们即将剥离的“尘埃”，虽然听起来是杂乱的白噪，但在统计学本质上，它依然试图模仿宇宙的心跳。
我们不是在简单地清扫垃圾，我们是在做一场精密的外科手术——试图分离两个纠缠在一起的生命体。

---

### Segment 1: 采样与法医鉴定 (法医样本)

> *   **Ref**: `[SLIDE: S02_UI_NoisePrint_cap]`
> *   **Scene**: 波形视图。
> *   **Action**: [ACT: Select_Range] 鼠标在大波峰（心跳）之间，极其小心地选中一段平坦区域（建议 1-2秒，至少 0.5s）。
> *   **Callout**: 高亮选区，标注 "仅噪音印记 (指纹)"。

**[AUDIO]**
(指引性语气，像法医)
请大家看这段波形。在驱逐尘埃之前，必须先告诉 Audition：什么是“尘埃”。
这就是 **采样 (Capture Noise Print)** 的意义。它不是截图，它是提取“指纹”。

请大家盯着这段波形。
那些**隐约可见的律动**是爱丽丝微弱的心跳（信号），而那些平坦区域里密密麻麻的毛刺，就是我们要通缉的犯人（噪音）。
现在，我们做一件**生死攸关**的事：
在波形中，**选中**一段**绝对没有心跳波峰**的区域，尽量寻找 **1 到 2 秒** 的长度。

> [VISUAL]
> *   **Action**: [ACT: Key_Shift_P] 按下快捷键，弹出 "Noise Print Captured" (已捕获噪音印记) 对话框。
> *   **Action**: [ACT: Click_OK] 确认捕获。

**[AUDIO]**
选好之后，按下 `Shift + P`，捕获它。

> [PACING]
> *   放慢语速，强调后果的严重性。

(警示)
一定要避开心跳。
如果你不小心采样到了心跳的一角，Audition 就会认为“心跳也是噪音”。
那样，当你按下“降噪”按钮的那一刻，你也杀死了爱丽丝。

---

### Segment 1.5: 不存在的无 (The Impossible Silence)

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Anechoic_Chamber]`
> *   **Scene**: John Cage 坐在消声室中。
> *   **Tagline**: "The Impossible Silence (John Cage, 1951)"

**[AUDIO]**
(声音变得非常轻，近乎耳语)
在你按下处理键之前，我想讲一个关于“绝对安静”的故事。

1951年，先锋音乐家 **John Cage** 走进哈佛大学的消声室——一个号称能吸走 99.9% 声音的房间。
他本以为会听到绝对的死寂。
但他听到了两个声音——一个高频的电流声，以及一个低频的搏动声。
工程师告诉他：
“那个高音，是你神经系统工作的电流声；那个低音，是你血液流经血管的声音。”

Cage 顿悟了一个真理——“只要你还活着，真正的寂静就不存在。”
我们此时此刻采样的这段噪音，不仅仅是环境底噪，它是这个房间“活着的证据”。

---

### Segment 2: 制造真空与电子鸟 (The Ghost in the Machine)

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_SelectAll_EnterNR_cap]`
> *   **Action**: [ACT: Select_All] **Ctrl + A** (全选音频)。 *Critical Step: Must apply to the whole file.*

**[AUDIO]**
(果断地回到技术界面)
采样结束，大家看这里，记得按 **Ctrl+A 全选整个文件**。只降刚才采样的那一小段是没有意义的。

> [VISUAL]
> *   **Action**: [ACT: Menu_Effects] Effects > Noise Reduction > Noise Reduction (process)。
> *   **Scene**: 降噪面板弹出。

**[AUDIO]**
现在，去菜单栏找到 Effects，点击 `Noise Reduction` 面板。
这里有两个核心参数，它们是相辅相成的。

> *   **Ref**: `[SLIDE: S02_UI_NR_Panel_Basic_cap]`
> *   **Action**: [ACT: Set_Reduction] 将 "Noise Reduction" 滑块拖动到 75%。
> *   **Asset**: 参考图 `S02_UI_NR_Panel_Basic_cap.png`。

**[AUDIO]**
首先是 **Noise Reduction (降噪比例)**。
为了洗去尘埃但保留皮肤的纹理（Story），我把它谨慎地推到 **75%**（Action）。
但这还不够。很多人会犯一个错误，以为推到 **100%** 不就干净了吗?
不，如果把比例推满，而下方的力度不够，你只会得到一堆细碎的数码垃圾。

所以，盯紧下面的 **Reduce by (降噪幅度)**。
这是手术刀切入的深度。

> [VISUAL]
> *   **Action**: [ACT: Highlight_Control] 鼠标悬停在下方的 "Reduce by" 滑块，设为 **50dB**。

**[AUDIO]**
我们把它设为 **50dB**。

(神秘地)
为什么是 **50dB**？官方手册会告诉你，**20dB** 就够了，再高会有副作用。
但那是给普通广播用的。
我们要造的是一个**真空**。在这个深渊里，我们要切得更深。

为了防止产生副作用，我们必须开启显微镜模式。

(神秘地)

(停顿，解释代价)
**50dB** 的代价是什么？是声音可能会破碎。
所以，我们需要一个盾牌。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_NR_Panel_Advanced_cap]`
> *   **Action**: [ACT: Set_Precision] 展开 Advanced，将 **Precision Factor** (精度) 设为 **32**。

**[AUDIO]**
把 **Precision Factor** 设为 **32**。
这是 Audition 的“电子显微镜”模式。只有在这个精度下，我们才敢下 **50dB** 的重手。

> [VISUAL]
> *   **Action**: [ACT: Check_SpectralDecay] 检查 **Spectral Decay Rate** (频谱衰减率) 设为 **50%**。

**[AUDIO]**
同时也检查一下 **Spectral Decay Rate**，把它设为 **50%**，防止由于过度降噪产生人工伪影。

> [VISUAL]
> *   **Action**: [ACT: Set_Transition] 将 **Transition Width** (过渡宽) 设为 **0dB**。

**[AUDIO]**
然后把 **Transition Width** 设为 **0dB**。
这意味着 —— 没有灰度。要么是心跳，要么是死寂。斩立决。


(停顿，引入反面教材)
> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Boll_Spectral_Subtraction]`
> *   **Visual**: Steven Boll 的论文配图，展示谱减法原理。
> *   **Note**: "这就是 1979 年 Steven Boll 的发现。"

更重要的是，1979 年 **Steven Boll** 在研发这套算法时发现了一个**物理层面的副作用**：
当你贪婪地想要切除 100% 的噪音时，数学公式会在真空中留下奇怪的残留物。
它们听起来像金属做的鸟叫声，学名叫 **"Musical Noise" (音乐噪声/电子鸟)**。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_NR_Panel_Advanced_cap]`
> *   **Visual**: 降噪面板特写。
> *   **Graphic**: 屏幕中央浮现一只由噪点组成的“半透明幽灵鸟”（Ref: `[S02_Ghost_Math]`），随后被 "75% / 30dB" 的参数组合击碎。

**[AUDIO]**
(听到电子鸟叫声后)
这些“数字鸟叫”比原本的底噪更可怕，因为它们听起来是“假”的。

(语气转为警戒)
现在，取消勾选 **Output Noise Only**。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Demo_OutputNoiseOnlyUncheck_cap]`
> *   **Action**: [ACT: Uncheck_OutputNoiseOnly] 取消勾选 **Output Noise Only** (仅输出噪音)。这是一道“验尸”程序。

**[AUDIO]**
这个时候，你应该**只能**听到“嘶嘶”的灰尘声。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Demo_OutputNoiseOnly]`
> *   **Action**: [ACT: Check_OutputNoiseOnly] 勾选 **Output Noise Only** (仅输出噪音)。这是一道“验尸”程序。

**[AUDIO]**
在嘶嘶声中，我们隐约能听到那颗心脏在极其微弱地挣扎。
(停顿)
如果不凑近听，你甚至发现不了它。
这就像是**伤疤**。

(哲学升华)
这就是 50dB 的代价。
我们为了追求极致的真空，不得不让爱丽丝受一点点伤。
**接受它**。
不要试图去抹平这个伤疤，否则你会连同她的生命一起抹去。
只要心跳的主体还在，这一点点残留，就是她是活着的证据。


记住，我们要的是**“听不见”**，而不是**“不存在”**。
把噪音压低 50dB，就像抽干了房间里的空气。
门外依然有尘埃，但它们已经无法侵扰爱丽丝的梦境。

---

### Segment 2.5: 手术台细节 (The Surgeon's Knife)

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_NR_Panel_Advanced_cap]`
> *   **Scene**: 降噪面板频谱图。取消勾选 Output Noise Only。
> *   **Highlight**: 解释红、黄、绿粒子。

**[AUDIO]**
(严肃纠偏，技术解密)
关掉 Output Noise Only，回到正常监听。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Concept_Noise_Fingerprint]`
> *   **Action**: [ACT: Click_Point] 在蓝色曲线 (Noise Reduction Curve) 调节。
> *   **Note**: "这红黄之间，就是指纹档案。"

**[AUDIO]**
现在，请盯着这张图谱。很多人第一眼看到这些红绿像素，只觉得头大。以为这只是枯燥的工程数据。不，其实这是一个战场。
那层**黄色粒子 (Yellow)**，代表噪音最高能有多响；而底部的**红色粒子 (Red)**，则代表噪音最低能有多弱。
这红黄之间，就是我们刚刚采样的那个**噪音指纹**。

而中间那些跳动的**绿色 (Green)**，才是真正的**警戒线 (Threshold)**。
任何落在绿色下方的声音，都会像死刑犯一样，直接处决。
I
**[AUDIO]**
看见这条**蓝色控制曲线 (Noise Reduction Curve)**了吗？它是你手里的**判决笔**，也是生死的**分界线**。
所有在这条蓝线之下的，都会被系统判定为“垃圾”，统统清洗。


> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_Curve_Shape_cap]`
> *   **Action**: [ACT: Reset_Curve] 点击 Reset 按钮，将曲线重置为平直。

**[AUDIO]**
首先，点击 **Reset** 重置曲线，确保我们在一个干净的画布上。

> [VISUAL]
> *   **Action**: [ACT: Create_Points] 在蓝线上点击添加两个新节点。

**[AUDIO]**
然后在蓝线上点击，添加两个关键点。
现在，当这两个点出现在蓝线上后，我们来决定谁生谁死。

> [VISUAL]
> *   **Action**: [ACT: Drag_Point_1] 将最左侧节点拖至 **(0Hz, -43dB)**。

**[AUDIO]**
**左边的低频区**——这里藏着爱丽丝的心跳。
参考这组坐标... 把 **0Hz** 处拉到 **-43dB**。
这意味着，在这个极低频的区域，我们将降噪力度**减弱 43分贝**。
这是一份免死金牌。我们几乎不对心跳做任何降噪。

> [VISUAL]
> *   **Action**: [ACT: Drag_Point_2] 将中间节点拖至 **(3.3k, -9dB)**。

**[AUDIO]**
**中间的过渡区**——**3300Hz 处拉到 -9dB**。
给它一个温柔的坡度。

> [VISUAL]
> *   **Action**: [ACT: Drag_Point_3] 将最右侧节点维持在 **(24k, 0dB)**。
> *   **Graphic**: 形成一个从左下角攀升至右上角的“坡道”。

**[AUDIO]**
现在，来看看**右边的高频区**。
请一定要将 **24000Hz** 的位置，牢牢地**钉在 0dB**。
这是“死刑区”。对那些嘶嘶声，我们不再仁慈，要全额执行那 50dB 的降噪判决。

(补充)
不必死记硬背这些数字。
你要记住的是这个**“左低右高”的形态**。
像一个从深渊爬向光明的坡道。




记住口诀——低频放生，高频镇压。

---

### Segment 2.6: 愈合伤口 (Smoothing)

> [VISUAL]
> *   **Scene**: 降噪面板特写。
> *   **Action**: [ACT: Change_Value] 将 Smoothing 从 1 改为 4。

**[AUDIO]**
为了进一步掩盖手术痕迹，看这个 **Smoothing (平滑度)**。
如果说蓝色曲线是手术刀，那么 Smoothing 就是术后的**绷带**。


> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_Smoothing_Concept]`
> *   **Note**: "这就是 Helmholtz 的理论。"

**[AUDIO]**
(插入历史背景)
在音频处理的历史上，**Helmholtz** (赫尔姆霍茨) 曾提出耳朵是一个频谱分析仪。
这里的 Spectral Smoothing (频谱平滑)，其实是在模仿人耳的特性。
> [VISUAL]
> *   **Ref**: `[SLIDE: S02_UI_Smoothing_Set_4]`
> *   **Action**: [ACT: Set_Smoothing] 将平滑度设为 4。

**[AUDIO]**
当我们把这个值设为 **4**，我们是在告诉机器：
“不要像数学家那样精确地切割每一个频率点，要像医生那样，给这个伤口裹上一层更厚的绷带。”

简单说，就是把刚刚切开的锯齿状伤口，抚平得圆润一点。
对于心跳这种低频信号，**4** 的平滑度能防止它听起来像机械故障。

---

### Segment 3: 测不准原理 (The Uncertainty Principle)

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Visual_Apply_cap]`
> *   **Scene**: 降噪面板的高级设置区 (Advanced Settings)。
> *   **Highlight**: 高亮 "FFT Size: 4096"。


**[AUDIO]**
(学术注脚，升华主题)
大家请看面板下方，把这个 **Advanced Settings** (高级设置) 的小三角**打开**。
这给同学们的一个终极彩蛋。
看这个参数，**FFT Size**，默认是 4096。
这是一个关于 **“得失”** 的哲学选择。
1946年，全息之父 **Dennis Gabor** 在他的传世论文 **《通讯理论》 (Theory of Communication)** 中，提出了声学的 **“测不准原理” (Acoustical Uncertainty)**。

他证明了一个让所有工程师绝望的公式，那就是 **Δt 乘以 Δf，永远大于等于 1**。

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Ghost_Math]`
> *   **Note**: 展示 Shannon, Fourier, Gabor 三种图示的对比。

请看屏幕上的这张图。这定义了我们能在屏幕上看到的极限。
如果我们像**香农 (Shannon)** 那样，只画垂直的线，那我们就在乎时间，却牺牲了频率。
如果我们像**傅里叶 (Fourier)** 那样，只画水平的线，那我们就得到了频率，却丢失了时间。
而 **加博尔 (Gabor)**... 他画出了**网格**。他妥协了。他把时间与频率切割成了一个个固定面积的小方块。

这种不可分割的最小单位，被称为 **“加博尔原子” (Gabor Atom)**。
你无法同时拥有极短的时间 (Δt) 和极准的频率 (Δf)。就像盖房子，砖头的面积是固定的。你想把它压扁（获得时间精度），它就必然变宽（损失频率精度）。

> [PACING]
> *   给两个极端选项留出想象空间。

如果你选 **Small FFT (比如 512)**，时间反应极快，心跳会像拳头一样硬，但这会让底噪听起来像破碎的玻璃渣。
相反，如果你选 **Large FFT (比如 16384)**，噪音会像烟雾一样柔顺地消失，但心跳也会变得像棉花一样软弱无力。

**4096** 是我们的妥协。
我们在“真实的力度”与“梦境的模糊”之间，取了一个中间值。
我们保留了心跳作为生命的冲击力，同时也让现实的尘埃被柔顺地剥离。


最后, 闭上眼确认最后一次——心跳还在吗？那种该死的电子鸟叫声出现了吗？
只有当你确信爱丽丝还活着的时候...

> [VISUAL]
> *   **Ref**: `[SLIDE: S02_Preview_Final]`
> *   **Action**: [ACT: Click_Preview] 点击左下角的**绿色播放键 (Preview)**。

点击 **Apply**。
(声音瞬间变得清澈)
听到了吗？空气变稀薄了，但没有窒息。
现在的声音，不再属于那个嘈杂的录音棚。
它已经准备好，坠入深渊。

---
