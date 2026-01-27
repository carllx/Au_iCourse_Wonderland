# Performance_Map (课堂演示流程)

> **关联文档**: [Design Spec (参数真理)](../01_MVP_Demo/00_Design_Spec_Alice.md)
> **项目**: 爱丽丝声音剧场 (Alice Sound Theatre)
> **软件**: Adobe Audition (最新版)

## ACT_00_Intro (开场)

### ACT_00_Play_Bad_Audio
*   **文件**: `_Library/S0X_Shared/asset_S0X_bad_case_demo.wav`
*   **动作**: 播放 10秒。
*   **观察**: 嘶嘶声（底噪）如同厚重的尘埃，掩盖了底层微弱的**心跳 (Heartbeat)**。（虽然主要是人声，但我们的听觉焦点在寻找生命律动）。
*   **解说词**: "听到了吗？现实的尘埃(Hiss)太厚了。我们需要剥离它，去确认爱丽丝是否还活着（听见心跳）。"

### ACT_00b_Toolbox_Showcase
*   **动作**: 快速切换预设效果（展示可能性）。
*   **快捷键**: Shift+D (Doppler), Shift+G (Distortion), Shift+E (Center Extract)。

---

## Phase 1: 净化 (Purify) — 真相的考古学

### ACT_01_Capture_Print (捕捉噪声样本)
*   **菜单**: `Effects` > `Noise Reduction/Restoration` > `Capture Noise Print` (Shift+P)
*   **步骤**:
    1.  选择一段**没有心跳波峰**的纯噪片段。
    2.  点击 `Capture` (捕捉)。
*   **关键警告**: 如果你采样到了心跳声，降噪器会把生命律动当作垃圾抹杀掉。爱丽丝将死于你的粗心。

### ACT_02_Reduce_Noise (降噪处理)
*   **菜单**: `Effects` > `Noise Reduction/Restoration` > `Noise Reduction (process)`
*   **参数**:
    *   `Noise Reduction`: **70%** (保留一丝尘埃，不要过度洁癖)。
    *   `Reduce by`: **35dB**。
    *   `Smoothing`: **2** (磨砂玻璃质感)。
    *   **蓝色控制曲线 (Noise Reduction Curve)**: 
        *   **动作**: 在频谱图中点击**蓝色曲线**添加控制点。
        *   **目的**: 针对性地压低高频底噪，同时拉低低频处的降噪强度，以**避开并保护**心跳声所在的频段。
*   **关键检查 (The Heartbeat Check)**:
    *   勾选 `Output Noise Only` (仅输出噪声)。
    *   **Listen**: 你应该只听到单纯的“嘶嘶”声。**绝不能听到“咚咚”的心跳声**。
    *   *Correction*: 如果听到了心跳，说明采样有误或曲线压制过重，请重新调整。
*   **导演指令**: "所谓的净化，不是为了得到虚无的白纸，而是为了剥离现实的尘埃，去听见那个被孤立的本质。"

---

## Phase 2: 塑形 (Sculpt) — 丑小鸭的救赎

### ACT_04_Stretch_and_Pitch (伸缩与变调)
*   **菜单**: `Effects` > `Time and Pitch` > `Stretch and Pitch (process)`
*   **前提**: 选中整段音频 (此时是怪异的“丑小鸭”状态)。
*   **参数**:
    *   **Algorithm**: 必须切换为 **`iZotope Radius`**。
    *   `Stretch` (拉伸): **135%**。
        *   *Narrative*: **赋予成熟 (Maturity)**。让急促的动作变得舒缓沉稳。
    *   `Pitch Shift` (音调偏移): **-4** semitones。
        *   *Narrative*: **赋予优雅 (Elegance)**。增加深沉的性格底色。
    *   `Precision`: Speech (语音) + Solo Instrument (勾选)。
    *   **关键设置**: 勾选 **Preserve Speech Characteristics** (保持语音特性)。
*   **目标 (Target)**: 现在的爱丽丝，是一个**外表微小，但内心成熟、举止优雅的坚定灵魂**。
*   **对比演示**:
    *   **Stretch 变化**: 演示 <130% (急躁) vs 135% (成熟)。
    *   **Pitch 变化**: 演示 -2 (单薄) vs -4 (优雅的大提琴质感)。

---

## Phase 3: 置景 (Space) — 遗言的长度

### ACT_05a_Contrast_Listening (对比试错)
*   **目的**: 论证“为什么不能用普通混响”。
*   **Action A (Closet)**: 加载 `contrast_IR_small_closet.wav`。
    *   *Result**: 窒息、写实、犯罪片感。 -> **Reject**。
*   **Action B (Hall)**: 加载 `contrast_IR_large_hall.wav`。
    *   *Result**: 辉煌、文明、歌剧感。 -> **Reject**。
*   **解说词**: "深渊既不是棺材，也不是舞台。深渊是无限的虚无。"

### ACT_05b_Convolution_Load (真正动作: 加载深渊)
*   **菜单**: `Effects` > `Reverb` > `Convolution Reverb`
*   **文件**: 加载 `_Library/S04_Space/asset_S04_void_ir.wav`
*   **参数配置 (Abyss Physics)**:
    1.  **Room Size (房间尺寸)**: **150%**。
        *   *Purpose*: 物理拉长遗言。
    2.  **Mix Automation (混合)**:
        *   **Mix**: 0% -> **75%** (超过干声，达成“肉体消融”)。
    3.  **Damping HF (高频阻尼)**: 衰减高频。
        *   *Purpose*: 增加“黑暗的厚度”。
    4.  **Width (宽度)**: **150%**。
        *   *Purpose*: 从点声源炸裂为全景包裹。
    5.  **Pre-Delay**: **80ms** (灵魂出窍的间隙)。
*   **导演指令**: “同学们，不要迷信预设。混响太大变鬼魂，太小还在家。调到那个‘听不见地板’的临界点。”

---

## Phase 4: 定位 (Position) — 镜中双生 (Multitrack Session)

### ACT_07_Multitrack_Setup (多轨构建)
*   **动作**: 新建多轨会话 (Multitrack Session)，导入资产。
*   **轨道图谱 (Track Map)**:
    1.  **Track 1 [Voice]**: 降噪+变调后的爱丽丝语音。
        *   **Pan**: Center (0)。
    2.  **Track 2 [Heart]**: `_Library/S05_Position/asset_S05_heartbeat_visceral.wav`。
        *   **Pan**: Center (0)。
        *   **Role**: 那枚生锈的钉子。
    3.  **Track 3 [Shadow]**: `_Library/S05_Position/asset_S05_shadow_self.wav` (S05 新增资产)。
        *   **Effect**: **Reverse Voice** (反向人声) + **Slowing Tick**。
        *   **Pan**: Center (0)。它不在旁边，它就在镜子里。
    4.  **Track 4 [The World]**: `_Library/S04_Space/asset_S04_void_ir.wav` (纯湿声环境层)。

### ACT_08_Contrast_Stereo (立体声对抗)
*   **工具**: `Effects` > `Stereo Imagery` > `Stereo Expander`
*   **动作**:
    *   对 **Track 4 [The World]** 施加 **Stereo Expander**。
    *   **Width**: **150% - 200%** (带着敌意的辽阔)。
    *   对 **Track 2 [Heart]** (可选): 强制设为 Mono **0%**。
*   **导演指令**: "感受 **150% 的世界荒野** 与 **0% 的自我心跳** 之间的撕裂感。在那反向的呓语中，听见时间的枯竭。"
