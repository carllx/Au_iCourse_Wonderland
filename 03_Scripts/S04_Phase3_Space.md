# S04_Phase3_Space (环节三：置景 - 无底深渊)

> **Role**: 林昕 (Lin Xin)
> **Tone**: 沉浸式、引导性、哲学感但通俗易懂
> **Context**: 40:00 - 65:00 (25 min)
> **Asset**: `asset_S03_alice_sculpted.wav` -> `asset_S04_alice_wet.wav`

---

### Segment 0: 空间的迷思 (The Myth of Space)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Cover_Seg0_Shape]`
> *   **Scene**: 纯白背景 vs 纯黑背景的对比图。

**[AUDIO]**
(声音极其干涩，完全贴耳)
上一节课我们把爱丽丝变小了，也把她变老了。


但她现在听起来，依然是“假”的。


为什么？
因为她还是贴在你的耳膜上。
她在录音棚的话筒前，而不是在那个无底的兔子洞里。

> [TECH NOTE: 物理学的亲密 (Proximity Effect)]
> 为什么爱丽丝的声音听起就在你耳边？除了没有混响，还因为**近讲效应**。
> 当麦克风极度靠近嘴唇时，低频会被物理放大。
> 这种“过于丰富”的低频，是我们大脑判断“距离”的原始依据——只有爱人或敌人才会靠得这么近。

通常如果是做广播剧，导播总是说：“加个大厅混响，也就是所谓的 **Hall Reverb**，让声音听起来宽一点。”
我们习惯于用混响来“造房子”——造一间教室、一座教堂，或者一间浴室。

但在爱丽丝的故事里，我要你们忘掉“建筑”这个概念，我们要挖出一个无底的空间。

> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Inchindown_Tanks]`
> *   **Scene**: 苏格兰 Inchindown 储油罐内部照片。

**[AUDIO]**
**请看屏幕。这是 Inchindown 储油罐，这里保持着世界最长的混响记录——112秒。**
这不是“房间”，这是我们要赋予爱丽丝的、绝对没有体温的**工业深渊**。

我们不是在造房子，我们是在造一个深渊，也就是所谓的 **The Abyss**。

在这个环节，我们要用声音，去丈量“绝望”的物理深度。

---

### Segment 1: 幽灵的 DNA (The DNA of Ghosts)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Cover_Seg1_Use]`
> *   **Scene**: 手绘图解：一只气球在一个巨大的黑暗洞穴中爆炸。

**[AUDIO]**
我们进入第一部分。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Balloon_Cave]`
> *   **Asset**: 动态展示声波撞击墙壁折返的路径图。
> *   **Graphic**: 爆炸瞬间的脉冲波形被提取出来，标注为 "Impulse Response (IR)".
> *   **Metaphor**: 标为 "The DNA of Space" (空间的基因)。

**[AUDIO]**
**请大家看这张波形图**。
我们将要用的工具，叫 **Convolution Reverb (卷积混响)**。
这是 Audition 里**最耗费算力、也最迷人**的效果器。

为什么说"耗费算力"？因为它需要进行复杂的数学卷积运算。
如果预览时声音开始卡顿，请暂时放下对“实时反馈”的执念。


> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_Perf_Buffer]`
> *   **Action**: Show Preferences > Audio Hardware settings if playback stutters.

> [TECH NOTE: 性能警告 (Performance Warning)]
> 卷积混响需要大量的处理能力。在预览时，你可能会听到**咔嗒声 (Clicks)** 或 **爆裂声 (Pops)**。不要惊慌，这些瑕疵在应用效果后会消失。
> 如果卡顿严重，请尝试调高你的 **I/O Buffer Size** (如设为 512 samples 以上)。


脉冲不是靠计算机算出来的假回声。它是**采样**出来的。

就像我们采样了现实世界的噪音一样，我们也可以采样现实世界的“空间”。

怎么做？
(指着屏幕上的气球)
想象一下，为了捕捉这个山洞的**声学指纹**，我们在里面放飞了一只气球。
“砰！”
这声短促的爆炸，在声学上被称为 **Impulse (脉冲)**。
它会撞击岩壁、折射、反弹，最后汇成一串长长的尾音。
我们把它录下来，它就叫 **Impulse Response**，简称 **IR**，也就是所谓的“脉冲响应”。

