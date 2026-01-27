#!/usr/bin/env python3
"""
验证 QA 系统安装
================

验证所有核心模块是否正确安装和可导入。
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_installation():
    """验证安装"""
    print("=" * 60)
    print("Phase 4 QA 系统安装验证")
    print("=" * 60)
    
    errors = []
    
    # 1. 验证配置模块
    print("\n[1/4] 验证配置模块...")
    try:
        import config
        print("  ✓ config.py 导入成功")
        
        # 验证关键类
        assert hasattr(config, 'TestConfig')
        assert hasattr(config, 'ValidationResult')
        assert hasattr(config, 'Issue')
        assert hasattr(config, 'AcousticMetrics')
        print("  ✓ 所有数据模型定义正确")
    except Exception as e:
        errors.append(f"配置模块错误: {e}")
        print(f"  ✗ 错误: {e}")
    
    # 2. 验证音频分析器
    print("\n[2/4] 验证音频分析器...")
    try:
        import audio_analyzer
        print("  ✓ audio_analyzer.py 导入成功")
        
        # 验证关键类
        assert hasattr(audio_analyzer, 'AudioAnalyzer')
        print("  ✓ AudioAnalyzer 类定义正确")
        
        # 测试基本功能
        import numpy as np
        test_audio = np.random.randn(48000)  # 1秒音频
        analyzer = audio_analyzer.AudioAnalyzer(audio_data=test_audio, sample_rate=48000)
        print("  ✓ AudioAnalyzer 初始化成功")
        
        # 测试方法
        rms = analyzer.compute_rms_energy()
        print(f"  ✓ 计算 RMS 能量: {rms:.2f} dB")
        
    except Exception as e:
        errors.append(f"音频分析器错误: {e}")
        print(f"  ✗ 错误: {e}")
    
    # 3. 验证脚本分析器
    print("\n[3/4] 验证脚本分析器...")
    try:
        import script_analyzer
        print("  ✓ script_analyzer.py 导入成功")
        
        # 验证关键类
        assert hasattr(script_analyzer, 'ScriptAnalyzer')
        print("  ✓ ScriptAnalyzer 类定义正确")
        
    except Exception as e:
        errors.append(f"脚本分析器错误: {e}")
        print(f"  ✗ 错误: {e}")
    
    # 4. 验证心理声学验证器
    print("\n[4/4] 验证心理声学验证器...")
    try:
        import psychoacoustic_validator
        print("  ✓ psychoacoustic_validator.py 导入成功")
        
        # 验证关键类
        assert hasattr(psychoacoustic_validator, 'PsychoacousticValidator')
        print("  ✓ PsychoacousticValidator 类定义正确")
        
    except Exception as e:
        errors.append(f"心理声学验证器错误: {e}")
        print(f"  ✗ 错误: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    if errors:
        print("❌ 验证失败")
        print("\n错误列表:")
        for error in errors:
            print(f"  • {error}")
        return False
    else:
        print("✅ 所有模块验证通过！")
        print("\nQA 系统已成功安装，可以开始使用。")
        print("\n快速开始:")
        print("  1. 安装依赖: pip install -r requirements.txt")
        print("  2. 运行测试: pytest tests/")
        print("  3. 查看文档: cat README.md")
        return True

if __name__ == "__main__":
    success = verify_installation()
    sys.exit(0 if success else 1)
