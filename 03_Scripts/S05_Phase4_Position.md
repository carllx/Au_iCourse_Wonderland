# S05_Phase4_Position (环节四：定位 - 几何学的荒原)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 极简、物理、冷酷
> **Context**: 65:00 - 75:00
> **Story**: 声音不仅是波，它是点、线、面的几何运动。爱丽丝被困在绝对圆心（点），面对压迫之墙（面）和焦虑之线（线）。
> **Asset**: `asset_S05_heartbeat_visceral.wav`, `asset_S05_threat_pressure.wav`, `asset_S05_threat_anxiety.wav`, `asset_S04_void_ir.wav`
> **Ref**: [SLIDE: S05_Cover]

---

## Segment 0: 引入 - 声音的形状

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover]`
> *   **Scene**: 几何网格 (Geometry).
> *   **Text**: 模块五：定位 (S05_Cover)
> *   **Note**: 停留 ~5s，感受点线面的构成。

**[AUDIO]**
(精密，带有引导性)
在康定斯基的画笔下，世界是由三种元素构成的：**点、线、面**。
而在电影混音里，我们做的是完全相同的事情。声像（Panning）不是为了让声音变宽，而是为了在黑暗中构建**几何体**。

**(Pause: 3s)**
(感受 3s 的思考时间)

> **[VISUAL]**
> *   **Scene**: 历史影像资料 (1933)。
> *   **Action**: [ACT: Play_Clip] Alan Blumlein 在 Abbey Road 录音棚的立体声测试实验 (Walking & Talking)。
> *   **Ref**: `[SLIDE: S05_Blumlein_Walking]`
> *   **Note**: 视频播放至 "He is testing Presence" 结束，随即淡入黑场。

**[AUDIO]**
**请看屏幕**，早在 **1933 年**，立体声之父 **Alan Blumlein** 在 (Abbey Road) 录音棚拍摄了一部著名的测试短片，叫 **"Walking and Talking"**。在那时，他就在试图绘制第一条“线”。
(看画面)
他没有坐在调音台后，他在麦克风前走来走去。一边数数，一边描述自己的位置。
他证明了，声音不该只是贴在银幕上的**墙纸**。它应该是**幽灵**，仅仅在空间中移动还不够，它必须是**实体**。

(闭上眼)
让我们闭上眼睛。
在这个黑暗的荒原里，我们会遇到什么？
**一个不动的点**（你的心）。
**一面逼近的墙**（巨大的压力）。
**一条疯狂的线**（尖锐的焦虑）。

**[AUDIO]**
这就是我们今天要做的，一场声音几何形态的攻与防。

---

## Segment 1: 构建画布 (The Setup)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover_Seg1_Canvas]`
> *   **Concept**: 构建画布
> *   **Note**: 3D 容器的概念展示。

> [!NOTE]
> **Session Setup (会话设置)**:
> *   **Mix**: 5.1 Surround (提供物理空间).
> *   **Safety**: Mix Track -> Hard Limiter (-3dB).
> *   **Bus**: "The Void" (FX1) -> Convolution Reverb (`asset_S04_void_ir.wav`).
> *   **Routing**: Wall (T2) & Needle (T3) -> Send to Void. Heart (T1) -> Dry.

**[AUDIO]**
(精密，不容置疑)
首先，我们需要一张画布。但这张画布不是二维的，它是三维的。

### Phase 1: The Container (构建牢笼)

> **[VISUAL]**
> *   **Scene**: Audition 新建多轨会话窗口。
> *   **Action**: [ACT: Select_51] 在 Mix 菜单中选中 5.1 Surround。
> *   **Ref**: `[SLIDE: S05_Setup_Surround_NewSession]`

**请看屏幕，点击顶部的 File 菜单，选择 New，然后建立一个新的 Multitrack Session**。
在新建会话的对话框里，Mix 选项请务必不要选默认的 Stereo（立体声），而是选择 **5.1 Surround**。
为什么？因为立体声只是一张二维的纸，而 5.1 是一个**三维的容器**。
我们需要这个额外的维度，从前后左右来“囚禁”我们的声音。

