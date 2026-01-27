# 设计文档：Phase 4 合成质量保证系统

## 概述

本设计实现了一个全面的质量保证系统，用于验证、诊断和改进 Phase 4（定位）音频合成。系统基于 Python，集成了声学测量、频谱分析、立体声成像验证和心理声学评估功能。

**核心目标：**
1. 自动化验证 Phase 4 合成输出的质量
2. 诊断生成器脚本的逻辑错误和参数问题
3. 评估技术方法的实际可行性
4. 提供可操作的修复建议（代码级别）

**设计原则：**
- **模块化**：每个验证功能独立，可单独运行
- **可扩展**：易于添加新的验证指标
- **可解释**：提供详细的诊断信息和修复建议
- **集成性**：复用现有 IR 合成改进规范的声学验证函数

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│              Phase 4 QA System Architecture                  │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Audio Analysis Layer (音频分析层)                        │
│     ├─> Acoustic Metrics (T60, C80, EDT)                    │
│     ├─> Spectral Analysis (FFT, PSD, Centroid)              │
│     ├─> Stereo Imaging (Correlation, Width)                 │
│     └─> Artifact Detection (Clipping, DC, Discontinuity)    │
│                                                               │
│  2. Script Analysis Layer (脚本分析层)                       │
│     ├─> Parameter Extraction (AST parsing)                  │
│     ├─> Logic Validation (Processing order)                 │
│     └─> Algorithm Detection (Pink noise, convolution)       │
│                                                               │
│  3. Psychoacoustic Validation Layer (心理声学验证层)         │
│     ├─> Biofidelity Check (Heartbeat sine_sweep)           │
│     ├─> Threat Frequency Analysis (3000Hz detection)        │
│     └─> Spatial Separation (Inner vs Outer)                 │
│                                                               │
│  4. Reporting Layer (报告层)                                 │
│     ├─> Diagnostic Reports (Markdown + JSON)                │
│     ├─> Visualizations (Waveform, Spectrum, Stereo)         │
│     └─> Fix Recommendations (Code-level suggestions)        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## 组件和接口

### 组件 1：音频分析引擎 (AudioAnalyzer)

**职责**：分析音频文件的声学特性、频谱特征和立体声成像

**接口**：
```python
class AudioAnalyzer:
    def __init__(self, audio_path: str, sample_rate: int = 48000):
        """初始化音频分析器"""
        
    def measure_t60(self) -> float:
        """使用 Schroeder 积分测量 T60"""
        
    def measure_c80(self) -> float:
        """计算清晰度指数 C80"""
        
    def compute_stereo_correlation(self) -> float:
        """计算立体声相关系数"""
        
    def analyze_spectrum(self) -> Dict[str, np.ndarray]:
        """分析频谱特征（PSD, 频谱质心）"""
        
    def detect_artifacts(self) -> List[Artifact]:
        """检测削波、直流偏移、不连续性等伪影"""
```



**依赖**：
- 复用 IR 合成改进规范的声学验证函数（`measure_t60`, `measure_c80`, `measure_edt`）
- 使用 `scipy.signal` 进行频谱分析和滤波
- 使用 `numpy` 进行数值计算

### 组件 2：脚本分析引擎 (ScriptAnalyzer)

**职责**：分析生成器脚本的参数配置、处理逻辑和算法选择

**接口**:
```python
class ScriptAnalyzer:
    def __init__(self, script_path: str):
        """初始化脚本分析器"""
        
    def extract_parameters(self) -> Dict[str, Any]:
        """提取脚本中的关键参数（T60, 预延迟, 立体声宽度等）"""
        
    def validate_parameter_ranges(self) -> List[ParameterIssue]:
        """验证参数值是否在合理范围内"""
        
    def detect_algorithm_issues(self) -> List[AlgorithmIssue]:
        """检测算法选择问题（例如，朴素粉红噪音 vs Voss-McCartney）"""
        
    def validate_processing_order(self) -> List[OrderIssue]:
        """验证处理顺序的正确性"""
        
    def generate_fix_suggestions(self, issues: List[Issue]) -> List[FixSuggestion]:
        """生成代码级别的修复建议"""
```

