# Action_Map (MVP 演示操作映射表)

> **Project**: Alice Sound Theatre
> **Software**: Adobe Audition (latest)

## ACT_00_Play_Bad_Audio
*   **File**: `_Library/S0X_Shared/asset_S0X_bad_case_demo.wav`
*   **Action**: Play 10s.
*   **Observe**: **Alice's Voice** buried in Hiss (Noise) and occasional Clicks.
*   **Comment**: "听到了吗？爱丽丝被困在杂音的监狱里。我们需要把她救出来。"

## ACT_00b_Toolbox_Showcase
*   **Action**: Rapidly toggle pre-set effects.
*   **Items**:
    *   Doppler Shifter (Shift+D)
    *   Guitar Distortion (Shift+G)
    *   Center Extract (Shift+E)
*   **Goal**: Show "Possibilities" without explaining parameters.

## ACT_01_Capture_Print (捕捉噪声样本)
*   **Menu**: `Effects` > `Noise Reduction/Restoration` > `Capture Noise Print` (快捷键 Shift+P)
*   **Step**:
    1.  Select a "silent" section (only noise).
    2.  Click `Capture`.
    3.  Popup: "Current selection will be used..." -> OK.

## ACT_02_Reduce_Noise (降噪处理)
*   **Menu**: `Effects` > `Noise Reduction/Restoration` > `Noise Reduction (process)`
*   **Param**:
    *   `Noise Reduction`: **80%** (Aggressive for Void effect)
    *   `Reduce by`: **20dB**
*   **Critical Check**: Toggle `Output Noise Only`. If you hear voice, lower the threshold.
*   **Director's Call**: "Noise Reduction is not just cleaning. It is **Expelling Reality's Dust** (驱逐现实尘埃). Every decibel of noise is reality clinging to us. We need a vacuum for the dream to breathe."

## ACT_03_Vocal_Enhancer (人声增强)
*   **Menu**: `Effects` > `Special` > `Vocal Enhancer`
*   **Preset**: **Music** (Customized for Fiction).
*   **Action**: Switch to **Music Mode** to adjust "Formant" independently. We are sculpting a character, not fixing a broadcast host.

## ACT_04_Pitch_Shift (变调器)
*   **Menu**: `Effects` > `Time and Pitch` > `Pitch Shifter`
*   **Param**:
    *   `Semi-tones`: **-2** (Monster/Giant) OR **+3** (Elf).
    *   `Precision`: High.
*   **Visual**: See the duration unchanged (unlike Stretch).

## ACT_05_Convolution_Load (卷积混响加载)
*   **Menu**: `Effects` > `Reverb` > `Convolution Reverb`
*   **File**: Click `Load...` -> Select `_Library/S04_Space/ir_hall_large.wav`
*   **Director's Call**: "Decay Time isn't just room size. It is **Time's Relic** (时间的遗物). It's the sound of a lost bird trying to find the wall in the dark. 2.5s is not a length, it's the distance from home."

## ACT_06_Mix_WetDry (干湿比调整)
*   **Param**:
    *   `Mix`: **60% Wet** (Very distant).
*   **Interaction**: Drag slider from 0% to 100% while playing. Stop at 60%.

## ACT_07_Stereo_Expand (立体声扩展)
*   **Menu**: `Effects` > `Stereo Imagery` > `Stereo Expander`
*   **Param**:
    *   `Stereo Expand`: **150%** (Artificial Wide).
*   **Center Channel**: Keep `Center Pan` at 0.

## ACT_Listen_Silence_Heartbeat (深听：真空心跳)
*   **Action**: Play `_Library/S02_Purify/asset_S02_heartbeat_subtle.wav` loops.
*   **Step**:
    1.  Play Heartbeat mixed with NOISE (15s).
    2.  Sudden Cut to Heartbeat in SILENCE (15s).
    3.  Back to NOISE (15s).
*   **Goal**: Demonstrate "Unmasking". In silence, the heartbeat transients are sharp; in noise, they are smeared.
*   **Director's Call**: "It's not about volume. It's about Clarity."

## ACT_Listen_Tail (深听：混响尾音)
*   **Action**: Play a short burst ("Hello?").
*   **Duration**: 45s.
*   **Goal**: Count the seconds until the sound completely vanishes.
*   **Director's Call**: "1... 2... 3... It's still there. That's the Reverb Tail."

## ACT_Listen_Width (深听：声场边缘)
*   **Action**: Use headphones. Toggle Stereo Expander On/Off.
*   **Duration**: 40s.
*   **Goal**: Use fingers to point to where the sound comes from.
*   **Director's Call**: "150% is the **Hostile Vastness** (带着敌意的辽阔). But this is only half the story. We need the contrast."

## ACT_08_Contrast_Solitude (孤独的相对论)
*   **Action**: Play the **150% Width** Reverb Tail against the **0% Width** Heartbeat.
*   **Visual**: Show the meters. Background is everywhere; Heartbeat is a thin line in the center.
*   **Director's Call**: "The world is infinite (150%), but you are just a rusty nail in the center (0%). This tear between the two IS the sound of Solitude."