> [TECH NOTE: The Headphone Lie]
> 如果你现在戴着耳机，Audition 会自动把这 6 个声道折叠回立体声 (Downmix)。
> 所有的“脑后”声音听起来可能会像是在“脑中”，这是物理限制，但几何逻辑依然成立。

**[注意，安全第一]**
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

**请看屏幕上的这张照片**，这不仅是历史，这是 Fantasound。
迪士尼的 **《幻想曲》 (Fantasia)** 不仅发明了多声道。请注意看**胶片边缘那条抖动的波浪线**。
在早期的体积式录音中，高频导频信号会在胶片上留下特殊的痕迹。视觉上，它们就像一群游动的、带着长尾巴的圆点。所以，工程师们给它起了一个浪漫的绰号：**"蝌蚪"控制轨 (Tadpole Control Track)**。

> **[VISUAL]**
> *   **Scene**: Audition 多轨会话界面。
> *   **Ref**: `[SLIDE: S05_Automation_Curve]`
> *   **Action**: [ACT: Show_Automation_Lane] 点击轨道标题下方的 **Show Envelopes** 按钮，展开 Volume 自动化波纹。

**现在回到我们的屏幕。请点击轨道下方的“显示包络线”按钮**。
我们在 Audition 里亲手画下的每一条**自动化曲线 (Automation Envelopes)**，其实都是那些 1940 年“光影蝌蚪”的数字化转生。
当这些“蝌蚪”在你的屏幕上游动时，静止的声音就开始了它在空间里的奔跑。

### Phase 2: The Inhabitants (角色入场)

现在，也就是我们的演员入场的时候了。

> **[VISUAL]**
> *   **Scene**: Audition 编辑器面板，由于导入素材产生的三个轨道。
> *   **Action**: [ACT: Import_Assets] 将 asset_S05_ 开头的三个素材拖入轨道 T1-T3。
> *   **Ref**: `[SLIDE: S05_Setup_Import_Tracks]`

**请看屏幕**，我们将三位“几何演员”依次拖入时间线。
首先是第一轨，它扮演一颗清晰的心跳 (`asset_S05_heartbeat_visceral`)。
其次是第二轨，它是一堵沉重的压迫感 (`asset_S05_threat_pressure`)。
最后是第三轨，它代表着尖锐的焦虑 (`asset_S05_threat_anxiety`)。

**[AUDIO]**
(Listen)
在开始处理之前，让我们逐一听一听它们的本来面目。
首先，请听心跳。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Heart_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始心跳。

**[AUDIO]**
**听**，它是脆弱的，点状的。
其次，请听压力。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Wall_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始压力声。

**[AUDIO]**
**听**，它是沉闷的，像一堵无法穿透的墙。
最后，请听焦虑。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Needle_Raw]`
> *   **Action**: [ACT: Play_Original] 试听原始焦虑声。

**[AUDIO]**
**听**，它是尖锐的，线性的。
记住这些原始的质感，因为马上，我们就要把它们扔进**虚空**。

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
因为算法混响是**数学**构建的完美空间，而卷积混响是**物理**世界的真实拓印。
在这个几何实验里，我们需要那种**真实的荒凉感**。

> **[VISUAL]**
> *   **Scene**: Convolution Reverb 脉冲响应加载窗口。
> *   **Action**: [ACT: Load_IR] 导入 IR 素材 `asset_S04_void_ir.wav` (Void)。
> *   **Ref**: `[SLIDE: S05_Setup_IR_Detail]`

**请看 这个卷积混响效果器 窗口**，我们需要加载一个采样文件。
还记得我们在 上节课 (Phase 3 置景环节) 使用的那个代表 **虚空** 的脉冲吗？
**点击 Load 按钮**，加载这个采样素材。
如果没有找到，也可以先用 Audition 自带的 "Hall" 预设代替，但要记得把 Mix 调到 100% Wet。
把它加载进去。一间等待客人的空房子就构建好了。

---


## Segment 2: The Point (点) - 绝对圆心

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover_Seg2_Point]`
> *   **Concept**: 绝对圆心
> *   **Note**: 绝对静止的红点。

