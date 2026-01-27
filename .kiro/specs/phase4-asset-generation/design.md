# 设计文档：Phase 4 音频素材生成器

## 概述

本设计实现了一个完整的音频素材生成器，用于生成爱丽丝声音剧场项目 Phase 4（定位 - 镜中双生）所需的所有音频轨道。生成器基于 Python，集成了声学处理、心理声学设计和自动化验证功能。

**核心目标：**
1. 生成 4 个符合设计规范的音频轨道
2. 确保声学指标符合要求（立体声宽度、T60、频谱特征）
3. 创造预期的心理声学效果（"恐惧"而非"滑稽"）
4. 提供自动化验证和详细报告

**设计原则：**
- **模块化**：每个轨道的生成逻辑独立
- **可配置**：所有参数通过配置文件调整
- **可验证**：集成 QA 系统进行自动验证
- **可重复**：使用固定随机种子确保一致性

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│         Phase 4 Asset Generation Architecture                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Configuration Layer (配置层)                             │
│     └─> YAML/JSON 配置文件                                   │
│                                                               │
│  2. Track Generation Layer (轨道生成层)                      │
│     ├─> Track 1: Voice Processor (人声处理器)               │
│     ├─> Track 2: Heartbeat Generator (心跳生成器)           │
│     ├─> Track 3: Shadow Generator (影子生成器)              │
│     └─> Track 4: Void Expander (虚空扩展器)                 │
│                                                               │
│  3. Audio Processing Layer (音频处理层)                      │
│     ├─> Noise Reduction (降噪)                              │
│     ├─> Time Stretching (时间拉伸)                          │
│     ├─> Pitch Shifting (音高调整)                           │
│     ├─> Convolution Reverb (卷积混响)                       │
│     └─> Stereo Expansion (立体声扩展)                       │
│                                                               │
│  4. Validation Layer (验证层)                                │
│     ├─> Acoustic Metrics (声学指标)                         │
│     ├─> Psychoacoustic Validation (心理声学验证)            │
│     └─> QA System Integration (QA 系统集成)                 │
│                                                               │
│  5. Reporting Layer (报告层)                                 │
│     └─> Markdown Report Generator (报告生成器)              │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 组件和接口

### 组件 1：配置管理器 (ConfigManager)

**职责**：加载和验证配置参数

**接口**：
```python
class Phase4Config:
    """Phase 4 生成配置"""
    
    # 全局配置
    sample_rate: int = 48000
    duration_sec: float = 10.0
    random_seed: int = 42
    output_dir: str = "_Library/S05_Position"
    
    # Track 1: Voice
    voice_input_path: str = "_Library/S0X_Shared/asset_S0X_dry_voice_clean.wav"
    voice_noise_reduction: float = 75.0  # %
    voice_noise_reduce_by: float = 35.0  # dB
    voice_stretch: float = 135.0  # %
    voice_pitch_shift: int = -4  # semitones
    voice_reverb_mix: float = 75.0  # %
    voice_room_size: float = 150.0  # %
    
    # Track 2: Heartbeat
    heartbeat_bpm: int = 60
    heartbeat_lpf_cutoff: float = 500.0  # Hz
    
    # Track 3: Shadow
    shadow_voice_mix: float = 60.0  # %
    shadow_tick_mix: float = 40.0  # %
    shadow_tick_start_interval: float = 0.5  # seconds
    shadow_tick_slowdown_factor: float = 1.15
    
    # Track 4: Void
    void_ir_path: str = "_Library/S04_Space/asset_S04_void_ir.wav"
    void_stereo_width: float = 175.0  # % (150-200)
    
    # Validation
    enable_qa: bool = True
    quick_mode: bool = False

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置管理器"""
        
    def load_config(self) -> Phase4Config:
        """加载配置文件或使用默认配置"""
        
    def validate_config(self, config: Phase4Config) -> List[str]:
        """验证配置参数的合理性"""
        
    def save_config(self, config: Phase4Config, path: str):
        """保存配置到文件"""
```

### 组件 2：Track 1 - 人声处理器 (VoiceProcessor)

**职责**：处理干净人声，应用 Phase 1-3 的所有效果