**实现策略**：
- 使用 Python AST（抽象语法树）解析脚本
- 模式匹配识别关键参数和算法调用
- 基于规则的验证系统

### 组件 3：心理声学验证器 (PsychoacousticValidator)

**职责**：验证音频的心理声学设计是否达到预期效果

**接口**:
```python
class PsychoacousticValidator:
    def __init__(self, audio_path: str):
        """初始化心理声学验证器"""
        
    def validate_heartbeat_biofidelity(self) -> BiofidelityReport:
        """验证心跳的生物拟真性（sine_sweep, 低通滤波）"""
        
    def validate_threat_audio(self) -> ThreatReport:
        """验证威胁音频的心理效果（3000Hz, 尖锐包络）"""
        
    def validate_spatial_separation(self, tracks: Dict[str, str]) -> SpatialReport:
        """验证"内"（心跳）与"外"（威胁）的声像分离"""
        
    def assess_perceptual_impact(self) -> PerceptualReport:
        """评估感知影响（明亮度、黑暗度、焦虑值）"""
```

**参考设计**：
- 基于 `04_stereo_panning` 的心理声学设计原则
- 检测关键频率（3000Hz 对应婴儿哭声敏感频率）
- 验证包络曲线（高次幂制造尖锐突袭感）

### 组件 4：多轨混音验证器 (MultiTrackValidator)

**职责**：验证多轨混音的平衡、掩蔽和空间分布

**接口**:
```python
class MultiTrackValidator:
    def __init__(self, tracks: Dict[str, str]):
        """
        初始化多轨验证器
        
        Args:
            tracks: 轨道名称到文件路径的映射
                   例如 {'vocal': 'path/to/vocal.wav', 
                         'heartbeat': 'path/to/heartbeat.wav', ...}
        """
        
    def validate_level_balance(self) -> BalanceReport:
        """验证轨道间的相对电平平衡"""
        
    def detect_frequency_masking(self) -> List[MaskingIssue]:
        """检测频率掩蔽问题（特别是中心声像位置）"""
        
    def validate_stereo_imaging(self) -> StereoReport:
        """验证立体声成像（150% 虚空 vs 0% 心跳）"""
        
    def detect_mono_disaster(self) -> List[MonoIssue]:
        """检测"单声道灾难"问题（多个轨道在 Center 竞争相同频段）"""
```

### 组件 5：参考比较器 (ReferenceComparator)

**职责**：将合成输出与参考音频进行比较

**接口**:
```python
class ReferenceComparator:
    def __init__(self, test_audio: str, reference_audio: str):
        """初始化参考比较器"""
        
    def compute_spectral_similarity(self) -> float:
        """计算频谱相似度（0-1）"""
        
    def compute_stereo_correlation_diff(self) -> float:
        """计算立体声相关性差异"""
        
    def compute_rms_energy_diff(self) -> float:
        """计算 RMS 能量差异（dB）"""
        
    def generate_comparison_visualization(self) -> ComparisonViz:
        """生成并排比较可视化"""
```

### 组件 6：诊断报告生成器 (DiagnosticReporter)

**职责**：生成全面的诊断报告和可视化

**接口**:
```python
class DiagnosticReporter:
    def __init__(self, results: Dict[str, Any]):
        """初始化报告生成器"""
        
    def generate_markdown_report(self, output_path: str):
        """生成 Markdown 格式的人类可读报告"""
        
    def generate_json_report(self, output_path: str):
        """生成 JSON 格式的机器可读报告"""
        
    def generate_visualizations(self, output_dir: str):
        """生成可视化（波形、频谱图、立体声图）"""
        
    def prioritize_issues(self, issues: List[Issue]) -> List[Issue]:
        """按严重程度对问题进行优先级排序"""
```