接下来是第二部分，关于点。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Visual_Guests]`
> *   **Concept**: 混响逻辑 - 内与外的隔离。
> *   **Action**: [ACT: Show_Diagram] 显示“客人与主人”的方位示意图。

**请看屏幕上的这张示意图**。那么，在这间房子里，谁是“客人”？又是谁，必须站在门外？

在这间房子里，第二轨和第三轨是**客人**，是外部的威胁。我们要把它们彻底浸泡在环境中，模糊掉它们原本干瘪的边界。
而第一轨的心跳是你的**内部核心**，是仅存的清醒。它绝对不能进入混响。一旦心脏也被混响吞噬，你就失去了定位，也就失去了“自我”。


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

**但请注意**，务必检查发送电平（Send Level）的旋钮。确保它**不是默认的负无穷**。只要你将其推起，声音就会真正进入这个通道。

(Concept)
通过这一步，我们实际上建立了一个 **“力场” (Force Field)** ：
外界的回响在虚空中漫延，而你的心脏始终保持**干涩 (Dry)**，驻守在你的胸腔圆心——也就是 **Center Channel**——独自跳动。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Heart]`
> *   **Concept**: 绝对圆心 (The Static Center).

**[AUDIO]**
(Fixated)
几何学的第一定律，就是**确立圆心**。
请看屏幕中央那个绝对静止的**红点**。
这就是我们唯一拥有的东西——我们的心跳。

> **Track 1: The Heart (心脏)。**
它是第一轨，心脏。

> **[VISUAL]**
> *   **Action**: [ACT: Open_Track_Panner] 打开 Track 1 的声像设置窗口。
> *   **Ref**: `[SLIDE: S05_Heart_Panner_Open]`

**现在，双击 Track 1 头部的小圆盘图标**，打开 **Track Panner** (轨道声像) 面板。
这就是我们的“几何绘图板”。
这里的 **Angle** 代表声音的方位，**Spread** 控制声音张开的宽度，**Radius** 决定声音离圆心的远近。
还有 **Center** 用于调节中置音箱的音量比例，以及 **LFE**，那是发送给低音炮的信号量。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Heart_Panner_Settings]`
> *   **Action**: [ACT: Zero_Radius] 将 Radius 设为 0%。

**请看此时声像面板上的参数**。
我们将 **Radius** (半径) 直接拉到 **0%**。
在几何学上，半径为零的圆，就是一个**点 (Point)**。
你会发现屏幕中心那个指示点，它被死死地“钉”在了**圆心 (Center)**。
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

**为了让这个点更纯粹**，请打开 **Parametric EQ**，使用 **Low Pass** (低通滤波)，将频率极其凶狠地切到 **200Hz** 以下。
斜率设为最陡峭的 **48分贝斜率(48dB/Oct)**。
同时，为了防止低频共振导致过载，请记得把 **Gain** (增益) 稍微拉低到 **-3dB**。

现在，请播放它。

(播放预览)
> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Diff_Material_Preview]`


听到了吗？我们切掉了所有高频的质感，只剩下那个**极简的质点**。
这个声音不再是从扬声器或喉咙的声带里出来的，而是从你胸腔深处传出来的。





---

## Segment 3: The Plane (面) - 压迫之墙

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover_Seg3_Plane]`
> *   **Concept**: 压迫之墙
> *   **Note**: 巨大的灰色面。

来到第三部分，也就是面。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Wall]`
> *   **Concept**: 几何压迫 (The Crushing Weight).
> *   **Concept**: **ILD (Interaural Level Difference)** - 低频是面，高频是纹理声音才有方向感。

**[AUDIO]**
(Heavy)
现在，视线离开中心。看那个从上方压下来的巨大**灰色体块**。
它是第二轨，那一堵压迫之墙。