**接口**：
```python
class VoiceProcessor:
    def __init__(self, config: Phase4Config):
        """初始化人声处理器"""
        
    def load_voice(self, path: str) -> np.ndarray:
        """加载干净人声"""
        
    def apply_noise_reduction(self, audio: np.ndarray, 
                               reduction_pct: float, 
                               reduce_by_db: float) -> np.ndarray:
        """应用降噪处理（Phase 1）"""
        
    def apply_time_stretch(self, audio: np.ndarray, 
                           stretch_pct: float) -> np.ndarray:
        """应用时间拉伸（Phase 2）"""
        
    def apply_pitch_shift(self, audio: np.ndarray, 
                          semitones: int) -> np.ndarray:
        """应用音高调整（Phase 2）"""
        
    def apply_convolution_reverb(self, audio: np.ndarray, 
                                  ir_path: str, 
                                  mix_pct: float, 
                                  room_size_pct: float) -> np.ndarray:
        """应用卷积混响（Phase 3）"""
        
    def process(self) -> np.ndarray:
        """执行完整的人声处理流程"""
```

**实现策略**：
- 降噪：使用频谱减法（Spectral Subtraction）
- 时间拉伸：使用 librosa 的 time_stretch 或 scipy 的 resample
- 音高调整：使用 librosa 的 pitch_shift 或频域处理
- 卷积混响：使用 scipy.signal.fftconvolve

### 组件 3：Track 2 - 心跳生成器 (HeartbeatGenerator)

**职责**：生成生物拟真的内脏心跳音频

**接口**：
```python
class HeartbeatGenerator:
    def __init__(self, config: Phase4Config):
        """初始化心跳生成器"""
        
    def generate_single_beat(self, fs: int) -> np.ndarray:
        """
        生成单次心跳（Lub-Dub）
        
        使用 sine_sweep 模拟肌肉收缩：
        - Lub: 90Hz -> 40Hz, 持续 0.1s
        - Dub: 70Hz -> 30Hz, 持续 0.08s, 延迟 0.15s
        """
        
    def apply_bone_conduction_filter(self, audio: np.ndarray, 
                                      cutoff_hz: float) -> np.ndarray:
        """应用低通滤波器模拟骨传导的沉闷感"""
        
    def generate(self) -> np.ndarray:
        """生成完整的心跳序列"""
```

**实现策略**：
- 使用 sine_sweep（频率扫描）模拟心肌收缩
- 应用低通滤波器（Butterworth, 4阶）模拟骨传导
- 确保单声道输出（立体声相关性 = 1.0）

### 组件 4：Track 3 - 影子生成器 (ShadowGenerator)

**职责**：生成反向人声 + 减慢滴答声的混合音频

**接口**：
```python
class ShadowGenerator:
    def __init__(self, config: Phase4Config):
        """初始化影子生成器"""
        
    def reverse_voice(self, audio: np.ndarray) -> np.ndarray:
        """反向播放人声"""
        
    def generate_slowing_tick(self, duration_sec: float, 
                               fs: int) -> np.ndarray:
        """
        生成逐渐变慢的滴答声
        
        特征：
        - 起始间隔 0.5s（120 BPM）
        - 每次间隔增加 15%
        - 带通滤波 2500-3500Hz（金属机械声）
        """
        
    def mix_shadow(self, voice: np.ndarray, 
                   tick: np.ndarray, 
                   voice_mix: float, 
                   tick_mix: float) -> np.ndarray:
        """混合反向人声和滴答声"""
        
    def generate(self) -> np.ndarray:
        """生成完整的影子自我音频"""
```

**实现策略**：
- 反向人声：简单的数组反转 `audio[::-1]`
- 滴答声：短脉冲 + 带通滤波器（Butterworth, 4阶）
- 混合：加权和，确保两者都清晰可听

### 组件 5：Track 4 - 虚空扩展器 (VoidExpander)

**职责**：加载虚空 IR 并应用立体声扩展

