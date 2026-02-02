# S05_Phase4_Position (环节四：定位 - 几何学防御战)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 极简、物理、冷酷
> **Context**: 65:00 - 75:00
> **Story**: 爱丽丝失去了语言，只剩下心跳。世界（墙与针）正在围剿这个唯一的坐标。
> **Asset**: `asset_S05_heartbeat_visceral.wav`, `asset_S05_threat_pressure.wav`, `asset_S05_threat_anxiety.wav`

---

### Segment 0: 引入 - 声音的形状 (The Shape)

> *   **Note**: 视频播放至 "He is testing Presence" 结束，随即淡入黑场。

**[AUDIO]**
(精密，带有引导性)
以前我们谈论声像，总是说“左边”或者“右边”。
但在电影制作里，声像不是一个点，它是一条**轨迹 (Trajectory)**。

**(Pause: 3s)**
(感受 3s 的思考时间)

> **[VISUAL]**
> *   **Scene**: 历史影像资料 (1933)。
> *   **Action**: [ACT: Play_Clip] Alan Blumlein 在 Abbey Road 录音棚的立体声测试实验 (Walking & Talking)。
> *   **Ref**: `[SLIDE: S05_Blumlein_Walking]`
> *   **Note**: 视频播放至 "He is testing Presence" 结束，随即淡入黑场。

请看屏幕：早在 **1933 年**，当立体声之父 **Alan Blumlein** 在录音棚拍摄那部著名的测试短片 **"Walking and Talking"** 时，他并没有坐在调音台后。
(看画面)
他在麦克风前走来走去，一边数数，一边描述自己的位置。
他不是在测试线材，他是在测试**存在 (Presence)**。
他证明了：声音不应该只是贴在银幕上的墙纸，它应该是一个跟随演员移动的**幽灵实体**。

(闭上眼)
让我们闭上眼睛。
想象一根针，它不是静止在你的右耳边。
它是从远处飞来，绕着你的头顶盘旋，越来越快，最后——

(拍手声)
扎进你的眉心。


**[AUDIO]**
这就是我们今天要做的：**外部的围剿 vs 内部的防御**。

---

### Segment 1: 猎场布局 (The Setup) - Fantasound 的回响



> [!NOTE]
> **Session Setup (会话设置)**:
> *   **Mix**: 5.1 Surround (提供物理空间)。
>     *   > **Ref**: `[SLIDE: S05_Setup_Surround_NewSession]`
>     *   **Step**: File > New > Multitrack Session > Master: 5.1.
>     *   > [WARNING: Safety Check] 在 Master Track 挂载 **Hard Limiter** (-0.1dB)，防止后续操作爆音。
> *   **Bus**: 创建 "The Void" (FX1)，加载 Convolution Reverb (`asset_S04_void_ir.wav`)。
> *   **Track 1 (Heart)**:
>     *   Asset: `asset_S05_heartbeat_visceral.wav`
>     *   **Width**: **Stereo Spread 30° (Radius 0)**. 虽然是点，但不是真空的点。
>     *   **EQ**: **Parametric EQ (Low Pass 200Hz, 48dB/Oct)**.
>     *   **Processing**: 这是一个**死寂的点**。
> *   **Track 2 (Wall)**: `asset_S05_threat_pressure.wav`.
> *   **Track 3 (Needle)**: `asset_S05_threat_anxiety.wav`.


**[AUDIO]**
(精密，不容置疑)
> **[VISUAL]**
> *   **Scene**: Audition 多轨会话界面 (Multitrack Session)。
> *   **Action**: [ACT: Show_Tracks] 依次高亮 Track 1-3。
> *   **Action**: [ACT: Show_Automation] 在讲解 "蝌蚪" 时，鼠标扫过并高亮显示任意一条 Automation Lane 的关键帧连线。
> *   **Graphic**: 将六个轨道框选，标注为 "Force Field" (力场)。
> *   **Reference**: Disney *Fantasasia* (1940) 的 "Fantasound" 扬声器布局图。

首先，请看我们的时间线结构。
在进入虚空之前，我们先要建造**牢笼 (Cage)**。
**(Switch to Multitrack View)**

**Step 1: The Cage (建立笼子)**
新建一个多轨会话 (Multitrack Session)。
但在 Master 选项里，不要选 Stereo。请选择 **5.1 Surround**。
为什么？
因为立体声只是一面墙，而 5.1 是一个**笼子**。我们需要这个额外的维度来囚禁声音。
为了防止意外爆音，请务必在 Master Track 上加载硬限制器 (**Hard Limiter**)，设定为 **-0.1dB**。安全第一。

**Step 2: The Cast (引入角色)**
现在，把我们的三位演员拖入时间线：
*   **Track 1**: 那颗清晰的心跳 (`asset_S05_heartbeat_visceral`)。
*   **Track 2**: 沉重的压迫感 (`asset_S05_threat_pressure`)。
*   **Track 3**: 尖锐的焦虑 (`asset_S05_threat_anxiety`)。

