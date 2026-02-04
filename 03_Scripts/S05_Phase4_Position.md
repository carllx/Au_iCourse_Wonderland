# S05_Phase4_Position (环节四：定位 - 几何学防御战)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 极简、物理、冷酷
> **Context**: 65:00 - 75:00
> **Story**: 爱丽丝失去了语言，只剩下心跳。世界（墙与针）正在围剿这个唯一的坐标。
> **Asset**: `asset_S05_heartbeat_visceral.wav`, `asset_S05_threat_pressure.wav`, `asset_S05_threat_anxiety.wav`, `asset_S04_void_ir.wav`

---

### Segment 0: 引入 - 声音的形状

> *   **Note**: 视频播放至 "He is testing Presence" 结束，随即淡入黑场。

**[AUDIO]**
(精密，带有引导性)
以前我们谈论声像，总是说“左边”或者“右边”。
但在电影制作里，声像不是一个点，它是一条**轨迹**。

**(Pause: 3s)**
(感受 3s 的思考时间)

> **[VISUAL]**
> *   **Scene**: 历史影像资料 (1933)。
> *   **Action**: [ACT: Play_Clip] Alan Blumlein 在 Abbey Road 录音棚的立体声测试实验 (Walking & Talking)。
> *   **Ref**: `[SLIDE: S05_Blumlein_Walking]`
> *   **Note**: 视频播放至 "He is testing Presence" 结束，随即淡入黑场。

**请看屏幕**：早在 **1933 年**，当立体声之父 **Alan Blumlein** 在录音棚拍摄那部著名的测试短片 **"Walking and Talking"** 时，他并没有坐在调音台后。
(看画面)
他在麦克风前走来走去，一边数数，一边描述自己的位置。
他不是在测试线材，他是在测试**存在感**。
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

### Segment 1: 猎场布局 (The Setup) - 牢笼与地基

> [!NOTE]
> **Session Setup (会话设置)**:
> *   **Mix**: 5.1 Surround (提供物理空间).
> *   **Safety**: Master Track -> Hard Limiter (-3dB).
> *   **Bus**: "The Void" (FX1) -> Convolution Reverb (`asset_S04_void_ir.wav`).
> *   **Routing**: Wall (T2) & Needle (T3) -> Send to Void. Heart (T1) -> Dry.

**[AUDIO]**
(精密，不容置疑)
首先，请看我们的时间线结构。
在进入虚空之前，我们先要建造一个物理上的“牢笼”。

#### Phase 1: The Container (构建牢笼)

> **[VISUAL]**
> *   **Scene**: Audition 新建多轨会话窗口。
> *   **Action**: [ACT: Select_51] 在 Master 菜单中选中 5.1 Surround。
> *   **Ref**: `[SLIDE: S05_Setup_Surround_NewSession]`

**请看屏幕，点击顶部的 File 菜单，选择 New，然后建立一个新的 Multitrack Session**。
在新建会话的对话框里，Master 选项请务必不要选默认的 Stereo（立体声），而是选择 **5.1 Surround**。
为什么？因为立体声只是一面二维的墙，而 5.1 是一个**三维的笼子**。
我们需要这个额外的维度，从前后左右来“囚禁”我们的声音。

> [TECH NOTE: The Headphone Lie]
> **Headphone Check**: 如果你现在戴着耳机，Audition 会自动把这 6 个声道折叠回立体声 (Downmix)。
> 所有的“脑后”声音听起来可能会像是在“脑中”，这是物理限制，但逻辑依然成立。

**[注意：安全第一]**
由于 5.1 混音汇聚了六个声道的能量，极易产生数字溢出。我们需要先挂载一把“安全锁”。

> **[VISUAL]**
> *   **Scene**: Mix 轨道效果架菜单路径。
> *   **Action**: [ACT: Open_Menu] 依次点击 Amplitude and Compression > Hard Limiter。
> *   **Ref**: `[SLIDE: S05_Setup_HardLimiter_Path]`