**接口**：
```python
class VoidExpander:
    def __init__(self, config: Phase4Config):
        """初始化虚空扩展器"""
        
    def load_void_ir(self, path: str) -> np.ndarray:
        """加载虚空 IR"""
        
    def apply_stereo_expansion(self, audio: np.ndarray, 
                                width_pct: float) -> np.ndarray:
        """
        应用立体声扩展（Mid-Side 处理）
        
        算法：
        1. 分离 Mid 和 Side 信号
        2. 调整 Side 信号增益
        3. 重新组合
        
        width_pct:
        - 100%: 正常立体声
        - 150%: Side 增益 +3dB
        - 200%: Side 增益 +6dB
        """
        
    def generate(self) -> np.ndarray:
        """生成扩展后的虚空环境音频"""
```

**实现策略**：
- Mid-Side 处理：
  - Mid = (L + R) / 2
  - Side = (L - R) / 2
  - 调整 Side 增益
  - L' = Mid + Side * gain
  - R' = Mid - Side * gain
- 验证立体声相关性 < 0.5

### 组件 6：混音器 (Mixer)

**职责**：混合 4 个轨道生成最终混音

**接口**：
```python
class Mixer:
    def __init__(self, config: Phase4Config):
        """初始化混音器"""
        
    def align_tracks(self, tracks: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """对齐所有轨道的长度"""
        
    def apply_mix_levels(self, tracks: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        应用混音电平
        
        建议比例：
        - Voice: 0 dB (参考)
        - Heart: -6 dB (可听但不压制)
        - Shadow: -12 dB (背景)
        - Void: -9 dB (环境)
        """
        
    def mix(self, tracks: Dict[str, np.ndarray]) -> np.ndarray:
        """混合所有轨道"""
        
    def normalize(self, audio: np.ndarray, target_peak: float = 0.95) -> np.ndarray:
        """归一化混音，防止削波"""
```

### 组件 7：验证器 (Validator)

**职责**：验证生成的素材是否符合声学要求

**接口**：
```python
class Phase4Validator:
    def __init__(self, config: Phase4Config):
        """初始化验证器"""
        
    def validate_heartbeat(self, audio: np.ndarray) -> ValidationResult:
        """
        验证心跳音频
        - 立体声相关性 > 0.95
        - 高频衰减 > 20dB @ 500Hz
        """
        
    def validate_shadow(self, audio: np.ndarray) -> ValidationResult:
        """
        验证影子音频
        - 包含 3000Hz 频率成分
        - 滴答声清晰可辨
        """
        
    def validate_void(self, audio: np.ndarray) -> ValidationResult:
        """
        验证虚空音频
        - 立体声相关性 < 0.5
        - T60 ≥ 5.0s
        """
        
    def validate_mix(self, audio: np.ndarray, tracks: Dict[str, np.ndarray]) -> ValidationResult:
        """
        验证最终混音
        - 无削波
        - 心跳 SNR ≥ 6dB
        """
        
    def generate_report(self, results: Dict[str, ValidationResult]) -> str:
        """生成 Markdown 格式的验证报告"""
```

**集成 QA 系统**：
- 复用 `phase4-synthesis-qa` 的声学验证函数
- 使用相同的数据模型和验证逻辑

### 组件 8：主生成器 (Phase4Generator)

**职责**：协调所有组件，执行完整的生成流程

**接口**：
```python
class Phase4Generator:
    def __init__(self, config_path: Optional[str] = None):
        """初始化生成器"""
        
    def generate_all_tracks(self) -> Dict[str, np.ndarray]:
        """生成所有 4 个轨道"""
        
    def generate_final_mix(self, tracks: Dict[str, np.ndarray]) -> np.ndarray:
        """生成最终混音"""
        
    def validate_outputs(self, tracks: Dict[str, np.ndarray]) -> Dict[str, ValidationResult]:
        """验证所有输出"""
        
    def save_outputs(self, tracks: Dict[str, np.ndarray]):
        """保存所有输出文件"""
        
    def run(self):
        """执行完整的生成流程"""
```

## 数据模型

### 配置模型

```python
@dataclass
class Phase4Config:
    """Phase 4 生成配置（见组件 1）"""
    pass
```

### 验证结果模型

```python
@dataclass
class ValidationResult:
    """验证结果"""
    
    track_name: str
    passed: bool
    metrics: Dict[str, float]  # 测量的指标
    issues: List[str]  # 发现的问题
    suggestions: List[str]  # 修复建议
```