**请大家在屏幕上点击并选中 Track 2。**
在这里，我们有一堵低频的音墙。
为什么它在远处？因为它目前只有低频。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_ILD_Diagram]`

> [TECH NOTE: The ILD Trick]
> **双耳声级差 (ILD)** 的原理其实很简单。低频波长很长，能像水一样绕过你的头，让你分不清方向（包围感）；只有高频波长短，会被头骨挡住，大脑才能通过两耳的音量差判别方向。
> 所以**低频代表包围 (远处/潜意识)**，**高频代表定位 (近处/现实)**。

为了制造“逼近”的效果，我们必须手动把高频找回来。


> **[VISUAL]**
> *   **Action**: [ACT: Select_Track_2] 选中 Track 2 (Wall)。
> *   **Ref**: `[SLIDE: S05_Wall_EQ_Start]`

(操作: 添加 EQ)
请在 **Track 2** 的 **Effect Rack** (效果架) 中，点击箭头，依次选择 **Filter and EQ**，然后选择 **Parametric Equalizer**。

**打开面板后**，我们面对的是一张没有任何表情的频响图。
目前的 **Band 5** (高频节点) 处于左下角，这意味着高频被彻底切除。
这就是为什么这堵墙听起来像是在“另一个房间”。

> [TECH NOTE: The GPS of Sound (为何高频决定方位？)]
> *   **Ref**: `[SLIDE: S05_Duplex_Theory_Visual]`
> *   **低频波长**，能像水一样绕过头骨 (Diffraction)，双耳几乎没有音量差。高频波长短，像光一样会被头骨挡住 (Shadow)，产生显著的 **双耳声级差 (ILD)**。

**[AUDIO]**
(Know-How)
没有高频，声音就没有具体的“位置”，只有模糊的“氛围”。
这在声学上被称为 **“双工理论” (Duplex Theory听觉双重定位理论)**。
**Track 2** 既然失去了高频，你的大脑就无法通过“头部的阴影”来锁定它。它就变成了幽灵。
我们要做的，就是把这个从左下角的阴影里找回来，赋予它实体。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Wall_EQ_HighFreq_Return_demo]`
> *   **Action**: [ACT: Watch_Demo] 观看高频回归的效果演示。

**请看屏幕演示**。
当我们把切掉的高频找回来时，原本沉闷的嗡嗡声，瞬间拥有了那种似乎能摸到的**粗糙质感**。
这就是把“远处的背景”变成了“眼前的**实体面**”。
你相信它能**撞到你**, 它才有**压迫感**。

(操作: 自动化绘制)
让我们用 **自动化包络(Automation Envelopes)** 来绘制这个“面”逼近的过程。

> **[VISUAL]**
> *   **Scene**: Track 2 Automation Panel.
> *   **Ref**: `[SLIDE: S05_EQ_Automation_Setup_cap]`
> *   **Action**: [ACT: Enable_Automation] 依次点选 Parametric EQ > Band 5 > Frequency 和 Gain。

**请点击 Track 2 轨道头部的 Show Envelopes (显示包络) 小三角**。
在下拉菜单中，我们需要分别将 **Band 5** 的 **Frequency**(频率：控制明一度) 以及 **Gain** (增益：控制响度) 勾选。

**请注意轨道头部 Read 模式下方的参数选择框**，我们可以在这里切换要编辑的曲线。

**首先，我们要处理的是频率 (Frequency)。**
请在下拉框中选择 **Frequency**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_EQ_Automation_Freq_cap]`
> *   **Action**: [ACT: Draw_Curve] 绘制 Frequency: 2000Hz -> 20,000Hz。

**请看屏幕**，在音频剪辑的**起始处**点击产生一个关键帧，为了制造“远处的模糊感”，我们将频率凶狠地压到 **2000Hz (Muffled Distance)**。
然后，在**结束处**再点一个关键帧，为了迎接“逼近的冲击”，我们把它拉满到 **20000Hz (Clear Reality)**。
这意味着“细节”从模糊逐渐变得清晰。

**画完频率后，我们立刻切换到增益 (Gain)。**
接下来，请切换到 **Gain**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_EQ_Automation_Gain_cap]`
> *   **Action**: [ACT: Draw_Curve] 绘制 Gain: -40dB -> +12dB。