### 组件 7：自动化测试套件 (TestSuite)

**职责**：协调所有验证组件，提供单一入口点

**接口**:
```python
class Phase4TestSuite:
    def __init__(self, config: TestConfig):
        """初始化测试套件"""
        
    def run_all_tests(self) -> TestResults:
        """运行所有验证测试"""
        
    def run_component_test(self, component: str) -> ComponentResults:
        """运行单个组件的测试"""
        
    def generate_summary_report(self) -> SummaryReport:
        """生成摘要报告（通过/失败状态）"""
```

## 数据模型

### 测试配置 (TestConfig)

```python
@dataclass
class TestConfig:
    """测试套件配置"""
    
    # 音频文件路径
    vocal_track: str
    heartbeat_track: str
    shadow_track: str
    void_ir_track: str
    final_mix: Optional[str] = None
    reference_audio: Optional[str] = None
    
    # 生成器脚本路径
    generator_script: Optional[str] = None
    
    # 验证阈值
    t60_tolerance: float = 0.1  # ±10%
    stereo_correlation_threshold: float = 0.05
    snr_threshold: float = 6.0  # dB
    
    # 输出配置
    output_dir: str = "./qa_reports"
    generate_visualizations: bool = True
```

### 验证结果 (ValidationResult)

```python
@dataclass
class ValidationResult:
    """单个验证测试的结果"""
    
    test_name: str
    passed: bool
    measured_value: Any
    expected_value: Any
    tolerance: Optional[float] = None
    message: str = ""
    severity: str = "info"  # "info", "warning", "error", "critical"
```

### 问题报告 (Issue)

```python
@dataclass
class Issue:
    """检测到的问题"""
    
    issue_type: str  # "parameter", "algorithm", "artifact", "masking", etc.
    severity: str  # "low", "medium", "high", "critical"
    location: str  # 文件路径或时间位置
    description: str
    fix_suggestion: Optional[str] = None
    code_snippet: Optional[str] = None  # 代码级别的修复建议
```

### 声学指标 (AcousticMetrics)

```python
@dataclass
class AcousticMetrics:
    """声学测量指标"""
    
    t60: Optional[float] = None
    edt: Optional[float] = None
    c80: Optional[float] = None
    pre_delay_ms: Optional[float] = None
    stereo_correlation: Optional[float] = None
    stereo_width_percent: Optional[float] = None
    rms_energy_db: Optional[float] = None
    peak_amplitude: Optional[float] = None
    lufs: Optional[float] = None
    spectral_centroid_hz: Optional[float] = None
```

### 频谱分析结果 (SpectralAnalysis)

```python
@dataclass
class SpectralAnalysis:
    """频谱分析结果"""
    
    frequencies: np.ndarray
    psd: np.ndarray  # 功率谱密度
    octave_band_energy: Dict[str, float]  # 八度频段能量
    spectral_centroid: float
    spectral_rolloff: float
    dominant_frequencies: List[float]
```

### 伪影检测结果 (ArtifactReport)

```python
@dataclass
class ArtifactReport:
    """伪影检测报告"""
    
    has_clipping: bool
    clipping_locations: List[float]  # 时间位置（秒）
    has_dc_offset: bool
    dc_offset_value: float
    has_discontinuities: bool
    discontinuity_locations: List[float]
    has_aliasing: bool
```

## 正确性属性

*属性是一种特征或行为，应该在系统的所有有效执行中保持为真——本质上是关于系统应该做什么的正式陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*


### 属性反思

在完成预工作分析后，我需要识别和消除冗余属性：

**冗余分析**：
1. **T60 测量和验证**：需求 4.1（测量 T60）和 4.2（验证 T60 在范围内）可以合并为一个属性
2. **立体声相关性计算和验证**：需求 2.1（计算相关系数）、2.2（验证虚空 IR）、2.3（验证心跳）可以合并为一个综合属性
3. **伪影检测**：需求 6.1-6.4（检测各种伪影）和 6.5（报告位置）可以合并为一个属性
4. **参数提取和验证**：需求 14.1（提取参数）和 14.2（验证范围）可以合并
5. **往返验证**：需求 13.1（位相同）和 13.2（声学等效）实际上是同一个属性的不同容差级别