**注意看 Mix 轨道的效果架**。
点击 Slot 1 旁边的三角箭头，在菜单中找到 **Amplitude and Compression**，选中 **Hard Limiter**。

> **[VISUAL]**
> *   **Scene**: Hard Limiter 参数设置面板。
> *   **Action**: [ACT: Set_Limiter] 将 Maximum Amplitude 拖动至 -3.0 dB。
> *   **Ref**: `[SLIDE: S05_Setup_HardLimiter]`

**挂载完成后，请看弹出的窗口**。
将 Maximum Amplitude（最大振幅） 设为 **-3.0 dB**。
这就是为你的监听系统和观众耳膜装上的“物理保险”。

做好防御准备后，我们先来致敬这场声音革命的**里程碑**。

> **[VISUAL]**
> *   **Scene**: 1940 年 Fantasound 原始布线图与四轨胶片细节。
> *   **Ref**: `[SLIDE: S05_Fantasound_Layout]`
> *   **Action**: [ACT: Highlight_Track4] 高亮显示胶片右侧的第 4 条轨道。

**请看屏幕上的这张照片**：这不仅是历史，这是 Fantasound。
迪士尼的 **《幻想曲》 (Fantasia)** 不仅发明了多声道，请注意看**胶片边缘那条抖动的波浪线**。
由于早期的面积式录音在记录高频导频信号时，视觉上就像一群游动的、带着长尾巴的圆点，所以工程师们给它起了一个浪漫的绰号：**"蝌蚪"控制轨 (Tadpole Control Track)**。

> **[VISUAL]**
> *   **Scene**: Audition 多轨会话界面。
> *   **Ref**: `[SLIDE: S05_Automation_Curve]`
> *   **Action**: [ACT: Show_Automation_Lane] 点击轨道标题下方的 **Show Envelopes** 按钮，展开 Volume 自动化波纹。

**现在回到我们的屏幕。请点击轨道下方的“显示包络线”按钮**。
我们在 Audition 里亲手画下的每一条**自动化曲线 (Automation Envelopes)**，其实都是那些 1940 年“光影蝌蚪”的数字化转生。
当这些“蝌蚪”在你的屏幕上游动时，静止的声音就开始了它在空间里的奔跑。

#### Phase 2: The Inhabitants (角色入场)

现在，也就是我们的演员入场的时候了。

> **[VISUAL]**
> *   **Scene**: Audition 编辑器面板，由于导入素材产生的三个轨道。
> *   **Action**: [ACT: Import_Assets] 将 asset_S05_ 开头的三个素材拖入轨道 T1-T3。
> *   **Ref**: `[SLIDE: S05_Setup_Import_Tracks]`

**请看屏幕**，我们将三位“演员”依次拖入时间线：
*   **Track 1 (T1-心跳)**: 那颗清晰的心跳 (`asset_S05_heartbeat_visceral`)。
*   **Track 2 (T2-墙)**: 沉重的压迫感 (`asset_S05_threat_pressure`)。
*   **Track 3 (T3-焦虑)**: 尖锐的焦虑 (`asset_S05_threat_anxiety`)。

**[AUDIO]**
(Listen)
在开始处理之前，让我们逐一听一听它们的本来面目。



**[AUDIO]**
首先，请听心跳。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Heart_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始心跳。

**[AUDIO]**
**听**，它是脆弱的，清晰的。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Wall_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始压力声。

**[AUDIO]**
其次，请听压力。


> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Needle_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始焦虑声。

**[AUDIO]**
**听**，它是沉闷的，像一堵无法穿透的墙。

**[AUDIO]**
最后，请听焦虑。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Needle_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始焦虑声。

**[AUDIO]**
**听**，它是尖锐的，神经质的。
记住这些原始的质感，因为马上，我们就要改变它们。