**请看**同样的方法。**起始点**我们要压到 **-40dB (潜伏)**，让它如同耳语般微弱；而**结束点**我们要拉到 **12dB (爆发)**，这**代表**了能量从被压抑到无法忽视的彻底释放。


这样一来，高频的声音被**拔地而起**，强行撕开被遮蔽的距离感。

(操作: Radius 逼近)
别忘了物理位置。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Pan_Radius_Toggle_cap]`
> *   **Action**: [ACT: Enable_Radius] 勾选 Radius 包络。

**请注意**在同一个包络菜单里，找到 **Pan** (声像) 分类，勾选 **Radius** (半径)。
然后，在参数选择框中切换到 **Radius**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Pan_Radius_Curve_cap]`
> *   **Action**: [ACT: Draw_Radius] 绘制 Radius: 100% -> 50%。

**请看屏幕演示**：
我们将起始点的 **Radius** 设为 **100% (最远)**，将结束点拉低到 **50% (压迫)**。
这也是一条下潜的曲线。



现在，让我们停下来听一听最终的效果。
(Pause)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Wall_Final]`
> *   **Action**: [ACT: Watch_Preview] 观看压力逼近的效果展示。

**[AUDIO]**
(Interpret)
听到了吗？
**频谱 (Spectrum)** 的处理，让我们的大脑在混沌中确定了它的**方向**。
而 **空间 (Space)** 的处理，则让你清晰地感知到，这个声音正沿着刚才确定的方向，**向你逼近**。
这不再是模糊的噪音，而是一面巨大的**平面 (Plane)**，正缓慢地、有预谋地，向圆心——也就是向你——推压过来。

---

## Segment 4: The Line (线) - 混沌之线

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover_Seg4_Line]`
> *   **Concept**: 混沌之线
> *   **Note**: 某种神经质的线条。

进入第四部分，也就是线。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Icon_Anxiety]`
> *   **Concept**: 混沌螺旋 (The Chaotic Orbit).

**[AUDIO]**
(Sharp)
最后，看这团**白色的乱线**。

它是第三轨，就是那根焦虑的针。
它不是点，也不是面，它是疯狂旋转的**线 (Line)**。它是试图钻进你脑子里的螺旋轨迹。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Automation_Setup_cap]`
> *   **Action**: [ACT: Show_Automation] 找到和展开 Track 3 的 Pan Angle 和 Pan Radius。

**请看轨道头部**，点击 **Show Envelopes** 按钮 (那个折线图标)， 勾选 **Pan Angle** (角度) 和 **Pan Radius** (半径) 参数。
同时我们也在 **Track Panner** (轨道声像) 中找到 **Angle** (角度) 和 **Radius** (半径) 参数。 作为调节的参考. 

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Act_Perform_Pan]`
> *   **Action**: [ACT: Perform_Spiral] 绘制螺旋空袭包络。

(动作指引)
**请看**，我们来制造这场空袭。它的核心不需要复杂的理论，只有唯一的动作：**螺旋逼近 (Spiral Approach)**。
实现它, 只需要两步，分别是控制 **Angle (角度)** 和 **Radius (半径)**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Pan_Angle_cap]`
> *   **Action**: [ACT: Draw_Angle] 绘制 Angle 锯齿波。