**Step 3: The Void (制造虚空)**
现在的它们还需要一个存在的空间。
新建一条 **Bus Track**。命名为 "The Void"。
加载我们的 Convolution Reverb。这就是那场它们即将走进的“雨”。

---

**[AUDIO]**
**First, the foundation (先打地基)。**
大家看一眼我们的会话设置——这不再是普通的立体声。
我们将 Mix 模式改为了 **5.1 Surround**。为什么？
因为立体声是一面墙，而 5.1 是一个**笼子**。这多出来的四个声道（左环绕、右环绕、中置、低音），就是我们今天要讲故事的地方。

> [TECH NOTE: The Headphone Lie]
> **Headphone Check**: 如果你现在戴着耳机，Audition 会自动把这 6 个声道折叠回立体声 (Downmix)。
> 你依然能感觉到声音在变远，但那种“脑后发凉”的物理触感会打折。这就是维度的降级。

我们先来致敬一位历史上的巨人。
> **Ref**: `[SLIDE: S05_Fantasound_Layout]`
**Fantasound (幻想声系统)**。
请看屏幕上这张图——如果是1940年，这就是你的调音台。
迪士尼的 **《幻想曲》 (Fantasia)** 不仅发明了多声道，请注意看**胶片边缘的那条波浪线**。
那是一条 **"蝌蚪"控制轨 (Tadpole Control Track)**。

> **[VISUAL]**
> *   **Scene**: Audition 多轨会话界面，高亮显示 Automation Envelopes。
> *   **Ref**: `[SLIDE: S05_Automation_Curve]` (Source: S05_Automation_Curve_cap.png)

(切回 Audition 界面)
现在回到我们的屏幕。
我们在 Audition 里即将画下的每一条**自动化曲线 (Automation Envelopes)**，就是那些“蝌蚪”的现代后裔。
它们游动的地方，声音就有了生命。

今天，我们的 FX Bus 就是一个微型的 Fantasound 系统。

**Pre-Segment: 工作室升级 (Studio Upgrade)**

> [TEACHING MOMENT: 什么是 Bus?]
> "Bus" 不是公共汽车吗？在音频里也是！
> 这个词源自拉丁语 **"Omnibus"**，意思是“为了所有人”。
想象一下：
*   **Insert (插入)**: 给爱丽丝穿上一件雨衣。虽然她湿了，但那是她自己的事。
*   **Bus (总线)**: 让爱丽丝走进一场暴雨里。
*   雨 (Reverb) 是独立存在的环境。Track 1 的心脏走进雨里 (Send)，Track 3 的焦虑也走进雨里。
*   这就是 Bus 的核心：**环境与个体的分离**。

第一步，建立空间。创建一条新的 **Bus Track**，命名为 "The Void"。
> **Ref**: `[SLIDE: S05_Setup_Bus_Creation]`
在 Bus 上挂载我们之前准备好的 Convolution Reverb。这是一间空房子。

接下来，选中 Track 2 (Wall) 和 Track 3 (Needle)。
在 **Sends** 面板，将 Send 1 指向 "The Void"。

> [TEACHING MOMENT: Send vs Output]
> 注意，我们是用 **Send (发送)**，不是 Output (输出)。
*   **Output** 是把爱丽丝推得远远的。
*   **Send** 是让爱丽丝有一个“分身”走进房间里，而她的本体还在你面前。
我们既要听到她干枯的心跳 (Dry)，也要听到房间的回声 (Wet)。
> **Ref**: `[SLIDE: S05_Setup_Sends_Routing]`

请把这前三个轨道看作是一个**力场 (Force Field)**。

**First, the Anchor (建立锚点)。**
爱丽丝已经失去了语言。她只剩下一个最原始的生命征象：**心跳**。

(操作: Track 1)
请大家看 Track 1。我做了一个非常极端的设置：
1.  **Width**: **Stereo Spread 30°, Radius 0**.
    看这个圆点。它被死死地钉在 Center (圆心)。它是静止的。
    > **Ref**: `[SLIDE: S05_Heart_Panner_Settings_cap]`
2.  **Bone Conduction EQ (极致骨导)**:
    *   **Low Pass 200Hz (48dB/Oct)**: 这是一个极端的切除。
    *   **Gain -3dB**: 为了防止滤波产生的共振导致爆红，请略微降低增益。
    *   我们切掉了所有的高频，甚至中频。只剩下胸腔深处的震动。
    > **Ref**: `[SLIDE: S05_Heart_EQ_Settings_cap]`
    
(播放预览)
听到了吗？这个声音不是从扬声器里出来的，它是从你的**喉咙里**长出来的。
它是**内部 (Internal)** 的。
在这个疯狂旋转的世界里，这是你唯一的立足点。