现在，这三个声音还漂浮在真空中。
为了让那堵代表压力的 **墙 (Wall)** 和那根代表焦虑的 **针 (Needle)** 能够展开围剿我们的耳朵，我们需要提供一个**活动空间**。我们需要建立 **"The Void" (虚空)**。

> **[VISUAL]**
> *   **Scene**: Audition 编辑器面板，新建 Bus Track 菜单路径。
> *   **Action**: [ACT: Open_Menu] 依次点击 Track > Add Bus Track。
> *   **Ref**: `[SLIDE: S05_Add_Bus_RightClick]`

**在任意轨道的空白位置点击右键**，在 **Track** (轨道) 弹出的菜单中选择 **Add Bus Track**，新建一条 **Bus Track**。
我们将它命名为 **"The Void"**。

> **[VISUAL]**
> *   **Scene**: Audition 编辑器面板，Convolution Reverb 参数设置面板。
> *   **Action**: [ACT: Set_Reverb] 将 Convolution Reverb 加载到 Bus Track 的效果架上。
> *   **Ref**: `[SLIDE: S05_Setup_Bus_Reverb]`

**请点击 Bus 轨的效果架**，加载 **Convolution Reverb** (卷积混响)。
为什么要选择 **Convolution Reverb** (卷积混响) 而不是其他算法的混响？
因为算法混响是**数学计算**出的, 更像是模拟概念上的, 完美的空间 (Artificial)，而卷积混响是**真实物理空间**的声学拓印 (Imprint)。
在这个环境里，我们需要那种**真实的荒凉感**，而不是数学上的平滑感。

> **[VISUAL]**
> *   **Scene**: Convolution Reverb 脉冲响应加载窗口。
> *   **Action**: [ACT: Load_IR] 导入 IR 素材 `asset_S04_void_ir.wav` (Void)。
> *   **Ref**: `[SLIDE: S05_Setup_IR_Detail]`

**请看 这个卷积混响效果器 窗口**，我们需要加载一个采样文件。
还记得我们在 上节课 (Phase 3 置景环节) 使用的那个代表 **虚空** 的脉冲吗？
**点击 Load 按钮**，加载这个采样素材。
如果没有找到，也可以先用 Audition 自带的 "Hall" 预设代替，但要记得把 Mix 调到 100% Wet。
把它加载进去。一间等待客人的空房子就构建好了。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Visual_Guests]`
> *   **Concept**: 混响逻辑 - 内与外的隔离。
> *   **Action**: [ACT: Show_Diagram] 显示“客人与主人”的方位示意图。

**请看屏幕上的这张示意图**。那么，在这间房子里，谁是“客人”？又是谁，必须站在门外？

- **Track 2 & 3 (墙与针)**：它们是外部的威胁，是造访这间屋子的“客人”。我们要把它们彻底浸泡在环境中，模糊掉它们原本干瘪的边界。
- **Track 1 (心跳)**：它是你的**内部核心**，是仅存的清醒。它绝对不能进入混响。一旦心脏也被混响吞噬，你就失去了定位，也就失去了“自我”。


> **[VISUAL]**
> *   **Scene**: Mixer View or Editor (Track Controls).
> *   **Action**: [ACT: Setup_Sends] 分别对 Track 2 (Wall) 和 Track 3 (Needle) 进行操作：在 Sends 面板，将 Send 1 指向 "The Void"。 **注意不要选 Track 1**。
> *   **Ref**: `[SLIDE: S05_Setup_Sends_Editor]`

**现在，请务必只选中 Track 2 压力声 (Wall) 和 Track 3 尖锐的焦虑声 (Needle)**。
不要选中代表心脏的第一轨。

**请看屏幕，我们有两种方式来完成发送设置**：

第一种，是在**编辑器面板 (Editor)**。找到轨道控制区上方的四个小图标，点击第三个类似“上下箭头”的按钮，即 **'Sends' (发送)** 切换按钮。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Setup_Sends_Routing]`

