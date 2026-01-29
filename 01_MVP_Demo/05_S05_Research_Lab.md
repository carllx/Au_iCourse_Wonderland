# S05 Research Lab: The Acoustics of the Void

> **Project**: Alice Sound Theatre
> **Scope**: S05_Position (Dynamic Geometry)
> **Assets**: Heartbeat, Shadow, Conscious, Wall, Needle
> **Status**: ✅ Integrated

---

## 1. 核心理论 (Core Theory): 动态几何学

在 S05 模块中，我们超越了传统的 L/R 静态声像，引入了**时间**与**心理**维度，构建了一个名为 **"The Void Geometry"** 的声场模型。

这个模型包含三个层级：
1.  **The Center (Self)**: 静态、绝对、内心。
2.  **The Trajectory (Threat)**: 动态、逼近、外部。
3.  **The Conflict (Drama)**: 意识与潜意识的镜像对立。

---

## 2. Part I: The Self (中心的静态)

### A. Track 2: The Heartbeat (生命锚点)
*   **Asset**: `asset_S05_heartbeat_visceral.wav`
*   **Design Logic**: **Bone Conduction (骨传导)**
    *   **Phenomenon**: 当一个人捂住耳朵或处于极度安静的环境中，心跳声不是通过空气传播的，而是通过组织和骨骼。
    *   **Acoustic Profile**: 截止频率极低的 Low Pass (没有高频脆响)，听起来浑浊而闷重。
    *   **Spatial**: **Mono, Center 0% Width**。它必须是声场中唯一的绝对死点。

### B. Track 6 vs Track 3: The Mirror (意识的镜像)
我们构建了一对互为镜像的声音来表达爱丽丝的精神分裂状态。

| 维度 | Track 6: Consciousness (意识) | Track 3: Shadow (潜意识) | 心理声学原理 |
|---|---|---|---|
| **方向** | Forward (正向) | **Reverse (反向)** | **Temporal Envelope Violation**: RSDA包络打破因果律，制造恐怖谷效应。 |
| **音高** | Natural | **Pitch Shift -3st** | 低频增加声音的"质量(Mass)"与"威胁感"。 |
| **空间** | **Dead Dry** (极干) | Wet (Dark Hall) | **Internal-Subjective Sound** (Michel Chion理论): 意识不应有房间反射。 |
| **频响** | **Bone EQ** (+150Hz) | Distorted | 模拟颅内共鸣的温暖感 vs 异化的失真感。 |
| **关系** | 主角 (0.7) | 回声 (0.25, +0.5s Delay) | 制造"时间镜像"：先听到思维，再听到被扭曲的潜意识回声。 |

---

## 3. Part II: The Threat (外部的动态)

我们设计了两种互补的几何运动来构建"围剿感"。

### A. Track 4: The Wall (压迫之墙)
*   **Asset**: `asset_S05_threat_pressure.wav` (低频轰鸣)
*   **Geometry**: **Approaching Wedge (逼近的楔形)**
*   **Algorithm**:
    1.  **Spectral Expansion**: Low Pass Filter 从 50Hz (Inaudible) 逐渐打开至 5000Hz (Harsh)。模拟物体从远处(只有低频绕射)移至近处(全频)的物理过程。
    2.  **Stereo Expansion**: Width 从 10% (远处的点) 扩张至 100% (面前的墙)。
*   **Narrative Function**: 正面的、物理的压迫。

### B. Track 5: The Needle (焦虑之刺)
*   **Asset**: `asset_S05_threat_anxiety.wav` (高频金属摩擦)
*   **Geometry**: **Deep Spiral (深渊螺旋)**
*   **Algorithm**:
    1.  **360° Panning**: 使用正弦波控制 Pan，频率随时间指数增加 (越转越快)。
    2.  **Doppler Effect**: 当声像穿过 Center 时微调音高，模拟飞行物的掠过感。
*   **Narrative Function**: 头顶的、神经质的撕裂。

---

## 4. Part III: The Synthesis (混音策略)

最终的 `demo_S05_spiral_mix.wav` 呈现了这样的声景：

*   **Center**: 死寂的心跳 + 顽强的理智 + 迟滞的阴影。
*   **Field**: 墙在推近，刺在旋转。
*   **Climax**: 当 Wall 打开至全频，Needle 转速达到极限时，全局 Width 推至 **150%** —— 物理空间极度拥挤，但心理空间瞬间崩塌为虚无。

---

*参考资料*:
1.  *Michel Chion, "Audio-Vision: Sound on Screen"* (Internal Sound Theory)
2.  *David Lynch, "Twin Peaks"* (Reverse Speech Aesthetic)
3.  *Voss & Clarke, "1/f noise in music and speech"* (Heartbeat Spectrum)
