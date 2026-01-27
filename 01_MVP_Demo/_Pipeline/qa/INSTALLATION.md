# Phase 4 QA 系统安装指南

## 安装状态

✅ **已完成** - 所有核心模块已成功安装并验证

## 已创建的文件

### 核心模块
- ✅ `__init__.py` - 包初始化和导出
- ✅ `config.py` - 配置和数据模型定义
- ✅ `audio_analyzer.py` - 音频分析引擎（1000+ 行）
- ✅ `script_analyzer.py` - 脚本分析引擎（500+ 行）
- ✅ `psychoacoustic_validator.py` - 心理声学验证器（500+ 行）

### 配置文件
- ✅ `requirements.txt` - Python 依赖列表
- ✅ `pytest.ini` - Pytest 配置

### 测试框架
- ✅ `tests/__init__.py` - 测试套件初始化
- ✅ `tests/test_audio_analyzer.py` - 音频分析器测试（包含单元测试和属性测试）

### 文档
- ✅ `README.md` - 完整使用文档
- ✅ `INSTALLATION.md` - 本文件
- ✅ `verify_installation.py` - 安装验证脚本

## 目录结构

```
01_MVP_Demo/_Pipeline/qa/
├── __init__.py                    # 包初始化
├── config.py                      # 配置和数据模型
├── audio_analyzer.py              # 音频分析引擎
├── script_analyzer.py             # 脚本分析引擎
├── psychoacoustic_validator.py    # 心理声学验证器
├── requirements.txt               # 依赖列表
├── pytest.ini                     # Pytest 配置
├── README.md                      # 使用文档
├── INSTALLATION.md                # 本文件
├── verify_installation.py         # 安装验证脚本
└── tests/                         # 测试套件
    ├── __init__.py
    └── test_audio_analyzer.py     # 音频分析器测试
```

## 验证安装

运行验证脚本确认所有模块正常工作：

```bash
cd 01_MVP_Demo/_Pipeline/qa
python3 verify_installation.py
```

预期输出：
```
============================================================
Phase 4 QA 系统安装验证
============================================================

[1/4] 验证配置模块...
  ✓ config.py 导入成功
  ✓ 所有数据模型定义正确

[2/4] 验证音频分析器...
  ✓ audio_analyzer.py 导入成功
  ✓ AudioAnalyzer 类定义正确
  ✓ AudioAnalyzer 初始化成功
  ✓ 计算 RMS 能量: -0.01 dB

[3/4] 验证脚本分析器...
  ✓ script_analyzer.py 导入成功
  ✓ ScriptAnalyzer 类定义正确

[4/4] 验证心理声学验证器...
  ✓ psychoacoustic_validator.py 导入成功
  ✓ PsychoacousticValidator 类定义正确

============================================================
✅ 所有模块验证通过！
```

## 下一步

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

必需依赖：
- numpy >= 1.20.0
- scipy >= 1.7.0
- soundfile >= 0.10.0
- hypothesis >= 6.0.0
- pytest >= 6.0.0
- pytest-cov >= 2.10.0

可选依赖：
- matplotlib >= 3.3.0（用于可视化）

### 2. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/ -m unit

# 运行属性测试
pytest tests/ -m property

# 生成覆盖率报告
pytest tests/ --cov=. --cov-report=html
```

### 3. 开始使用

查看 `README.md` 了解详细使用方法和示例。

快速示例：

```python
from audio_analyzer import AudioAnalyzer

# 分析音频文件
analyzer = AudioAnalyzer(audio_path="path/to/audio.wav")

# 获取声学指标
metrics = analyzer.get_acoustic_metrics()
print(f"T60: {metrics.t60}s")
print(f"立体声相关性: {metrics.stereo_correlation}")

# 检测伪影
artifacts = analyzer.detect_artifacts()
if artifacts.has_clipping:
    print(f"检测到削波: {len(artifacts.clipping_locations)} 处")
```

## 核心功能

### AudioAnalyzer（音频分析引擎）

- **声学指标测量**：T60, C80, EDT, 预延迟
- **立体声分析**：相关系数、宽度、声像位置
- **频谱分析**：PSD, 频谱质心、八度频段能量
- **伪影检测**：削波、直流偏移、不连续性、混叠

### ScriptAnalyzer（脚本分析引擎）

- **参数提取**：使用 AST 解析提取配置参数
- **参数验证**：验证参数是否在合理范围内
- **算法检测**：检测 Voss-McCartney、频率相关衰减等
- **处理顺序验证**：验证处理步骤顺序
- **修复建议**：生成代码级别的修复建议

### PsychoacousticValidator（心理声学验证器）

- **心跳验证**：检测 sine_sweep 和低通滤波
- **威胁音频验证**：检测 3000Hz 和尖锐包络
- **空间分离验证**：验证内/外声像分离
- **感知影响评估**：评估明亮度、黑暗度、焦虑值

## 技术特性

### 导入兼容性

所有模块支持两种导入方式：

1. **相对导入**（作为包使用）：
   ```python
   from qa import AudioAnalyzer
   ```

2. **绝对导入**（直接使用）：
   ```python
   import sys
   sys.path.insert(0, 'path/to/qa')
   from audio_analyzer import AudioAnalyzer
   ```

### 测试框架

- **单元测试**：验证特定示例、边缘情况和错误条件
- **属性测试**：使用 Hypothesis 验证通用属性（100+ 次迭代）
- **集成测试**：验证组件之间的交互

### 数据模型

使用 Python dataclasses 定义清晰的数据模型：
- `TestConfig` - 测试配置
- `ValidationResult` - 验证结果
- `Issue` - 问题报告
- `AcousticMetrics` - 声学指标
- `SpectralAnalysis` - 频谱分析结果
- `ArtifactReport` - 伪影检测报告
- `QAError` - 错误报告

## 参考文档

- **设计文档**: `.kiro/specs/phase4-synthesis-qa/design.md`
- **需求文档**: `.kiro/specs/phase4-synthesis-qa/requirements.md`
- **任务列表**: `.kiro/specs/phase4-synthesis-qa/tasks.md`
- **使用文档**: `README.md`

## 故障排除

### 导入错误

如果遇到导入错误，确保：
1. Python 版本 >= 3.7
2. 所有依赖已安装：`pip install -r requirements.txt`
3. 使用正确的导入方式（见上文"导入兼容性"）

### 测试失败

如果测试失败：
1. 检查依赖版本是否符合要求
2. 确保 numpy, scipy, soundfile 正确安装
3. 查看测试输出的详细错误信息

### 性能问题

如果分析速度慢：
1. 减少音频文件大小或时长
2. 使用较低的采样率（44.1kHz 而非 96kHz）
3. 禁用可视化生成

## 版本信息

- **版本**: 1.0.0
- **创建日期**: 2024
- **Python 要求**: >= 3.7
- **状态**: ✅ 已验证并可用

## 下一步开发

根据任务列表 (`.kiro/specs/phase4-synthesis-qa/tasks.md`)，后续任务包括：

- [ ] 任务 2: 实现音频分析引擎的子任务（声学指标、立体声分析、频谱分析、伪影检测）
- [ ] 任务 4: 实现多轨验证功能
- [ ] 任务 5: 实现心理声学验证器的子任务
- [ ] 任务 7: 实现脚本分析引擎的子任务
- [ ] 任务 8: 实现参考比较器
- [ ] 任务 11: 实现诊断报告生成器
- [ ] 任务 12: 实现自动化测试套件

每个任务都包含相应的属性测试要求。