**保留的核心属性**：
- 组件隔离测试（每个轨道独立验证）
- 立体声成像验证（综合相关性和宽度）
- 频谱分析和掩蔽检测
- 混响质量验证（T60, C80, EDT 综合）
- 混音平衡验证
- 伪影检测（综合所有类型）
- 参考比较
- 脚本逻辑诊断（参数和算法）
- 心理声学验证
- 往返验证（确定性）

### 属性 1：组件隔离验证

*对于任意* Phase 4 轨道（人声、心跳、影子、虚空 IR），QA 系统应该能够独立验证该轨道的声学特性，并且验证结果不受其他轨道的影响

**验证：需求 1.1, 1.2, 1.3, 1.4**

### 属性 2：立体声成像一致性

*对于任意* 立体声音频文件，计算的立体声相关系数应该在 [-1, 1] 范围内，并且：
- 如果音频是单声道或居中定位，相关系数应该 > 0.95
- 如果音频是宽立体声（150%），相关系数应该 < 0.5
- 系统应该能够正确识别和报告不符合要求的轨道

**验证：需求 2.1, 2.2, 2.3, 2.5**

### 属性 3：频谱掩蔽检测

*对于任意* 多轨混音，如果两个或多个轨道在相同频段（±100Hz）和相同声像位置（±10%）竞争能量，系统应该检测到潜在的频率掩蔽问题，并报告涉及的轨道和频段

**验证：需求 3.2, 3.3, 3.6**

### 属性 4：混响质量综合验证

*对于任意* 脉冲响应，系统应该能够测量 T60、EDT 和 C80，并且：
- 测量的 T60 应该在目标值的 ±10% 范围内
- 如果 IR 具有频率相关衰减，高频 T60 应该小于低频 T60
- C80 值应该与空间类型一致（遥远空间 < -5dB，近距离空间 > 0dB）

**验证：需求 4.1, 4.2, 4.3, 4.4, 4.5**

### 属性 5：混音平衡验证

*对于任意* 多轨混音，系统应该能够计算每个轨道的 RMS 能量，并且：
- 如果心跳轨道的 SNR（相对于虚空 IR）< 6dB，系统应该发出警告
- 人声轨道应该具有最高的 RMS 能量
- 如果影子自我轨道的 RMS 能量超过人声的 80%，系统应该发出警告

**验证：需求 5.1, 5.2, 5.3, 5.4**

### 属性 6：伪影综合检测

*对于任意* 音频文件，系统应该能够检测以下伪影，并报告其位置（时间）和严重程度：
- 削波（样本值 ≥ 0.99 或 ≤ -0.99）
- 直流偏移（|平均值| > 0.01）
- 不连续性（相邻样本差 > 0.1）
- 混叠（高频能量 > Nyquist 频率的 90%）

**验证：需求 6.1, 6.2, 6.3, 6.4, 6.5**

### 属性 7：参考比较一致性

*对于任意* 测试音频和参考音频对，系统应该能够计算：
- 频谱相似度（0-1，基于 PSD 相关性）
- 立体声相关性差异（绝对值）
- RMS 能量差异（dB）
并且如果任何差异超过 20%，系统应该标记为显著偏差

**验证：需求 7.1, 7.2, 7.3, 7.4**

### 属性 8：脚本参数验证

*对于任意* 生成器脚本，系统应该能够提取关键参数（T60, 预延迟, 立体声宽度, 混音比例），并且：
- 检测参数值是否在合理范围内（例如，T60 应为 0.1-10s）
- 如果参数异常，提供具体的修正建议（例如，"将 T60 从 2.5s 增加到 6.0s"）

**验证：需求 14.1, 14.2, 14.3**

### 属性 9：算法检测

