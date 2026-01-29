# 🎭 Design Spec: 爱丽丝声音剧场 (Alice Sound Theatre) v2.0

> **你的身份**: 声音导演 (Sound Director)
> **演示目标**: 将一段平平无奇的干声，通过 Audition 的四个步骤，重构为“爱丽丝坠入深渊”的电影场景。
> **提交物**: (本课程为智慧导赏课，无需提交作业，请专注于课堂体验)
> **Narrative Supervisor**: 汉斯·克里斯蒂安·安徒生

---

## Phase 1: 净化 (Purify) — 真相的考古学
> *Technical Reference: Effects > Noise Reduction/Restoration > Noise Reduction (process)*
> *ACT_ID: [ACT_01_Capture_Print], [ACT_02_Reduce_Noise]*

*   **Story (Andersen)**: “所谓的净化，不是为了得到虚无的白纸，而是为了剥离现实的尘埃，去听见那个被孤立的本质。”
*   **Target**: 消除覆盖在表层的 **Hiss (现实尘埃)**，显露出底层微弱的 **Heartbeat (卑微的生命律动)**。
*   **Action**:
    *   [ ] **采样 (Capture Noise Print)**: `Shift + P`。
        *   仔细观察波形，寻找**没有心跳波峰**的纯噪片段。
        *   *Warning*: 如果你采样到了心跳声，降噪器会把心跳也当作噪音抹杀掉。爱丽丝将死于你的粗心。
    *   [ ] **降噪 (Noise Reduction)**:
        *   **Reduction**: **75%**。保留一丝尘埃，不要过度洁癖。
        *   **Reduce by**: **20-30dB**。手术刀切入的深度。
        *   **Smoothing**: **2**。磨砂玻璃质感。
        *   **Curve (蓝色曲线)**: **左低右高** (Low-Release, High-Tighten)。
            *   *Left (Low Freq)*: **拉低**。让微弱的心跳声（红色粒子）跳过门槛。
            *   *Right (High Freq)*: **抬高**。高频只有嘶嘶的尘埃（绿色粒子），必须严厉镇压。
    *   [ ] **听觉检查 (Check)**: 勾选 `Output Noise Only`。此时只能听到纯粹的“嘶嘶”声。如果还是听到了心跳的“咚咚”声，说明蓝线把心跳误杀了，请进一步**拉低**左侧蓝线。



---

## Phase 2: 塑形 (Sculpt) — 丑小鸭的救赎
> *Technical Reference: Effects > Time and Pitch > Stretch and Pitch (process)*
> *ACT_ID: [ACT_04_Stretch_and_Pitch]*

*   **Story**: 爱丽丝喝下药水，变成了一只怪异的丑小鸭。通过物理声学的重构，我们要在这个微小的躯壳中注入成熟与优雅的灵魂。
*   **Guided Listening (The Input)**: 播放 `demo_S03_ugly_duckling.wav`。
    *   *听*: 一个被魔法极度压缩的、怪异且细小的声音。
    *   *Insight*: 这是**未被塑形的原始状态**。她虽已变小，但显得急促、滑稽，缺乏作为主角的“分量”。
*   **Action (The Transformation)**:
    *   选中整段音频。算法选择 **iZotope Radius**。
    *   [ ] **1. 赋予成熟 (Maturity)**:
        *   **Stretch**: 设定为 **135%**。
        *   *Effect*: 声音从急促变得舒缓。爱丽丝不再是一个惊慌失措的小女孩，而是一个拥有沉稳心智的**成熟女性**。
        *   *Dynamics*: 若 <130%，会显得过于急躁（不够成熟）；若 >140%，则会变得迟缓呆滞。135% 是完美的成熟点。
    *   [ ] **2. 赋予优雅 (Elegance)**:
        *   **Pitch Shift**: 下调 **-4** 半音 (Semitones)。
        *   *Effect*: 声音从单薄变得厚重。这赋予了她一种深沉、坚定的性格底色，即**优雅**。
        *   *Dynamics*: 若只调 -2，听起来仅仅是变粗了；调至 -4，声音获得了一种大提琴般的质感。
    *   [ ] **3. 保护细节**:
        *   勾选 **Preserve Speech Characteristics** (保持语音特性)。
    *   [ ] **Target**: 现在的爱丽丝，是一个**外表微小，但内心成熟、举止优雅的坚定灵魂**。

---

## Phase 3: 置景 (Space) — 遗言的长度
> *Technical Reference: Effects > Reverb > Convolution Reverb*
> *ACT_ID: [ACT_05a_Contrast_Listening], [ACT_05b_Convolution_Load]*