**请看，我们先来画圈 (Angle)。**
请在 **Angle** 轨道上，
让它在 **-180°** 爬升到 **+180°**，来模拟一圈环绕。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Pan_Radius_cap]`
> *   **Action**: [ACT: Draw_Radius] 绘制 Radius 下降线。

**紧接着，我们要让它逼近 (Radius)。**
请切换到 **Radius** 轨道，画出一条“死亡俯冲线”。
让它从 **96% (远方天际)** 笔直地坠落到 **20% (眉心眼前)**，请**想象**这就像一颗子弹击中了眉心。

此时，你已经得到了一个标准的机器空袭。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Needle_Pan_Random_cap]`
> *   **Action**: [ACT: Enable_Spline] 切换 Spline Curve。

**最后，如果你觉得太死板，你也可以右键点击关键帧，选择 Spline Curves (样条曲线)。**
通过添加和编辑控制点，你可以让死板的折线变成苍蝇般不可预测的**生物轨迹**。
(Pause)
**现在，请看演示**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Needle_Final]`
> *   **Action**: [ACT: Watch_Preview] 观看焦虑飞越的效果展示。

**看**，这条**线**，正绕着那个静止的**点**，穿透那面逼近的**墙**，直刺而来。
你的脖子后面，有没有感觉到一阵凉意？

---

## Segment 5: The Geometry(几何学)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Cover_Seg5_Geometry]`
> *   **Concept**: 孤独的几何学
> *   **Note**: 最终的坍塌。

最后是第五部分，关于几何学。

> **[VISUAL]**
> *   **Scene**: 全局总览。
> *   **Ref**: `[SLIDE: S05_Geometry_Loneliness]`
> *   **Text**: "The Geometry of Loneliness" (孤独的几何学)。

**[AUDIO]**
现在，让我们把这三个元素放在一起。
这是一场**几何学的防御战**。

(Solo Checklist)
首先是第一轨的心脏，它是圆心。不动，干燥，闷热。代表你自己。
其次是第二轨的墙，它是收缩的圆周。潮湿，巨大，缓慢逼近。代表环境。
最后是第三轨的针，它是切线。尖锐，疯狂，试图寻找缺口。代表威胁。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Azimuth_Coordinator]`
> *   **Ref**: Pink Floyd *Dark Side of the Moon* 的 **Azimuth Co-ordinator** (方位协调器)。

**[AUDIO]**
就像 Pink Floyd 在 1972 年 *Dark Side of the Moon* 的巡演中做的那样。
键盘手 Rick Wright 使用了一个叫做 **Azimuth Co-ordinator** 的自制操纵杆。

(操作: 演示崩塌)
> **[VISUAL]**
> *   **Scene**: Bus Track 效果窗口。
> *   **Action**: [ACT: Add_StereoExpander] 在 Convolution Reverb 下方添加 Stereo Expander 效果器。
> *   **Ref**: `[SLIDE: S05_Void_Expander_Settings]`

**请看 Bus 轨**。为了打破物理边界，我们需要在 **Convolution Reverb** 下方，再添加一个 **Stereo Expander** (立体声扩展器)。
打开它，找到 **Stereo Expand** (立体声扩展) 参数，瞬间推到 **150%**。

150% 意味着声场**超越**了物理可能的边界。
我们撕裂了这张画布。
**0% 的点**（心脏）对比 **150% 的面**（虚空）。
几何体崩塌了，只剩下那个孤独的点，悬浮在无限的黑暗中。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Preview_Geometry_Final]`
> *   **Action**: [ACT: Play_Final_Mix] 试听最终的几何坍塌效果。

(Full Playback)
当你在听这段声音时，请不要去听“混响好不好听”。
所有的声像移动，最终都是为了定义——**你在哪里**。
在这里，你被困在中心，无处可逃。


> **[VISUAL]**
> *   **Ref**: `[SLIDE: S05_Janet_Cardiff]`

**[AUDIO]**
就像艺术家 **Janet Cardiff** 的传世名作 **《四十声部经文歌》 (The Forty Part Motet)**。
她用 40 个扬声器围成一个椭圆，重构了 Tallis 的合唱曲。

深渊不是空的，它是活的。
这就是 Audition 赋予我们的权力：我们不仅是在放置声音，我们是在**构建世界**。

我是林昕。
我们下节课再见。