---

### Segment 2: 外化 I - 压迫之墙 (The Wall)

> *   **Concept**: **ILD (Interaural Level Difference)** - 高频才有方向感。

**[AUDIO]**
有了内部的“点”，现在我们需要外部的“面”。
**The Wall (压迫之墙)**。

(操作: Track 2)
在 Track 2，我们有一堵低频的音墙。
它利用了 **双耳声级差 (ILD)** 的心理声学原理：
低频波长很长，它可以绕过你的头，让你感觉不到方向（包围感）。
但当高频出现时，它会被你的头骨挡住，产生强烈的逼近感。

我们画一条自动化曲线：
**低通滤波器 (Low Pass Filter)**: 从 **50Hz** (隐喻：闷罐般的潜意识) 逐渐打开到 **5000Hz** (隐喻：清醒的现实)。
(手指描绘曲线)
想象一下，一堵墙正从远处推过来。远处的声音应该是什么样的？闷的。近处呢？刺耳的。
同时，让这一轨发送到 "The Void" (Bus 1)。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Wall_EQ_Start]` (Start: Muffled)

> [TECH NOTE: Technical Reality]
**为什么不用简单的 Low Pass?**
Audition 的原生 Filter 旋钮在实时写入 Automation 时，由于 DSP 采样精度的步进问题，会产生台阶状的 **"Zipper Noise" (拉链噪音/电泳声)**。
为了平滑，我们像做手术一样，使用 **Parametric EQ**。
> **[VISUAL]**
> *   **Scene**: Track 2 Automation 面板。
> *   **Ref**: `[SLIDE: S05_Wall_EQ_Start]`
> *   **Action**: [ACT: Open_Parametric_EQ_Automation] 绘制 Low Pass Filter 曲线。
> *   **Concept**: **ILD (Interaural Level Difference)** - 高频才有方向感。

请在 Track 2 打开 **Parametric Equalizer** 面板。我们需要用它来手动**画**出关键帧。这种旁路手段能避免数码伪影。

(操作指引)
点击轨道上的 **Show Envelopes** 箭头，在复杂的下拉菜单中，找到这条隐秘的路径：**Rack Effect > Parametric EQ > Band 5 > Frequency**。

**Technique: 偷梁换柱**
> **Ref**: `[SLIDE: S05_Wall_EQ_End]` (End: Piercing)
我们用 **Parametric EQ 的 Band 5 (High Shelf)** 来模拟这个 Low Pass 效果：
1.  **Why High Shelf?** 为什么不用 Low Pass？由于我们需要在结尾做出“刺破耳膜”的夸张效果 (+36dB)，High Shelf 既能做减法（挡住高频），也能做加法（刺穿耳膜），比单纯的 Low Filter 更有弹性。
2.  **Automation**: 画两条线：
    *   **Frequency**: 从 2000Hz 滑向 20,000Hz。
    *   **Gain**: 从 -40dB (被挡住) 猛推到 **+12dB** (刺穿)。
    *   > [WARNING: Safety Check] +36dB 会导致爆音。这里我们限制在 +12dB，配合 Limiter 使用。

(结合播放)
感受一下：
心脏 (Track 1) 在你体内跳动，纹丝不动。
而这堵墙 (Track 2) 正在从远处的虚空，慢慢地、不可阻挡地向你压过来。
一个是**干 (Dry)** 的，一个是**湿 (Wet)** 的。
一个是**点**，一个是**面**。

---

### Segment 3: 外化 II - 焦虑之刺 (The Needle)



**[AUDIO]**
如果说墙是面的压迫，那么 Track 3 就是点的刺穿。
**The Needle (焦虑之刺)**。

它的几何形态是 **Spiral (螺旋)**。

它利用了 **混淆锥 (Cone of Confusion)** 的原理：
人类的耳朵经常分不清声音是在正脸前，还是在脑后勺。
怎么打破这个迷局？我们不仅要动 Pan (左右)，还要动 **Doppler (音调)**。

(操作: Track 3)
这一次，我们不再“表演”推子，我们要像外科医生一样**画**出焦虑。
把 Automation Mode 保持在 **Read**。
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Automation_Setup_cap]`
> *   **Ref**: `[SLIDE: S05_Act_Perform_Pan]` (Refined as Keyframe Drawing)
> *   > [DID YOU KNOW: Cone of Confusion] & Doppler Effect.

请看轨道头部，点击 **Show Envelopes** 按钮 (那个折线图标)，或者在菜单中选择 **Show Automation Lanes**。
展开它，找到 **Track Panner > Angle** 和 **RADIUS** 参数。