第二种，是打开顶部的 **Window** (窗口) 菜单，选择 **Mixer**，进入**调音台界面**。

**无论在哪种视图下**，请分别点击这两条轨道的 **Send 1** 目标槽位，将其指向我们刚建立的 **"The Void"**。

**注意**：请检查发送电平（Send Level）的旋钮。确保它**不是默认的负无穷**。只要你将其推起，声音就会真正进入这个通道。

(Concept)
通过这一步，我们实际上建立了一个 **“力场” (Force Field)** ：
外界的回响在虚空中漫延，而你的心脏始终保持**干涩 (Dry)**，驻守在你的胸腔圆心——也就是 **Center Channel**——独自跳动。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Heart]`
> *   **Concept**: 绝对圆心 (The Static Center).
> 
**[AUDIO]**
(Fixated)
请看屏幕中央那个绝对静止的**红点**。
这就是我们唯一拥有的东西——我们的心跳。
**Track 1: The Heart (心脏)。**

> **[VISUAL]**
> *   **Action**: [ACT: Open_Track_Panner] 打开 Track 1 的声像设置窗口。
> *   **Ref**: `[SLIDE: S05_Heart_Panner_Open]`


首先，请双击 Track Header 上的圆盘小图标，打开 **Track 1** 的 **Track Panner** (轨道声像) 面板。
**打开面板后**，在开始之前，让我们先认识一下这张地图：
*   **Angle (角度)**: 声音的方位。
*   **Spread (扩散)**: 声音张开的宽度。
*   **Radius (半径)**: 声音离圆心的远近。
*   **Center (中置)**: 中置音箱 (C) 的音量比例。
*   **LFE**: 发送给低音炮的信号量。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Heart_Panner_Settings]`
**请看此时声像面板上的参数变化**：
我们为心脏定位。
把 **Radius** (半径) **归零**。
你会发现屏幕中心那个指示点。它不再是弥散的空气，它被死死地“钉”在了**圆心 (Center)**。
它是被锚定的，它是静止的。




(操作: Track 1 EQ)
**但这还不够。** 为了拉开这种“内外对立”，我们需要更极端的听觉隔离。
这一轨是“内部”的声音，它必须像是在深水里听见自己的心跳。

> **[VISUAL]**
> *   **Action**: [ACT: Open_Menu] 在 Track 1 的效果架上点击三角按钮。
> *   **Ref**: `[SLIDE: S05_Heart_EQ_Add]`

**请看屏幕**，在 Track 1 的效果器（Effects Rack）里，找到 **Filter and EQ** (滤波与均衡) 分类，加载 **Parametric EQ** (参数均衡器)。

> **[VISUAL]**
> *   **Action**: [ACT: Open_Parametric_EQ] 打开 EQ 面板。
> *   **Ref**: `[SLIDE: S05_Heart_EQ_Settings_cap]`

**打开 EQ 后**，我们使用 **Low Pass** (低通滤波)，将频率极其凶狠地切到 **200Hz** 以下。
斜率设为最陡峭的 **48dB/Oct**。
同时，为了防止低频共振导致过载，请记得把 **Gain** (增益) 稍微拉低到 **-3dB**。
我们切掉了所有的高频，甚至中频。只剩下胸腔深处的震动。


(播放预览)
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Diff_Material_Preview]`

现在，请播放它。
听到了吗？这个声音不是从扬声器里出来的，它是从你的**喉咙里**传出来的。
它是**内部**的。
在这个疯狂旋转的世界里，这是你唯一的立足点。

---

### Segment 2: 外化 I - 压迫之墙 (The Wall)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Wall]`
> *   **Concept**: 几何压迫 (The Crushing Weight).

> *   **Concept**: **ILD (Interaural Level Difference)** - 高频才有方向感。

