# Action_Map (MVP 演示操作映射表)

> **Project**: Alice Sound Theatre
> **Software**: Adobe Audition (latest)

## ACT_00_Play_Bad_Audio
*   **File**: `assets/bad_case_demo.wav`
*   **Action**: Play 10s.
*   **Observe**: Hiss (Noise), Hum (60Hz), Click (Pops).
*   **Comment**: "听到了吗？这就是灾难现场。"

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
*   **Director's Call**: "For normal podcast, 50% is enough. But for Alice's dream, we want 80% absolute silence."

## ACT_03_Vocal_Enhancer (人声增强)
*   **Menu**: `Effects` > `Special` > `Vocal Enhancer`
*   **Preset**: `Male` (if source is low) or `Music` (for background).
*   **Action**: Toggle `Male` mode to add "Broadcast Quality" bottom end.

## ACT_04_Pitch_Shift (变调器)
*   **Menu**: `Effects` > `Time and Pitch` > `Pitch Shifter`
*   **Param**:
    *   `Semi-tones`: **-2** (Monster/Giant) OR **+3** (Elf).
    *   `Precision`: High.
*   **Visual**: See the duration unchanged (unlike Stretch).

## ACT_05_Convolution_Load (卷积混响加载)
*   **Menu**: `Effects` > `Reverb` > `Convolution Reverb`
*   **Preset**: `Hall` > `Cathedral` OR `Weird` > `Drainpipe`.
*   **Director's Call**: "Let's try 'Cathedral' first... too realistic. Let's try 'Drainpipe'... Yes, that's the Rabbit Hole!"

## ACT_06_Mix_WetDry (干湿比调整)
*   **Param**:
    *   `Mix`: **60% Wet** (Very distant).
*   **Interaction**: Drag slider from 0% to 100% while playing. Stop at 60%.

## ACT_07_Stereo_Expand (立体声扩展)
*   **Menu**: `Effects` > `Stereo Imagery` > `Stereo Expander`
*   **Param**:
    *   `Stereo Expand`: **150%** (Artificial Wide).
*   **Center Channel**: Keep `Center Pan` at 0.

## ACT_Listen_Silence (深听：真空黑洞)
*   **Action**: Mute all tracks. Close eyes.
*   **Duration**: 30s.
*   **Goal**: Feel the "pressure" of absolute silence vs. room tone.
*   **Director's Call**: "Do you feel uncomfortable? Good. That's the void."

## ACT_Listen_Tail (深听：混响尾音)
*   **Action**: Play a short burst ("Hello?").
*   **Duration**: 45s.
*   **Goal**: Count the seconds until the sound completely vanishes.
*   **Director's Call**: "1... 2... 3... It's still there. That's the Reverb Tail."

## ACT_Listen_Width (深听：声场边缘)
*   **Action**: Use headphones. Toggle Stereo Expander On/Off.
*   **Duration**: 40s.
*   **Goal**: Use fingers to point to where the sound comes from.
*   **Director's Call**: "First it's between your eyes. Now... it's behind your ears."