*对于任意* 生成器脚本，系统应该能够检测：
- 是否使用 Voss-McCartney 粉红噪音算法（而不是朴素 FFT 方法）
- 是否正确实现频率相关衰减
- 处理顺序是否正确（例如，卷积应在立体声扩展之前）

**验证：需求 10.3, 10.4, 14.4, 14.5**

### 属性 10：心理声学特征检测

*对于任意* 心跳音频，系统应该能够检测：
- 是否使用 sine_sweep 模拟肌肉收缩（检测频率扫描特征）
- 是否应用低通滤波器（检测高频衰减 > 20dB @ 500Hz）

*对于任意* 威胁音频，系统应该能够检测：
- 是否包含 3000Hz 频率成分（±200Hz 范围内的能量峰值）
- 包络曲线是否使用高次幂（检测尖锐突袭特征）

**验证：需求 11.6, 11.8, 16.1, 16.2, 16.3, 16.4**

### 属性 11：空间分离验证

*对于任意* 多轨混音，系统应该能够验证：
- "内"（心跳）轨道的立体声相关性 > 0.95（居中）
- "外"（虚空 IR）轨道的立体声相关性 < 0.5（宽立体声）
- 两者之间的声像分离度 > 0.4（相关性差异）

**验证：需求 16.5**

### 属性 12：往返确定性

*对于任意* Phase 4 组件，如果使用固定随机种子生成两次，输出应该：
- 位相同（字节级别完全一致），或
- 声学等效（T60, C80, 立体声相关性等指标在 ±1% 容差范围内）

**验证：需求 13.1, 13.2, 13.3, 13.5**

### 属性 13：卷积无双重干信号

*对于任意* 脉冲响应和干信号，卷积输出应该只包含一个直达声峰值（在 IR 的预延迟位置），而不是两个峰值（一个在 t=0，一个在预延迟位置）

**验证：需求 1.5**

### 属性 14：频谱特征差异

*对于任意* 影子自我轨道和人声轨道，两者的频谱质心差异应该 > 500Hz，或者八度频段能量分布的相关性 < 0.7，以确保它们具有不同的频谱特征

**验证：需求 3.4**

### 属性 15：感知质量指标计算

*对于任意* 音频文件，系统应该能够计算：
- LUFS 响度（应在 -40 到 0 LUFS 范围内）
- 峰值因数（应在 3-20 dB 范围内）
- 频谱质心（应在 20-20000 Hz 范围内）
- 感知立体声宽度（应在 0-200% 范围内）

**验证：需求 11.1, 11.2, 11.3, 11.4**

## 错误处理

### 错误类型

1. **文件不存在错误**
   - 检测：在加载音频文件前验证文件存在
   - 处理：返回清晰的错误消息，指出缺失的文件路径
   - 恢复：提供文件路径建议（基于常见位置）

2. **音频格式错误**
   - 检测：验证采样率、位深度、声道数
   - 处理：报告期望格式和实际格式
   - 恢复：提供格式转换建议

3. **参数范围错误**
   - 检测：验证所有参数在合理范围内
   - 处理：报告异常参数和合理范围
   - 恢复：提供修正建议

4. **计算失败错误**
   - 检测：捕获数值计算异常（除零、溢出等）
   - 处理：记录详细的错误上下文
   - 恢复：使用默认值或跳过该指标

5. **脚本解析错误**
   - 检测：AST 解析失败或无法识别的代码模式
   - 处理：报告解析失败的位置和原因
   - 恢复：提供部分分析结果

### 错误报告格式

```python
@dataclass
class QAError:
    """QA 系统错误"""
    
    error_type: str  # "file_not_found", "format_error", "parameter_error", etc.
    severity: str  # "warning", "error", "critical"
    message: str
    location: str  # 文件路径或代码位置
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
```

### 错误处理策略