**[AUDIO]**
(Heavy)
现在的视线离开中心。看那个从上方压下来的巨大**灰色体块**。
它是沉重的、缓慢的、没有感情...
**Track 2: The Wall (压迫之墙)。**

> **[VISUAL]**
> *   **Action**: [ACT: Select_Track_2] 选中 Track 2 (Wall)。
> *   **Ref**: `[SLIDE: S05_Wall_EQ_Start]`

**请大家在屏幕上点击并选中 Track 2。**
在这里，我们有一堵低频的音墙。
为什么它在远处？因为它目前只有低频。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_ILD_Diagram]`

> [TECH NOTE: The ILD Trick]
> **双耳声级差 (ILD)**: 低频波长很长，会绕过你的头，让你分不清方向（包围感）。只有高频波长短，会被头骨挡住，大脑才能通过两耳的音量差判别方向。
> 所以：**低频 = 包围 (远处/潜意识)**，**高频 = 定位 (近处/现实)**。

为了制造“逼近”的效果，我们必须手动把高频找回来。

(操作: 添加 EQ)
请在 Track 2 的 Effect Rack (效果架) 中，添加一个 **Parametric Equalizer**。
我们不用常规的方法调节，我们要用 **Automation Envelopes (自动化包络)** 来画出这个过程。

> **[VISUAL]**
> *   **Scene**: Track 2 Automation Panel.
> *   **Ref**: `[SLIDE: S05_EQ_Automation_Setup_cap]`
> *   **Action**: [ACT: Enable_Automation] 依次勾选 Rack Effect > Parametric EQ > Band 5 > Frequency 和 Gain。

点击轨道头部的 **Show Envelopes** (显示包络) 小三角。
在下拉菜单中，我们需要勾选两条线：
首先，在 **Rack Effect** 中找到 **Parametric EQ**，展开 **Band 5**，勾选 **Frequency** (频率)。
其次，勾选同一位置下的 **Gain** (增益)。

现在的屏幕上会出现一紫一红两条直线。

(操作: 绘制曲线)
我们用 **Band 5 (High Shelf)** 来模拟墙体的逼近：
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_EQ_Automation_Curve_cap]`
> *   **Action**: [ACT: Draw_Curve] 绘制 Frequency 从 2k 到 20k，Gain 从 -40 到 +12 的曲线。

现在，请看屏幕。我们在坐标系上找到 **Band 5** 的那个控制点。
我们需要把它从**左下角**（低频、低音量）猛地推向**右上角**（高频、高音量）。
这就像是把高频的声音**拔地而起**，强行将被遮蔽的距离感撕开。

具体参数上：
第一步，让 **Frequency (频率)** 横向滑过，从 **2000Hz** (闷) 冲向 **20,000Hz** (亮)。
第二步，让 **Gain (音量)** 纵向拉升，从 **-40dB** (被挡住) 猛推到 **+12dB** (刺耳)。
    > [WARNING: Safety Check] 理论上我们需要 +36dB 来制造痛感，但为了保护耳朵，我们限制在 +12dB，配合 Limiter 食用。

(操作: Radius 逼近)
别忘了物理位置。
在同一个菜单里，找到 **Pan** (声像) 分类，勾选 **Radius** (半径)。
> **Ref**: `[SLIDE: S05_Pan_Radius_Toggle_cap]`

让 Radius 从 **100% (最远)** 逐渐缩小到 **50% (压迫)**。
> **Ref**: `[SLIDE: S05_Pan_Radius_Curve_cap]`

(结合播放)
感受一下：
频率打开的同时，墙体也在物理上逼近。
一个是**频谱 (Spectrum)** 的压迫，一个是**空间 (Space)** 的压迫。
双重夹击。

