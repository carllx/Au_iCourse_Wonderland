"""
配置文件和数据模型定义
=====================

定义 QA 系统的配置参数、数据模型和常量。
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
import numpy as np


# ============================================================================
# 测试配置
# ============================================================================

@dataclass
class TestConfig:
    """测试套件配置"""
    
    # 音频文件路径
    vocal_track: Optional[str] = None
    heartbeat_track: Optional[str] = None
    shadow_track: Optional[str] = None
    void_ir_track: Optional[str] = None
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
    
    # 采样率
    sample_rate: int = 48000


# ============================================================================
# 验证结果
# ============================================================================

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
    
    def __str__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status} | {self.test_name}: {self.message}"


# ============================================================================
# 问题报告
# ============================================================================

@dataclass
class Issue:
    """检测到的问题"""
    
    issue_type: str  # "parameter", "algorithm", "artifact", "masking", etc.
    severity: str  # "low", "medium", "high", "critical"
    location: str  # 文件路径或时间位置
    description: str
    fix_suggestion: Optional[str] = None
    code_snippet: Optional[str] = None  # 代码级别的修复建议
    
    def __str__(self):
        severity_icon = {
            "low": "ℹ️",
            "medium": "⚠️",
            "high": "❌",
            "critical": "🔥"
        }
        icon = severity_icon.get(self.severity, "•")
        return f"{icon} [{self.severity.upper()}] {self.issue_type}: {self.description}"


# ============================================================================
# 声学指标
# ============================================================================

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
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "t60": self.t60,
            "edt": self.edt,
            "c80": self.c80,
            "pre_delay_ms": self.pre_delay_ms,
            "stereo_correlation": self.stereo_correlation,
            "stereo_width_percent": self.stereo_width_percent,
            "rms_energy_db": self.rms_energy_db,
            "peak_amplitude": self.peak_amplitude,
            "lufs": self.lufs,
            "spectral_centroid_hz": self.spectral_centroid_hz
        }


# ============================================================================
# 频谱分析结果
# ============================================================================

@dataclass
class SpectralAnalysis:
    """频谱分析结果"""
    
    frequencies: np.ndarray
    psd: np.ndarray  # 功率谱密度
    octave_band_energy: Dict[str, float]  # 八度频段能量
    spectral_centroid: float
    spectral_rolloff: float
    dominant_frequencies: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式（不包含大数组）"""
        return {
            "octave_band_energy": self.octave_band_energy,
            "spectral_centroid": self.spectral_centroid,
            "spectral_rolloff": self.spectral_rolloff,
            "dominant_frequencies": self.dominant_frequencies
        }


# ============================================================================
# 伪影检测结果
# ============================================================================

@dataclass
class ArtifactReport:
    """伪影检测报告"""
    
    has_clipping: bool
    has_dc_offset: bool
    has_discontinuities: bool
    has_aliasing: bool
    clipping_locations: List[float] = field(default_factory=list)  # 时间位置（秒）
    dc_offset_value: float = 0.0
    discontinuity_locations: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "has_clipping": self.has_clipping,
            "clipping_locations": self.clipping_locations,
            "has_dc_offset": self.has_dc_offset,
            "dc_offset_value": self.dc_offset_value,
            "has_discontinuities": self.has_discontinuities,
            "discontinuity_locations": self.discontinuity_locations,
            "has_aliasing": self.has_aliasing
        }


# ============================================================================
# 错误报告
# ============================================================================

@dataclass
class QAError:
    """QA 系统错误"""
    
    error_type: str  # "file_not_found", "format_error", "parameter_error", etc.
    severity: str  # "warning", "error", "critical"
    message: str
    location: str  # 文件路径或代码位置
    suggestion: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
    
    def __str__(self):
        severity_icon = {
            "warning": "⚠️",
            "error": "❌",
            "critical": "🔥"
        }
        icon = severity_icon.get(self.severity, "•")
        return f"{icon} [{self.severity.upper()}] {self.error_type}: {self.message}"


# ============================================================================
# 常量定义
# ============================================================================

# 八度频段定义（Hz）
OCTAVE_BANDS = [
    (31.5, 63),
    (63, 125),
    (125, 250),
    (250, 500),
    (500, 1000),
    (1000, 2000),
    (2000, 4000),
    (4000, 8000),
    (8000, 16000)
]

# 参数合理范围
PARAMETER_RANGES = {
    "t60": (0.1, 10.0),  # 秒
    "pre_delay_ms": (0, 200),  # 毫秒
    "stereo_width": (0, 200),  # 百分比
    "sample_rate": (44100, 96000),  # Hz
    "bit_depth": (16, 24),  # bits
}

# 立体声相关性阈值
STEREO_CORRELATION_THRESHOLDS = {
    "mono": 0.95,  # > 0.95 认为是单声道/居中
    "wide": 0.5,   # < 0.5 认为是宽立体声
}

# 伪影检测阈值
ARTIFACT_THRESHOLDS = {
    "clipping": 0.99,  # 样本值 >= 0.99 认为是削波
    "dc_offset": 0.01,  # |平均值| > 0.01 认为有直流偏移
    "discontinuity": 0.1,  # 相邻样本差 > 0.1 认为是不连续
}

# 心理声学关键频率
PSYCHOACOUSTIC_FREQUENCIES = {
    "threat": 3000,  # Hz，婴儿哭声敏感频率
    "heartbeat_cutoff": 500,  # Hz，心跳低通滤波截止频率
}