**[AUDIO]**
> [CULTURAL REF]: **声学摄影**，或者说 **Acoustic Photography**
> *   `[SLIDE: S04_IR_Recording]`
> 有一群像 Audio Ease 这样的声音猎人，他们潜入维也纳金色大厅或吉萨金字塔，只为录制那一声枪响。
> 有些专业的声学团队，为了获得更完美的脉冲，甚至不仅用气球，还会用**发令枪**去“射击”空间。

> **[VISUAL]**
> *   `[SLIDE: S04_Visual_Sound_Hunter]`
> 枪声比气球更短、更脆，能极其清晰地激发空间的每一个角落。
> 所以，所谓的 IR，其实就是**空间对枪声的回应**。
> 对我们来说，这叫 **"声学摄影"**——把空间的基因，也就是 **IR** 偷回来，永远定格。

这也是为什么我说它是“空间的 DNA”。
只要有了这个文件，我们就可以把爱丽丝的干声，扔进这个 DNA 里进行“卷积运算”。
无论她在哪里录音，只要经过这个计算，她就会瞬间被传送到那个山洞里。

这听起来像魔法，对吧？
所谓“魔法”，其实是数学上的 **"Convolution" (卷积运算)**。它不仅是简单的叠加，而是将空间的声学指纹刻进声音的每一毫秒里。
但魔法是有代价的。如果选错了 DNA，比如将一个充满低频的 IR 强加给同样低频的人声，会导致严重的**频谱冲突 (Frequency Masking)**。你造出来的就不是深渊，而是一锅浑浊的泥浆。

> [TECH NOTE: 脉冲文件规范 (Impulse Specs)]
> `[SLIDE: S04_Impulse_Specs]`
> 顺便说一句，如果你想自己录制 IR，要确保文件是**未压缩的 16位 或 32位** 格式，采样率得跟你的项目匹配。
> 还有一个小小的建议：**别太贪心**，脉冲长度最好不要超过 **30秒**。太长了计算机跑不动，听众也会觉得拖沓。
> 当然，除了枪声和气球，你完全可以尝试各种奇奇怪怪的声音作为脉冲——比如甩鞭子的声音，甚至是你拍手的声音。在这门课里，**实验**永远比**规范**重要。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Alvin_Lucier]`

**[AUDIO]**
> [CULTURAL REF]:
1969年，Alvin Lucier 做了一个著名的实验。他把自己说话的声音在房间里录下来，然后播放这段录音，再录下来……如此循环。最后，他的语言消失了，只剩下房间的共振频率在歌唱。
这告诉我们：**空间本身就是一种乐器**。我们不是在给爱丽丝“加特效”，我们是在让她“演奏”这个深渊。

---

### Segment 2: 试错 - 寻找虚无 (Finding the Void)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Cover_Seg2_Void]`

**[AUDIO]**
接下来，我们进入第二阶段：寻找虚无。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_Three_IRs]`
> *   **Scene**: Project Panel showing the Dry Vocal and 3 IR files (Closet, Hall, Void).

**[AUDIO]**
大家看项目面板，我们准备了三个不同的脉冲文件：衣柜、大厅，和那个特殊的“虚无”。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_IR_Types]`
> *   **Scene**: Audition `Effects > Reverb > Convolution Reverb` 面板。
> *   **Action**: [ACT: Load_IR] 鼠标悬停在 Load 按钮上。
> *   **Split Screen**: 屏幕分割为三部分，分别对应三次尝试。

**[AUDIO]**
我们在 Effects 菜单里找到 Reverb，打开 Convolution Reverb 面板。
但先别急着加载那个完美的脉冲。
在直接给出标准答案之前，我要你们先去犯两个“正确”的错误。
只有听过错误的深渊，你们才能认出真正的深渊。

**[AUDIO]**
我们先来看第一种尝试。**请看屏幕**，这是采样自一个狭窄衣柜的脉冲。仅仅是几声短促的拍手。