- **快速失败**：对于关键错误（文件不存在、格式错误），立即停止并报告
- **优雅降级**：对于非关键错误（单个指标计算失败），记录警告并继续
- **详细日志**：所有错误都应记录到日志文件，包含完整的上下文信息
- **用户友好**：错误消息应该清晰、可操作，避免技术术语

## 测试策略

### 双重测试方法

本 QA 系统采用单元测试和属性测试的组合：

- **单元测试**：验证特定示例、边缘情况和错误条件
- **属性测试**：验证跨所有输入的通用属性
- 两者互补，共同提供全面覆盖

### 单元测试

**重点领域**：
- 特定示例（例如，已知 T60 的 IR）
- 边缘情况（空文件、极短/极长音频）
- 错误条件（无效格式、缺失文件）
- 集成点（组件之间的交互）

**示例单元测试**：
```python
def test_measure_t60_known_ir():
    """测试 T60 测量的准确性（已知 IR）"""
    # 生成已知 T60 = 2.0s 的 IR
    ir = generate_test_ir(t60=2.0, sample_rate=48000)
    analyzer = AudioAnalyzer(ir, sample_rate=48000)
    measured_t60 = analyzer.measure_t60()
    
    # 验证测量值在 ±10% 范围内
    assert 1.8 <= measured_t60 <= 2.2

def test_detect_clipping():
    """测试削波检测"""
    # 生成有削波的音频
    audio = np.array([0.5, 0.8, 1.0, 1.0, 0.9, 0.6])
    analyzer = AudioAnalyzer(audio, sample_rate=48000)
    artifacts = analyzer.detect_artifacts()
    
    # 验证检测到削波
    assert any(a.type == "clipping" for a in artifacts)
    assert artifacts[0].location == [2, 3]  # 样本索引
```

### 属性测试

**配置**：
- 使用 `hypothesis` 库（Python）
- 每个属性测试运行 **最少 100 次迭代**
- 每个测试必须引用设计文档中的属性

**标签格式**：
```python
# Feature: phase4-synthesis-qa, Property 2: 立体声成像一致性
# 对于任意立体声音频文件，计算的立体声相关系数应该在 [-1, 1] 范围内
```

**示例属性测试**：
```python
from hypothesis import given, strategies as st
import hypothesis.extra.numpy as npst

# Feature: phase4-synthesis-qa, Property 2: 立体声成像一致性
@given(
    left=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000)),
    right=npst.arrays(dtype=np.float32, shape=st.integers(1000, 10000))
)
def test_stereo_correlation_range(left, right):
    """属性：立体声相关系数应该在 [-1, 1] 范围内"""
    # 确保左右声道长度相同
    min_len = min(len(left), len(right))
    left = left[:min_len]
    right = right[:min_len]
    
    # 创建立体声音频
    stereo = np.stack([left, right], axis=1)
    analyzer = AudioAnalyzer(stereo, sample_rate=48000)
    
    # 计算立体声相关系数
    correlation = analyzer.compute_stereo_correlation()
    
    # 验证范围
    assert -1.0 <= correlation <= 1.0

# Feature: phase4-synthesis-qa, Property 4: 混响质量综合验证
@given(
    t60_target=st.floats(min_value=0.5, max_value=8.0),
    sample_rate=st.sampled_from([44100, 48000, 96000])
)
def test_t60_measurement_accuracy(t60_target, sample_rate):
    """属性：测量的 T60 应该在目标值的 ±10% 范围内"""
    # 生成已知 T60 的 IR
    ir = generate_test_ir(t60=t60_target, sample_rate=sample_rate)
    analyzer = AudioAnalyzer(ir, sample_rate=sample_rate)
    
    # 测量 T60
    measured_t60 = analyzer.measure_t60()
    
    # 验证在 ±10% 范围内
    tolerance = t60_target * 0.1
    assert abs(measured_t60 - t60_target) <= tolerance
```

### 集成测试