## 算法细节

### 立体声扩展算法（Mid-Side 处理）

```python
def expand_stereo_midside(stereo_audio, width_pct):
    """
    Mid-Side 立体声扩展
    
    参数:
        stereo_audio: (N, 2) 立体声数组
        width_pct: 立体声宽度百分比（100 = 正常，150 = 扩展）
    
    返回:
        扩展后的立体声数组
    """
    L = stereo_audio[:, 0]
    R = stereo_audio[:, 1]
    
    # 分离 Mid 和 Side
    Mid = (L + R) / 2
    Side = (L - R) / 2
    
    # 计算 Side 增益
    # width_pct = 100: gain = 1.0 (正常)
    # width_pct = 150: gain = 1.5 (扩展 50%)
    # width_pct = 200: gain = 2.0 (扩展 100%)
    side_gain = width_pct / 100.0
    
    # 重新组合
    L_new = Mid + Side * side_gain
    R_new = Mid - Side * side_gain
    
    # 归一化防止削波
    max_val = max(np.max(np.abs(L_new)), np.max(np.abs(R_new)))
    if max_val > 1.0:
        L_new /= max_val
        R_new /= max_val
    
    return np.stack([L_new, R_new], axis=1)
```

### 降噪算法（频谱减法）

```python
def spectral_subtraction(audio, noise_profile, reduction_pct, reduce_by_db):
    """
    频谱减法降噪
    
    参数:
        audio: 输入音频
        noise_profile: 噪音频谱（从纯噪音段采样）
        reduction_pct: 降噪百分比（0-100）
        reduce_by_db: 降噪量（dB）
    
    返回:
        降噪后的音频
    """
    # 转换为频域
    fft_audio = np.fft.rfft(audio)
    fft_noise = np.fft.rfft(noise_profile)
    
    # 计算噪音幅度
    noise_mag = np.abs(fft_noise)
    
    # 计算减法系数
    alpha = (reduction_pct / 100.0) * (10 ** (reduce_by_db / 20.0))
    
    # 频谱减法
    audio_mag = np.abs(fft_audio)
    audio_phase = np.angle(fft_audio)
    
    # 减去噪音（保证非负）
    clean_mag = np.maximum(audio_mag - alpha * noise_mag, 0)
    
    # 重建信号
    clean_fft = clean_mag * np.exp(1j * audio_phase)
    clean_audio = np.fft.irfft(clean_fft, n=len(audio))
    
    return clean_audio
```

## 错误处理

### 错误类型

1. **文件不存在错误**
   - 检测：验证输入文件路径
   - 处理：输出清晰的错误信息
   - 恢复：提供文件路径建议

2. **音频格式错误**
   - 检测：验证采样率、位深度、声道数
   - 处理：输出期望格式和实际格式
   - 恢复：提供格式转换建议

3. **参数范围错误**
   - 检测：验证配置参数
   - 处理：输出异常参数和合理范围
   - 恢复：使用默认值

4. **处理失败错误**
   - 检测：捕获处理异常
   - 处理：记录详细的错误上下文
   - 恢复：跳过该步骤或使用备用方法

## 性能优化

- **并行处理**：使用 multiprocessing 并行生成多个轨道
- **缓存**：缓存卷积结果，避免重复计算
- **快速模式**：跳过验证步骤，只生成音频

## 依赖项

```python
# 音频处理
numpy>=1.20.0
scipy>=1.7.0
soundfile>=0.10.0
librosa>=0.9.0  # 用于时间拉伸和音高调整

# 配置管理
pyyaml>=5.4.0

# 验证（复用 QA 系统）
# 从 phase4-synthesis-qa 导入验证函数
```

## 成功标准

1. ✅ 生成所有 4 个轨道，符合设计规范
2. ✅ 所有声学指标验证通过
3. ✅ 心理声学效果符合预期（"恐惧"而非"滑稽"）
4. ✅ 生成时间 < 30 秒
5. ✅ 输出文件格式正确（48kHz, 16-bit PCM）
6. ✅ 生成详细的验证报告
7. ✅ 可重复性（固定随机种子）