**(Pause: Play Video)**
> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Closet_Raw]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Closet_Raw_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放衣柜 IR 脉冲原声。

很短，很脆，几乎没有尾音。那么，如果把爱丽丝放进去是什么感觉？

**(Pause: Play Video)**
> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Closet_Result]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Closet_Result_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放加载也就是后的效果。

**[AUDIO]**
**(Pause: Play Video)**

听到了吗？太闷了。感觉像是被关在了衣柜里。这听起来太像写实的犯罪片现场，没有那种梦境般的“飘渺感”。

**[AUDIO]**
那么，如果我们把空间撑大呢？**请再听听**第二段名为“大厅”的脉冲采样。

**(Pause: Play Video)**
> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Hall_Raw]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Hall_Raw_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放大厅 IR 脉冲原声。

**[AUDIO]**
这一声枪响，有着长长的、平滑的反射。让我们来看应用后的效果。

**(Pause: Play Video)**
> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Hall_Result]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Hall_Result_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放应用大厅混响后的效果。

**[AUDIO]**
**(Pause: Play Video)**

虽然空间感宽敞了很多，像是在歌剧院里，但它还是太“文明”了。音乐厅是有墙壁的，是有观众的。

> [STORY TIME]:
> **人造的孤独 (The Synthetic Loneliness)**
> *   `[SLIDE: S04_BladeRunner_City]`
> 在电影**《银翼杀手》**里，配乐大师 **Vangelis** 使用了经典的 **Lexicon 224** 混响器。他创造出的那个湿漉漉的、霓虹闪烁的洛杉矶，并不是建立在物理真实上的。他把混响时间推到了极致，创造了一种"心理上的雨夜"。
> 有时候，**Fake is better than Real**。依然是那个道理：我们不是在复刻物理，我们是在构建心理。

而爱丽丝掉进的那个洞……那里没有观众。那里只有她自己。

所以，我们既不要衣柜，也不要舞台。我们要的是——**虚空**。

> [CULTURAL REF]:
> *   德国工业乐队 **Einstürzende Neubauten**。他们不进录音棚，而是钻进高速高路桥洞、废弃水塔里录音。为什么？因为那些非人造的、粗粝的工业废墟，有着录音棚里绝对造不出来的“压迫感”。
> *   `[SLIDE: S04_Neubauten]`
> *   爱丽丝的深渊，也必须是这样的：它充满了生锈的管道、滴水声和未知的恐惧。

**[AUDIO]**
最后，我们来听听那个特殊的、名为“虚无”的脉冲。**请注意听**，这段素材采集自一个巨大的废弃蓄水池。

> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Void_Raw]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Void_Raw_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放虚无 IR 脉冲原声。

**[AUDIO]**
**(Pause: Play Video)**

漫长、黑暗、甚至带着一点金属的质感。它有着极其漫长且黑暗的尾音。
我们来听听最终的结合。

> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Demo_IR_Void_Result]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_IR_Void_Result_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放应用虚无混响后的效果。
> *   **Scene**: Deep Listening Mode (Pure Black).

> **不存在的"虚无" (The Impossible Nothing)**
> [DID YOU KNOW]:
> *   `[SLIDE: S04_Anechoic_Chamber]`
> 音乐家 **John Cage** 曾经进过哈佛大学的消声室 (Anechoic Chamber)，那是世界上最安静的地方，墙壁吸收了 99.9% 的声音。
> 他以为他会听到绝对的死寂。结果他听到了两个声音：一个高频，一个低频。
> 工程师告诉他：高频是你神经系统工作的滋滋声，低频是你血液流动的轰鸣声。
> **"只要还有生命，就没有寂静。"**
> 

**[AUDIO]**
同样，这个名为 `Void` 的IR 并不是来自真正的虚空环境，而是一个废弃蓄水池的"呼吸声"。
它的尾音很长，因为它没有撞到墙壁。
就像黑色的墨水滴进水里，慢慢晕开，直到消失。
这就是我们要的“底色”。
但光有底色还不够。我们要通过参数调整，赋予这个深渊**物理法则**。

---