**测试场景**：
1. **完整 Phase 4 管道**：生成所有轨道 → 验证每个轨道 → 混音 → 验证最终混音
2. **脚本分析管道**：解析脚本 → 提取参数 → 验证参数 → 生成修复建议
3. **参考比较管道**：加载参考音频 → 加载测试音频 → 计算相似度 → 生成报告

**示例集成测试**：
```python
def test_full_phase4_pipeline():
    """集成测试：完整 Phase 4 验证管道"""
    # 1. 生成所有轨道
    generator = Phase4Generator(config=test_config)
    tracks = generator.generate_all_tracks()
    
    # 2. 验证每个轨道
    suite = Phase4TestSuite(config=test_config)
    results = suite.run_all_tests()
    
    # 3. 验证所有测试通过
    assert all(r.passed for r in results.component_tests)
    
    # 4. 验证生成了报告
    assert os.path.exists(results.report_path)
```

### 测试覆盖率目标

- **代码覆盖率**：≥ 85%
- **属性覆盖率**：每个设计属性至少有一个属性测试
- **边缘情况覆盖率**：每个错误类型至少有一个单元测试

### 测试执行

**本地开发**：
```bash
# 运行所有测试
pytest tests/

# 运行属性测试（更多迭代）
pytest tests/ --hypothesis-iterations=1000

# 运行特定测试
pytest tests/test_audio_analyzer.py::test_measure_t60_known_ir
```

**CI/CD 集成**：
- 每次提交自动运行所有测试
- 属性测试使用 100 次迭代（快速反馈）
- 每日构建使用 1000 次迭代（深度验证）

### 性能测试

**目标**：
- 完整测试套件应在 60 秒内完成
- 单个轨道验证应在 5 秒内完成
- 脚本分析应在 2 秒内完成

**性能测试**：
```python
import time

def test_full_suite_performance():
    """性能测试：完整测试套件应在 60 秒内完成"""
    suite = Phase4TestSuite(config=test_config)
    
    start_time = time.time()
    results = suite.run_all_tests()
    elapsed_time = time.time() - start_time
    
    assert elapsed_time < 60.0, f"测试套件耗时 {elapsed_time:.1f}s，超过 60s 限制"
```

## 依赖项

### 必需库

```python
# 音频处理
numpy>=1.20.0
scipy>=1.7.0
soundfile>=0.10.0

# 属性测试
hypothesis>=6.0.0

# 数据处理
dataclasses  # Python 3.7+

# 可视化（可选）
matplotlib>=3.3.0

# 测试
pytest>=6.0.0
pytest-cov>=2.10.0
```

### 外部依赖

- **IR 合成改进规范**：复用声学验证函数（`measure_t60`, `measure_c80`, `measure_edt`）
- **Python 3.8+**：使用 dataclasses 和类型提示
- **48kHz 音频文件**：所有测试音频应使用 48kHz 采样率

## 向后兼容性

- **文件格式**：保持与现有生成器脚本的兼容性（48kHz, 16-bit PCM, WAV）
- **API**：QA 系统是独立的，不修改现有生成器脚本
- **报告格式**：Markdown 和 JSON 格式，易于集成到现有工作流

## 性能考虑

- **并行处理**：可以并行验证多个轨道（使用 `multiprocessing`）
- **缓存**：缓存 FFT 结果和频谱分析，避免重复计算
- **增量验证**：只验证修改过的轨道，跳过未修改的轨道
- **可选可视化**：可视化生成是可选的，可以禁用以提高速度

## 文档更新

1. **README.md**：添加 QA 系统使用指南
2. **API 文档**：为所有公共类和函数添加 docstrings
3. **示例**：提供完整的使用示例和教程
4. **故障排除**：常见问题和解决方案

## 成功标准

1. ✅ 所有属性测试通过（100 次迭代）
2. ✅ 所有单元测试通过
3. ✅ 代码覆盖率 ≥ 85%
4. ✅ 完整测试套件在 60 秒内完成
5. ✅ 生成清晰、可操作的诊断报告
6. ✅ 与现有 IR 合成改进规范集成
7. ✅ 文档完整，易于使用