双重夹击。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Wall_Final]`
> *   **Action**: [ACT: Watch_Preview] 观看压力逼近的效果展示。

**[AUDIO]**
(Pause)
现在，让我们停下来听一听最终的效果。
这不是一面普通的墙。
感受那个灰色的体块是如何从远处——那个模糊的低频——通过自动化曲线的一点点抬升，逐渐逼近，直到它压迫在你的眉毛上。

---

### Segment 3: 外化 II - 焦虑之刺 (The Needle)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Anxiety]`
> *   **Concept**: 混沌螺旋 (The Chaotic Orbit).



**[AUDIO]**
(Sharp)
最后，看这团**白色的乱线**。
它不是点，也不是面，它是疯狂旋转的**针尖**。它是试图钻进你脑子里的东西。
**Track 3: The Needle (焦虑之刺)**。

它的几何形态是 **Spiral (螺旋)**。

它利用了 **混淆锥 (Cone of Confusion)** 的原理：
人类的耳朵经常分不清声音是在正脸前，还是在脑后勺。
怎么打破这个迷局？我们要让声音**动起来**。

(操作: Track 3)
这一次，我们不再“表演”推子，我们要像外科医生一样**画**出焦虑。
把 Automation Mode 保持在 **Read**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Automation_Setup_cap]`
> *   **Action**: [ACT: Show_Automation] 展开 Track 3 的 Automation Lanes，找到 Angle 和 Radius。

**请看轨道头部**，点击 **Show Envelopes** 按钮 (那个折线图标)，或者在菜单中选择 **Show Automation Lanes**。
展开它，在 **Track Panner** (轨道声像) 中找到 **Angle** (角度) 和 **Radius** (半径) 参数。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Act_Perform_Pan]` (Refined as Keyframe Drawing)

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

> [TEACHING MOMENT: The Sniper's Eye (如何对齐)]
> 你可能会问：怎么才能画准？
> 不需要看网格，画出那种杂乱无章的感觉，**Your ears are faster than your eyes (你的耳朵比眼睛更快)。**

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Needle_Final]`
> *   **Action**: [ACT: Watch_Preview] 观看焦虑飞越的效果展示。

**[AUDIO]**
(Pause)
再次停下来，观看演示，检查我们的“针”。

你的脖子后面有没有感觉到一阵凉意？

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
首先是 **The Heart (心脏)**，占据第一轨。它是圆心。不动，干燥，闷热。代表你自己。
其次是 **The Wall (墙)**，在第二轨。它是收缩的圆周。潮湿，巨大，缓慢逼近。代表环境。
最后是 **The Needle (针)**，在第三轨。它是切线。尖锐，疯狂，试图寻找缺口。代表威胁。

**[AUDIO (Finale)]**
就像 Pink Floyd 在 1972 年 *Dark Side of the Moon* 的巡演中做的那样。
键盘手 Rick Wright 使用了一个叫做 **Azimuth Co-ordinator** 的自制操纵杆。
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Azimuth_Coordinator]`
> *   **Ref**: Pink Floyd *Dark Side of the Moon* 的 **Azimuth Co-ordinator** (方位协调器)。
在这场几何防御战的最后，当那堵墙 (Wall) 压到眼前，当那根刺 (Needle) 转到极速——

(操作: 演示崩塌)
> **[VISUAL]**
> *   **Scene**: Bus Track 效果窗口。
> *   **Action**: [ACT: Open_Reverb] 打开 Void 轨道的混响插件窗口。
> *   **Ref**: `[SLIDE: S05_Void_Expander_Settings]`

**请看 Bus 轨**。点击打开那个 **Convolution Reverb** 效果器的窗口。
找到 **Width** (宽度) 推子。
我们要做的不是画线，而是**实时手控**。
**按住鼠标**，将 **Width** 参数瞬间推到 **150%**。

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
所有的声像移动，最终都是为了定义——**你在哪里**。
在这里，你被困在中心，无处可逃。

这就是 Audition 赋予我们的权力：我们不仅是在放置声音，我们是在**构建牢笼**。

我是林昕。
我们下节课再见。
