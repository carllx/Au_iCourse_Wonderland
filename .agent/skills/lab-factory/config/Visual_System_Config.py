# Visual_System_Config.py
# 视觉系统配置：定义 UI 主题、字体加载与指标通感翻译
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# --- Path Configuration ---
# Assuming this file is in .agent/skills/lab-factory/config/
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CONFIG_DIR, "../../../../"))
FONT_DIR = os.path.join(PROJECT_ROOT, ".agent/assets/fonts")

# --- Font Loading ---
def load_web_font(font_name="MiSans-Regular.ttf"):
    font_path = os.path.join(FONT_DIR, font_name)
    if not os.path.exists(font_path):
        # Fallback to system font if missing, but printing warning
        print(f"Warning: Font not found at {font_path}. Using default.")
        return None
    return fm.FontProperties(fname=font_path)

# Pre-load properties for efficiency
FONT_REGULAR = load_web_font("MiSans-Regular.ttf")
FONT_MEDIUM = load_web_font("MiSans-Medium.ttf")

class VisualTheme:
    """定义 Matplotlib 的视觉主题配置"""
    DARK_CINEMATIC = {
        'figure.facecolor': '#1A1A1A',   # 深石墨
        'axes.facecolor': '#1A1A1A',     # 深石墨
        'axes.edgecolor': '#444444',     # 枪灰色边框
        'axes.labelcolor': '#dddddd',    # 钛白文字
        'xtick.color': '#888888',
        'ytick.color': '#888888',
        'text.color': '#dddddd',
        'grid.color': '#333333',
        'grid.linestyle': '--',
        'lines.linewidth': 2.0,
        # 'font.family': 'sans-serif', # Handled by FontProperties manually in plot
        'savefig.facecolor': '#1A1A1A'
    }

class Palette:
    """DAW 配色方案"""
    BG = '#1A1A1A'
    WAVE = '#40E0D0'    # Spectrum Cyan
    ENV = '#FF007F'     # Cyber Pink
    HIGHLIGHT = '#FFD700' # Narrative Gold
    GRID = '#444444'

class MetricTranslator:
    """指标通感翻译器：将技术指标翻译为叙事语言"""
    
    _DICTIONARY = {
        "Decay Time": "时间的遗物 (Decay)", # Narrative Layer transition target
        "T60": "$T_{60}$", # LaTeX support
        "Pre-Delay": "空间的留白",
        "Wet Level": "深渊的深度",
        "Dry Level": "人性的残留",
        "dB": "dBFS",
        # Bad Case Diagnosis
        "Hum Detected": "⏚ 电网干扰 (Hum)", # Used simple geometric symbol or text only if font supports, trying distinct text
        "Click Detected": "!!! 瞬态爆音 (Click)",
        "Hiss Floor": "::: 宽频底噪 (Hiss)",
        "Waveform Analysis": "时域分析 (Waveform)",
        "Spectral Diagnosis": "频域诊断 (Spectrogram)"
    }

    @staticmethod
    def translate(tech_term: str) -> str:
        return MetricTranslator._DICTIONARY.get(tech_term, tech_term)

# 当前激活主题
CURRENT_THEME = VisualTheme.DARK_CINEMATIC
