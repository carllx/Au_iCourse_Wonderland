# Extension: 心理声学与创意混音 (Psychological Acoustics)

> **Context**: S05 进阶扩展
> **Level**: Advanced / Experimental
> **Topic**: 探索声音的心理维度 —— 阴影、意识与空间的崩塌。

---

## Part 1: 荣格阴影 (The Shadow)

在基础课程中，我们处理了“物理位置”。在这里，我们要处理“心理位置”。
如果你想在电影或游戏中创造真正的恐惧，仅仅有“怪物”是不够的。你需要让听众听到主角**被压抑的自我**。

### 1.1 声音设计 (Sound Design)
*   **Asset**: `asset_S05_shadow_self.wav`
*   **Technique**: **Reverse Reverb + Pitch Shift**
    *   **Reverse (反向)**: 物理上，反向的声音是违反因果律的（先有果后有因）。这在心理上暗示了“潜意识”——它总是先于意识到达，或者总是像幽灵一样滞后。
    *   **Pitch Shift (-3 semitones)**: 稍微降低的音调，创造出一种“迟钝但强壮”的肉体感。

### 1.2 混音策略 (Mixing Strategy)
*   **Delay (滞后)**: 让它比主声源晚 500ms 出现。
*   **Position (位置)**: **Angle -179° (正后方), Radius 17 (贴脸), Spread 30°**. 它不是在左边或右边，它在**脑后**。
    > **Ref**: `[SLIDE: S05_Ext_Shadow_Panner_cap]`
*   **Concept**: **"反向鸡尾酒会效应" (Reverse Cocktail Party Effect)**
    *   在精神分裂或极端压力下，大脑的过滤器失效。通常被忽略的背景噪音（潜意识的低语）变得震耳欲聋。

---

## Part 2: 意识之声 (The Consciousness)

如果深渊是湿润、模糊的，那么“我”必须是干燥、极其清晰的。

### 2.1 骨导模拟 (Bone Conduction Simulation)
我们如何模拟“自己听自己说话”的声音？
当你说话时，你听到的声音主要通过头骨传导，而非空气。

> [!IMPORTANT]
> **Routing Check (路由检查)**:
> *   **Output**: 设为 **Master**，而不是 `The Void`。意识必须是干的 (Dry)。
> *   **Mute Test**: 如果 Mute 掉 Reverb Bus，你应该还能清晰听到这个声音。这是它作为“清醒自我”的证明。

**EQ Recipe (骨导配方)**:
1.  **Low Shelf (低频搁架)**: @ **250Hz**, Gain **+8dB**。
    *   模拟胸腔和头骨的物理共振。
2.  **Low Pass (低通)**: @ **2000Hz**, Slope **24dB/oct**。
    *   切除所有空气感。意识是封闭的。
    > **Ref**: `[SLIDE: S05_Ext_Consciousness_EQ_cap]`
3.  **Gain (增益)**: **-3dB** (Safety Net).
4.  **Result**: 一个极其“温暖”、“沉闷”且“贴脸”的声音。它不是在耳边，它在**脑中**。

---

## Part 3: 几何崩塌 (Geometric Collapse)

在 S05 中，我们学习了用 Pan 画圆。
在这里，我们学习如何**撕裂画布**。

### 3.1 超致宽立体声 (Hyper-Stereo)
*   **Tool**: Stereo Expander
*   **Setting**: Width **> 100% (e.g., 150%)**
*   **Effect**:
    *   当 Width 超过 100% 时，左右声道的相位差会让人感觉声音来自**扬声器外侧**，甚至后方。
    *   这是一种“非自然”的听感。在自然界中，没有声音比“左耳极左，右耳极右”更宽。
    *   **Metaphor**: 现实的崩塌 (Inception)。当你需要表达主角的精神世界由于极度压力而解体时，推大 Width。
    *   **Contrast**: 将一个极窄的单声道信号 (Mono, 0%) 突然切换到一个极宽的信号 (150%)，是制造心理惊悚的终极武器。

> **History Note**: Pink Floyd 在 *Dark Side of the Moon* 现场演出中使用的 **Azimuth Co-ordinator** 就是为了在四声道系统中制造这种让观众迷失方向的漩涡。