### Segment 3: 深渊物理学 (Physics of the Abyss)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Cover_Seg3_Physics]`
> *   **Scene**: 卷积混响参数面板特写。
> *   **Highlight**: 依次高亮 `Damping HF`, `Width`.

**[AUDIO]**
为了定义“绝望”的形状，我们需要利用 **Damping HF** 去吞噬光线，并推大 **Width** 以撕裂空间。

<!-- Step 1: 增益管理 (Gain Staging) - 能量控制 -->
我们来看看, 如何控制住这些能量。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_OutputGain_Headroom]`
> *   **Highlight**: Output Gain set to -3dB.
混响是能量的叠加，如果不控制增益，深渊会把电平表炸红。
大家注意那个 **Output Gain**，把它降下来 **-3dB 到 -6dB**。
我们要留出 **余地 (Headroom动态余量)**，别让深渊还没造好，电平先炸了。

<!-- Step 2: 不可变的命运 (The Immutability of Fate) -->
现在来到第二步，我们要处理“不可变的命运”。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_RoomSize]`
> *   **Highlight**: Room Size set to 100%.


> [TECH NOTE: Room Size 的真相]
> 你会发现这里有一个 **Room Size (房间尺寸)** 旋钮。
> 但它最大只能到 **100%** (即原始脉冲长度)。
> 我们必须把它推到顶，设定为 **100%**。
> 这意味着我们保留了深渊的完整深度，一毫秒都不能缩减。
> 这是一个没有折扣的坠落。


<!-- Step 3: 净化与黑暗 (Purification and Darkness) -->
接下来，让我们来讨论“如何净化深渊的黑暗”。

首先，我们要处理**频谱清理 (Spectral Cleaning)**。
这也是新手最容易犯的错误：把混响变成了"泥浆"。


> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_Conv_Damping]`

找到 **Damping LF (低频阻尼)** 参数。
请记住，在这里数值不仅代表阻尼，更代表**“保留率”**。
我们要把它设为 **75%**。
这意味着我们保留了 75% 的低频能量，让它们在这个空间里长久回荡。
这能制造出一种 **“隆隆声” (Rumble)**。爱丽丝掉进的不是下水道，而是深渊，深渊是 **厚重的**。

接下来，调整 **Damping HF (高频阻尼)**。
我们要把它降到 **35%**。
**不要推高它**。如果你把它推高，比如 100%，你会听到明显的**金属抖动声 (Flutter)**。
那种滋滋声像是一根廉价的铝合金管子，立刻破坏了神圣感。
把它压到 35%，抹去那些刺耳的高频反射，只留下温暖、黑暗的 **Warmth**。


> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Air_Absorption_Chart]`
> *   **Scene**: Air absorption coefficient chart showing higher absorption at high frequencies.
这在物理上模拟了 **Air Absorption (空气吸收)**——光线照不到深海，高频也传不到深渊。

> [TECH NOTE: 干湿声一致性]
> *   `[SLIDE: S04_UI_Conv_EQ]`
> 仅衰减混响尾音的高频——也就是 **Damping HF**——可能不够。如果你的干声依然很亮，会产生一种"在澡堂里穿西装"的违和感——干湿音色不匹配。
> 建议同步在轨道效果链中增加一个 **Parametric Equalizer（参数均衡器）**，对爱丽丝的**干声**进行低通滤波 (Low Pass Filter)，截止频率可以设在 5kHz~8kHz。整个声音场景会更加统一、协调。


**[AUDIO]**
爱丽丝的声音像是被一层厚厚的丝绒布盖住了。
这种“闷”，在音乐里是缺点，但在悬疑剧里，它就是**窒息感**。
它告诉观众：这里的空气很稀薄，这里离太阳很远。

