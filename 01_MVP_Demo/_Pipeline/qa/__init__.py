"""
Phase 4 合成质量保证系统
========================

自动化验证、诊断和改进 Phase 4（定位）音频合成的质量保证工具包。

核心模块:
- audio_analyzer: 音频分析引擎（声学指标、频谱分析、立体声成像）
- script_analyzer: 脚本分析引擎（参数提取、逻辑验证、算法检测）
- psychoacoustic_validator: 心理声学验证器（生物拟真性、威胁音频、空间分离）
- multi_track_validator: 多轨混音验证器（平衡、掩蔽、空间分布）
- reference_comparator: 参考比较器（频谱相似度、立体声差异、能量差异）
- diagnostic_reporter: 诊断报告生成器（Markdown、JSON、可视化）
- test_suite: 自动化测试套件（测试编排、摘要报告）

Version: 1.0.0
"""

__version__ = "1.0.0"

# 处理相对导入和绝对导入
try:
    from .audio_analyzer import AudioAnalyzer
    from .script_analyzer import ScriptAnalyzer
    from .psychoacoustic_validator import PsychoacousticValidator
except ImportError:
    from audio_analyzer import AudioAnalyzer
    from script_analyzer import ScriptAnalyzer
    from psychoacoustic_validator import PsychoacousticValidator

__all__ = [
    "AudioAnalyzer",
    "ScriptAnalyzer",
    "PsychoacousticValidator",
]