(动作指引)
我们来制造这场空袭。这就需要两个步骤：**螺旋逼近**与**随机盘旋**。
> **Ref**: `[SLIDE: S05_Needle_Pan_Angle_cap]`
第一，在 **Angle (角度)** 轨道上，画出剧烈的锯齿，让它在 **-180° 到 +180°** 之间快速旋转。
> **Ref**: `[SLIDE: S05_Needle_Pan_Radius_cap]`
第二，在 **Radius (半径)** 轨道上，让它从 **96% (远方的威胁)** 逼近到 **20% (贴脸的恐慌)**。
*Note*: 在 Surround Panner 中，**0% Radius (代表绝对中心)** 就是你的脑海中央。越小越近。
> **Ref**: `[SLIDE: S05_Needle_Pan_Random_cap]`
第三，赋予生命。右键点击这些关键帧，选择 **Spline Curves** (样条曲线)，让它像正弦波一样扭曲。
请记住：**切换 Spline Curve 才是模拟苍蝇盘旋的随机轨迹**。我们要的不是完美的圆，是一只**愤怒的**生物。

(停止)
看屏幕上的线条——这不是正弦波，这是你的**焦虑图谱 (Map of Anxiety)**。这才是真实的焦虑。

配合微小的 **Pitch Shift**：当它飞快划过时，让音调下降 **-50 cents**。

> [TEACHING MOMENT: The Sniper's Eye (如何对齐)]
你可能会问：怎么才能画准？
如果你把 Automation Lanes 叠在一起看，很容易眼花。
**听觉对齐法**：
1.  先画好 Pan (左右乱飞)。闭上眼听。
2.  感受那个“飞得最快”的瞬间（就是 Swish 声音最大的那一刻）。
3.  就在那个瞬间，点下 Pitch 的关键帧，把它拉低。
不需要看网格，**Your ears are faster than your eyes (你的耳朵比眼睛更快)。**

> [TECH NOTE: Physics Check (物理同步)]
这不仅仅是画两把线。**你的 Pan 旋转得越快，你的 Pitch 下降得就必须越深。**
这是物理定律（多普勒效应）。如果 Pan 疯转而 Pitch 不动，大脑的“真实感检测器”会报警。
一定要确保 Pitch 的波谷 (Dip) 对应 Pan 的最快移动点。 

音调的下坠，会欺骗你的大脑：它不仅仅在移动，它在**飞越**你。

---

### Segment 4: 几何对决 (The Showdown)

> **[VISUAL]**
> *   **Scene**: 全局总览。
> *   **Ref**: `[SLIDE: S05_Geometry_Loneliness]`
> *   **Text**: "The Geometry of Loneliness" (孤独的几何学)。

**[AUDIO]**
现在，让我们把这三个元素放在一起。
这是一场**几何学的防御战**。

(Solo Checklist)
1.  **The Heart (Internal)**: Track 1. 它是圆心。不动，干燥，闷热。代表你自己。
2.  **The Wall (External)**: Track 2. 它是收缩的圆周。潮湿，巨大，缓慢逼近。代表环境。
3.  **The Needle (External)**: Track 3. 它是切线。尖锐，疯狂，试图寻找缺口。代表威胁。

**[AUDIO (Finale)]**
就像 Pink Floyd 在 1972 年 *Dark Side of the Moon* 的巡演中做的那样。
键盘手 Rick Wright 使用了一个叫做 **Azimuth Co-ordinator** 的自制操纵杆。
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Azimuth_Coordinator]`
> *   **Ref**: Pink Floyd *Dark Side of the Moon* 的 **Azimuth Co-ordinator** (方位协调器)。
在这场几何防御战的最后，当那堵墙 (Wall) 压到眼前，当那根刺 (Needle) 转到极速——

(操作: 演示崩塌)
打开 Bus 轨道的混响插件。我们将 **Width** 参数瞬间推到 **150%**。
> **Ref**: `[SLIDE: S05_Void_Expander_Settings]`

150% 意味着声场**超越**了物理可能的边界。
感受一下：**0% 的心脏** 对比 **150% 的荒野**。
心脏被压缩成一个点，代表极致的孤独。而荒野则膨胀到无穷大，仿佛空间本身在撕裂。

**(Pause: 10s)**
> **[DEEP LISTENING]**
> (Silence: 10s)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Janet_Cardiff]`

就像艺术家 **Janet Cardiff** 的传世名作 **《四十声部经文歌》 (The Forty Part Motet)**。
她用 40 个扬声器围成一个椭圆，重构了 Tallis 的合唱曲。
深渊不是空的，它是活的。

(Full Playback)
当你在听这段声音时，请不要去听“混响好不好听”。
去感受这种**位置关系 (Positioning)**。
所有的声像移动，最终都是为了定义——**你在哪里**。
在这里，你被困在中心，无处可逃。

这就是 Audition 赋予我们的权力：我们不仅是在放置声音，我们是在**构建牢笼**。

我是林昕。
我们下节课再见。