*   **Story**: 声音在深渊里迷了路，它在消失前试图抓往墙壁的最后一次努力。
*   **Comparative Listening (The Trial)**:
    *   **1. 试错: Closet (衣帽间)**: 加载 `contrast_IR_small_closet.wav`。太窒息，像棺材。**Reject**。
    *   **2. 试错: Hall (音乐厅)**: 加载 `contrast_IR_large_hall.wav`。太文明，像歌剧。**Reject**。
*   **Action (The Choice)**:
    *   [ ] **Selection**: 加载 **`asset_S04_void_ir.wav`** (虚空)。
    *   [ ] **1. 物理尺寸 (Scale)**: 调节 **Room Size** 至 **150%**。
        *   *Meaning*: 物理拉长混响时间。这不是把房间变大，而是把“叹息”变长。
    *   [ ] **2. 坠落感 (Mix Automation)**:
        *   **Mix**: 0% -> **75%** (被虚无吞噬)。
        *   *Target*: 当 Mix > 50% 的瞬间，爱丽丝彻底失去了“实体感”。
    *   [ ] **3. 黑暗的厚度 (Damping HF)**: 衰减 **High Frequency** (高频)。
        *   *Philosophy*: 深渊是有重量的，它会吃掉高频的光泽。
    *   [ ] **4. 空间宽度 (Width)**: 推至 **150%**。
        *   *Image*: 声音从眉心一点，瞬间“炸开”包裹全身。
    *   [ ] **Pre-Delay**: **80ms**。
        *   *Note*: 制造“灵魂脱离肉体”的失重瞬间。若语速过快导致吞字，可微调至 50ms，但为了戏剧性首选 80ms。

---

## Phase 4: 定位 (Position) — 动态的几何学
> *Technical Reference: Multitrack Session > Effects > Stereo Imagery > Stereo Expander & Automation*
> *ACT_ID: [ACT_07_Multitrack_Setup], [ACT_08_Dynamic_Shape]*

*   **Story**: 在深渊底部，爱丽丝不仅要面对"孤独"(Width)，还要面对"围剿"(Motion)。
*   **Action (多轨构建)**:
    *   [ ] **Track 1 (Voice)**: 愛麗絲。**Center**。
    *   [ ] **Track 2 (Heart)**: `asset_S05_heartbeat_visceral.wav`。
        *   **Width**: 强制设为 Mono **0%** (死寂的点)。
    *   [ ] **Track 3 (Shadow)**: `asset_S05_shadow_self.wav`。
        *   *Sound*: **Reverse + Pitch Shift (-3 semitones)**。
        *   *Pan*: **Center**。它是心魔，不应该有位置偏倚。
        *   *Mix*: **0.25** (背景回声)，延迟 0.5s 开始。
    *   [ ] **Track 4 (The Wall)**: `asset_S05_threat_pressure.wav`。
        *   *Movement*: **Approaching** (逼近)。
        *   *Tech*: Low Pass Filter 逐渐打开 (50Hz -> 5000Hz) + 立体声宽度从窄变宽。
        *   *Feeling*: 一堵墙正迎面压过来。
    *   [ ] **Track 5 (The Needle)**: `asset_S05_threat_anxiety.wav`。
        *   *Movement*: **Spiral** (螺旋)。
        *   *Tech*: 360° Panning Automation + Doppler Effect (Pitch Shift)。
        *   *Feeling*: 一根刺在头顶疯狂盘旋。
    *   [ ] **Track 6 (Consciousness)**: `asset_S05_conscious_voice.wav`。
        *   *Sound*: **Dry + Bone Conduction EQ** (极干 + 骨导温暖)。
        *   *Pan*: **Center**。它是"我"的主体性位置。
        *   *Mix*: **0.7** (主角声音)。
    *   [ ] **Width Automation**:
        *   当 Track 4 & 5 逼近高潮时，将全局 Reverb 的 Width 推至 **150%**。
        *   *Experience*: 极端动态的物理压迫 vs 极端空旷的心理荒野。
*   **Experience**:
    *   即使闭上眼，你也能“看见”声音的形状：它不是平面的左右，而是立体的**漩涡**。

---

## ✅ 最终核查 (Verify)

1.  **Phase 1**: 降噪后，那颗卑微的心脏还在跳动吗？
2.  **Phase 2**: 爱丽丝的声音是“脆弱的锡兵”，而不是“滑稽的猴子”吗？
3.  **Phase 4**: 当反向的影子出现时，你感到恐惧还是好笑？（如果你想笑，说明气氛还没铺垫够，推大 Reverb）。

*“在最微小的事物中，发现最宏大的悲剧。” —— H.C. Andersen*