<!-- Step 4: 空间的爆破 (The Explosion of Space) -->
最后一步，我们要制造“空间的爆破”。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_Width_150]`
> *   **Action**: Expand width to limit.
**大家看屏幕**，找到 **Width (宽度)**。
它控制着**立体声的扩展 (Stereo Spread)**。如果是 0，就是单声道。
但我们要反其道而行之，把它推到 **150%**。
干声（Dry）是一个点，像激光一样打在你额头上。
但深渊是水。它是包裹全身的。
推大 Width，你会感觉声音瞬间从眉心炸开了，它流到了你的后脑勺，流到了你的脚底。
你不再是“看着”爱丽丝，你是“就在”她身边。

---

### Segment 4: 灵魂出窍 (The Out-of-Body Experience)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Cover_Seg4_Body]`
> *   **Scene**: Pre-Delay 参数特写 (80ms)。
> *   **Metaphor**: 一个人影（实体）和它的影子（鬼魂）分离的瞬间。

**[AUDIO]**
参数调好了，但还缺最后一口气。
我们要调整一个最容易被忽视的参数：**Pre-Delay (预延时)**。
它决定了混响需要多少毫秒才能建立到**最大振幅 (Maximum Amplitude)**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_UI_PreDelay_80ms]`

**[AUDIO]**
通常为了自然听感，我们会设为 0-10 毫秒。
但为了制造**特殊效果**，我要你们把它猛推到 **80ms** (50ms 以上)。

这模拟了爱丽丝发出声音，到第一声回声传回来的时间差。

这个数字代表着"惊恐的空白"。
那第一声回响，是在 80毫秒之后才传回来的。
根据声速（340m/s）计算，这意味着最近的反射面距离她约 **13.7米**。
这 13米 的半径内，没有任何物体。
**前景是空的 (Empty Foreground)。**

这 80 毫秒的空白，就像你一脚踩空，心脏停跳的那一拍。

> [VISUAL]
> *   **Ref**: `[SLIDE: S04_Myth_Echo_Narcissus]`
> *   **Scene**: Echo 凝视着水边的 Narcissus，身体逐渐透明。

> [PHILOSOPHY]:
> **Echo 的诅咒 (The Curse of Echo)**
> 神话中的 Echo 遭受的最可怕的诅咒，不是失去爱情，而是**失去了"主动发声"的权利**。她只能被动地反射。
> 这正是 80ms Pre-Delay 的本质：在这段空白里，爱丽丝的主体性消失了。我们听到的不再是“她在说话”，而是“深渊在使用她的声音说话”。

> [TECH NOTE: 哈斯效应与身份的边界 (The Haas Boundary)]
> *   `[SLIDE: S04_Haas_Effect_Diagram]`
> 声学心理学有一个著名的**哈斯效应 (Haas Effect)**：当回声在 40ms 以内到达时，大脑会把它和干声融合，认为它们是"同一个声音"。这代表了**“完整的自我”**。
> 但在这里，我们故意把 Pre-Delay 拉到了 80ms，强行打破了大脑的融合机制。
> 听众会听到明显的**两个爱丽丝**：一个贴在耳膜上（肉体），一个在深渊底（灵魂）。这在心理声学上被称为**"人格解体" (Dissociation)**。
> *如果这种"重影"太强导致听感不适，不要缩短时间，试着降低 Dry (干声) 电平。叙事逻辑是：与其试图缝合伤口，不如干脆让肉体消散，只留下灵魂。*

> **[VISUAL]**
> *   **Scene**: **多轨编辑器 (Multitrack Editor)** 中的自动化曲线绘制界面 (Automation Lane)。
> *   **Ref**: `[SLIDE: S04_Automation_Dissolution]`
> *   **Action**: [ACT: Draw_Automation] 绘制一条从 0% 缓慢爬升到 75% 的蓝色曲线。
> *   **Text**: "Dissolution" (消融).

**[AUDIO]**
最后，请切换到**多轨编辑器**。大家看这条线。
我们要随着爱丽丝的每一次呼救，让深渊一点点吞噬她。
这在专业上叫“画包络线” (Envelope)，但其实就是**动画曲线**。

> [TECH NOTE: 破坏性 vs 非破坏性]
> 建议在 **多轨编辑器 (Multitrack Editor)** 中使用 **包络自动化 (Envelope Automation)**。这相当于盖了一层"描图纸"，随时可以擦掉重画，而不会破坏原始音频文件。

请跟着我做，只需要简单的三步：

**第一步：找到那是根线**。
> **[VISUAL]**
> *   `[SLIDE: S04_Envelope_Show_Mix]`
默认情况下，你可能看不到它。
点击轨道左下角的小三角，在菜单里找到 **Mix (混合)**。
现在，你应该能看到一条贯穿音频的蓝线。

**第二步：打点**。
> **[VISUAL]**
> *   `[SLIDE: S04_Envelope_Mix_Keyframes]`
在这条线上点一下，就会长出一个“关键帧” (Keyframe)，也就是一个小圆点。
我们在开头点一个，在结尾点一个。

**第三步：爬升**。
我们要把结尾的那个点，慢慢拉高到 **75%**。
让它形成一个**上坡**。
这就意味着：随着时间推移，爱丽丝的声音会越来越“湿”，直到最后被深渊彻底淹没。

为什么要停在 75%？因为这是一个临界点。在这里，具体的语言已经听不清了，肉体开始消融。

但请注意，千万不要推到 **100%**。那样作为人类的她就彻底消失了，只剩下一种**纯粹的情绪**在黑暗中回荡。

这，就是我们为爱丽丝建造的牢笼。

> [TECH NOTE: 增益配置 (Gain Staging) — 保险措施]
> *   `[SLIDE: S04_UI_HardLimiter]`
> 添加这种重型混响后，由于多层声音叠加，输出电平极易超过 0dBFS 导致**失真 (Distortion)**——也就是我们常说的"爆音"。
> **强烈建议**：在效果链的**最末端**增加一个 **Hard Limiter（硬限幅器）**，设置最大幅度为 **-0.1dB**。
> 这相当于给深渊加了一道"安全网"——确保深渊只有黑暗，没有爆音。

(Silence: 5s)

现在，让我们来看看最终的形态。

---

### Segment 5: 最终演示 (Final Demonstration)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Demo_Final_Static]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_Final_Static_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放无自动化的静态混响效果。
> *   **Text**: "Stage 1: The Static Abyss"

**[AUDIO]**
**大家请看**，首先，这是没有任何动态变化的效果。
**(Pause: Play Video)**

声音很深，很湿。爱丽丝确实掉下去了。
但这里有一个问题：她从一开始就在那里。
这更像是一张静态的照片，而不是一个坠落的过程。

为了表现“下坠”，我们需要让深渊一点点吞噬她。
这就要用到我们刚才说的——**包络自动化 (Automation)**。

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Demo_Final_Dynamic]`
> *   **Asset**: `S04_Phase3_Space/S04_Demo_Final_Dynamic_rec.mp4`
> *   **Action**: [ACT: Play_Video] 播放带有包络线绘制操作和最终听感的演示。
> *   **Scene**: Full screen demo showing the drawing of spline curves and the resulting sound.
> *   **Text**: "Stage 2: The Decent (Automation)"

**[AUDIO]**
**请看屏幕上的操作**。
我们不仅是画一条直线，我们是在画一条**曲线 (Spline Curve)**。
起始点是干的，只有贴耳的人声。
随着她的每一次呼救，蓝线慢慢爬升。
深渊的水位线在上涨。

**(Pause: Matching the video content)**

最后，当曲线到达 75% 的时候，她的人性被剥离了。
只剩下那个 80ms 的回声，在无尽的虚空中反弹。

这，才是真正的“坠落”。

进入下一章：定位。

---

### Segment 6: 结语 (Conclusion)

> **[VISUAL]**
> *   **Ref**: `[SLIDE: S04_Conclusion_Abyss]`
> *   **Scene**: 全黑背景，只有文字浮现，最后化为爱丽丝在深渊漂浮的概念图。

**[AUDIO]**
我们今天做的，并不是在这款软件里调整几个参数。
我们是在用 **Convolution (卷积)** 和 **Damping (阻尼)**，在安全的空调房地板上，凿开了一个通往地心的、75秒的隧道。

记住：所有的失真、拉伸、爆破……
它们存在的唯一目的，就是为了守住那 **80毫秒** 的惊恐。

因为只有在那一瞬间的绝对空白里，听众才会相信——
爱丽丝，真的掉下去了。

(Fade out)
