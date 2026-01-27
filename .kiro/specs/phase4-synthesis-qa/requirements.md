# 需求文档

## 简介

本规范针对爱丽丝声音剧场项目中 Phase 4（定位）音频合成的质量保证系统。Phase 4 通过立体声定位、混响扩展和心理声音设计，创建一个多轨空间混音，表现"爱丽丝在深渊中遇见她的影子自我"。

**当前问题诊断：**
- Python 合成生成的声音素材本身质量正常
- 模拟结果也正常
- **怀疑是脚本逻辑有误**（生成器脚本的参数配置、处理流程可能存在问题）
- **技术可行性不确定**（某些音频处理方法可能在理论上可行但实际效果不佳）

Phase 4 是音频旅程的高潮：在净化（Phase 1）、塑形（Phase 2）和空间处理（Phase 3）之后，Phase 4 将多个音频元素定位在立体声空间中，在 150% 扩展的虚空环境和 0% 居中的心跳之间创造"撕裂的现实"。合成涉及卷积混响、立体声扩展、多轨混音和心理声音设计元素（反向人声、减慢的滴答声）之间的复杂交互。

**QA 系统的核心目标：**
1. 验证 Python 生成的素材质量（波形、频谱、声学指标）
2. 诊断生成器脚本的逻辑错误（参数配置、处理顺序、算法选择）
3. 评估技术可行性（某些处理方法是否真的能达到预期效果）
4. 提供可操作的修复建议（具体到代码级别的修改）

## 术语表

- **Phase_4（第四阶段）**: 爱丽丝声音剧场的"定位"阶段，通过立体声定位创建多轨空间混音
- **Synthesis_Pipeline（合成管道）**: 基于 Python 的音频生成系统，使用 scipy、numpy 和 soundfile
- **Multi_Track_Mix（多轨混音）**: Adobe Audition 会话，结合 4 个轨道：人声（居中）、心跳（居中单声道）、影子（居中反向）、虚空 IR（立体声扩展）
- **Stereo_Width（立体声宽度）**: 音频的感知空间范围，以百分比衡量（0% = 单声道，100% = 正常立体声，150%+ = 扩展）
- **Void_IR（虚空脉冲响应）**: 代表无限深渊空间的脉冲响应（T60 ≥ 5s，预延迟 ≥ 80ms）
- **Shadow_Self（影子自我）**: 带有减慢滴答效果的反向人声音频，代表异化的自我
- **Visceral_Heartbeat（内脏心跳）**: 定位在中心、立体声宽度为 0% 的内部心跳音频
- **Wet_Signal（湿信号）**: 通过卷积混响处理的音频（包含空间特性）
- **Stereo_Correlation（立体声相关性）**: 左右声道之间相似度的度量（-1 到 +1，其中 +1 = 相同，0 = 不相关，-1 = 反相）
- **QA_System（质量保证系统）**: 用于测试、验证和调试 Phase 4 合成的质量保证工具
- **Generator（生成器）**: 合成音频资产的 Python 脚本（例如 gen_S05_panning_assets.py）

## 需求

### 需求 1：组件隔离测试

**用户故事：** 作为音频开发者，我想单独测试 Phase 4 的各个组件，以便识别哪个特定元素导致了质量问题。

#### 验收标准

1. WHEN 测试单个轨道时，THE QA_System SHALL 独立生成和验证每个轨道（人声、心跳、影子、虚空 IR）
2. WHEN 验证虚空 IR 轨道时，THE QA_System SHALL 验证 T60 ≥ 5.0s、预延迟 ≥ 80ms 和立体声宽度 ≥ 150%
3. WHEN 验证心跳轨道时，THE QA_System SHALL 验证单声道定位（立体声相关性 ≈ 1.0）和居中声像
4. WHEN 验证影子自我轨道时，THE QA_System SHALL 验证反向人声特征和减慢滴答元素的存在
5. WHEN 测试卷积处理时，THE QA_System SHALL 验证湿信号不包含双重干信号伪影

### 需求 2：立体声成像验证

**用户故事：** 作为音频教育者，我想测量和验证立体声成像特性，以便验证 150% 世界和 0% 心跳之间的"撕裂现实"效果。

#### 验收标准

1. WHEN 分析立体声宽度时，THE QA_System SHALL 计算每个轨道的立体声相关系数
2. WHEN 测量虚空 IR 轨道时，THE QA_System SHALL 验证立体声相关性 < 0.5（表示宽立体声场）
3. WHEN 测量心跳轨道时，THE QA_System SHALL 验证立体声相关性 > 0.95（表示单声道/居中定位）
4. THE QA_System SHALL 生成立体声场可视化，显示每个轨道的空间分布
5. WHEN 检测到立体声宽度问题时，THE QA_System SHALL 报告未满足宽度要求的特定轨道

### 需求 3：频谱平衡分析与频率掩蔽检测

**用户故事：** 作为音频开发者，我想分析轨道间的频率平衡，以便确保没有频率掩蔽或"单声道灾难"问题。

#### 验收标准

1. WHEN 分析多轨混音时，THE QA_System SHALL 计算每个轨道的功率谱密度
2. THE QA_System SHALL 识别轨道竞争能量的频段（潜在掩蔽），特别是中心声像位置的频率冲突
3. WHEN 虚空 IR 主导低频（<200Hz）时，THE QA_System SHALL 警告潜在的心跳掩蔽（参考：04_stereo_panning 的"单声道灾难"）
4. THE QA_System SHALL 验证影子自我轨道与人声轨道具有不同的频谱特征（避免"浆糊"效果）
5. WHEN 生成频谱报告时，THE QA_System SHALL 可视化所有四个轨道的频率分布，并标注掩蔽风险区域
6. THE QA_System SHALL 检测"中间车道拥堵"问题（多个轨道在 Center 位置竞争相同频段）

### 需求 4：混响质量验证

**用户故事：** 作为音频教育者，我想验证混响特性，以便确保虚空空间听起来"无限、黑暗、遥远"而不是"近距离和浑浊"。

#### 验收标准

1. WHEN 分析虚空 IR 时，THE QA_System SHALL 使用 Schroeder 积分测量 T60 衰减时间
2. THE QA_System SHALL 验证 T60 在目标值的 ±10% 范围内（虚空 ≥5.0s）
3. WHEN 测量频率相关衰减时，THE QA_System SHALL 验证高频比低频衰减更快
4. THE QA_System SHALL 计算清晰度指数（C80）并验证其表示遥远/扩散空间（C80 < -5dB）
5. WHEN 检测到混响质量问题时，THE QA_System SHALL 报告特定的声学指标违规

### 需求 5：混音平衡验证

**用户故事：** 作为音频教育者，我想验证轨道之间的相对电平，以便确保心跳在虚空环境沉浸时保持可听。

#### 验收标准

1. WHEN 分析最终混音时，THE QA_System SHALL 计算每个轨道的 RMS 能量电平
2. THE QA_System SHALL 验证心跳轨道在虚空 IR 背景之上可听（SNR ≥ 6dB）
3. THE QA_System SHALL 验证人声轨道是主要焦点（最高 RMS 能量）
4. WHEN 影子自我轨道太响时，THE QA_System SHALL 警告可能分散主叙事的注意力
5. THE QA_System SHALL 生成电平平衡可视化，显示相对轨道能量

### 需求 6：伪影检测

**用户故事：** 作为音频开发者，我想检测常见的合成伪影，以便识别和修复削波、混叠或不连续性等技术问题。

#### 验收标准

1. WHEN 分析音频文件时，THE QA_System SHALL 检测削波（样本在 ±1.0 或 ±32767）
2. THE QA_System SHALL 检测直流偏移（平均值显著不同于零）
3. THE QA_System SHALL 检测不连续性（突然的幅度跳跃表示咔嗒/爆音）
4. WHEN 分析高频内容时，THE QA_System SHALL 检测潜在的混叠伪影
5. WHEN 检测到伪影时，THE QA_System SHALL 报告其位置（时间位置）和严重程度

### 需求 7：参考比较

**用户故事：** 作为音频教育者，我想将合成输出与参考音频进行比较，以便量化当前输出与预期的偏差程度。

#### 验收标准

1. WHEN 提供参考音频文件时，THE QA_System SHALL 计算频谱相似度指标
2. THE QA_System SHALL 计算参考音频和测试音频之间的立体声相关性差异
3. THE QA_System SHALL 计算参考音频和测试音频之间的 RMS 能量差异
4. WHEN 差异超过阈值（>20% 偏差）时，THE QA_System SHALL 标记显著偏差
5. THE QA_System SHALL 生成并排比较可视化（波形、频谱、立体声场）

### 需求 8：自动化测试套件

**用户故事：** 作为音频开发者，我想要一个自动化测试套件，以便在进行更改后快速验证合成输出。

#### 验收标准

1. THE QA_System SHALL 提供单个命令来运行所有验证测试
2. WHEN 运行测试套件时，THE QA_System SHALL 按顺序测试所有 Phase 4 组件
3. THE QA_System SHALL 生成摘要报告，显示每个测试的通过/失败状态
4. WHEN 任何测试失败时，THE QA_System SHALL 提供可操作的诊断信息
5. THE QA_System SHALL 在 60 秒内完成完整的测试套件

### 需求 9：诊断报告

**用户故事：** 作为音频教育者，我想要全面的诊断报告，以便准确了解问题所在以及如何修复。

#### 验收标准

1. WHEN 验证失败时，THE QA_System SHALL 生成详细的诊断报告
2. THE QA_System SHALL 在报告中包含可视化（波形、频谱图、立体声图）
3. THE QA_System SHALL 提供修复已识别问题的具体建议
4. THE QA_System SHALL 以人类可读（Markdown）和机器可读（JSON）格式保存报告
5. WHEN 检测到多个问题时，THE QA_System SHALL 按严重程度对其进行优先级排序

### 需求 10：与现有 IR 合成集成

**用户故事：** 作为开发者，我想让 QA 系统与现有的 IR 合成改进集成，以便利用经过验证的声学算法。

#### 验收标准

1. THE QA_System SHALL 使用与 IR 合成改进规范相同的声学验证函数（T60 测量、C80、EDT）
2. WHEN 验证虚空 IR 时，THE QA_System SHALL 应用与 gen_S04_void_ir.py 相同的质量标准
3. THE QA_System SHALL 检测生成的 IR 是否使用过时的算法（例如，朴素粉红噪音而不是 Voss-McCartney）
4. THE QA_System SHALL 验证所有 IR 组件中正确实现了频率相关衰减
5. WHEN 检测到 IR 质量问题时，THE QA_System SHALL 参考 IR 合成改进规范进行修复

### 需求 11：感知质量指标与心理声学验证

**用户故事：** 作为音频教育者，我想要感知质量指标和心理声学验证，以便评估音频是否达到预期的情感和教学影响。

#### 验收标准

1. THE QA_System SHALL 计算每个轨道和最终混音的响度指标（LUFS）
2. THE QA_System SHALL 计算动态范围指标（峰值因数、峰值与 RMS 比率）
3. THE QA_System SHALL 使用通道间相关性分析估计感知空间宽度
4. THE QA_System SHALL 计算频谱质心以评估虚空的"明亮度"或"黑暗度"
5. WHEN 感知指标偏离目标时，THE QA_System SHALL 解释感知影响（例如，"对于深渊场景来说听起来太明亮"）
6. THE QA_System SHALL 验证心跳的生物拟真性（检测是否使用 sine_sweep 模拟肌肉收缩，低通滤波模拟骨传导）
7. WHEN 分析影子自我的心理效果时，THE QA_System SHALL 评估是否达到"恐惧"而非"滑稽"（参考：04_stereo_panning 的焦虑刺激设计）
8. THE QA_System SHALL 检测关键频率的心理声学特性（例如，3000Hz 对应婴儿哭声的敏感频率）

### 需求 12：生成器脚本验证

**用户故事：** 作为开发者，我想验证生成器脚本，以便在运行完整合成管道之前确保它们产生正确的输出。

#### 验收标准

1. WHEN 验证 gen_S05_panning_assets.py 时，THE QA_System SHALL 验证它生成所有四个必需的轨道
2. THE QA_System SHALL 验证生成器脚本使用正确的采样率（48kHz）和位深度（16 位）
3. THE QA_System SHALL 验证生成器脚本将文件保存到正确的位置（_Library/S05_Position/）
4. WHEN 生成器参数无效时，THE QA_System SHALL 检测并报告配置错误
5. THE QA_System SHALL 验证生成器脚本包含适当的验证输出（声学指标）

### 需求 14：脚本逻辑诊断

**用户故事：** 作为开发者，我想诊断生成器脚本的逻辑错误，以便识别参数配置、处理顺序或算法选择的问题。

#### 验收标准

1. WHEN 分析生成器脚本时，THE QA_System SHALL 提取并验证所有关键参数（T60、预延迟、立体声宽度、混音比例）
2. THE QA_System SHALL 检测参数值是否在合理范围内（例如，T60 应为 5-8s 而不是 2.5s）
3. WHEN 检测到参数异常时，THE QA_System SHALL 提供具体的修正建议（例如，"将 T60 从 2.5s 增加到 6.0s"）
4. THE QA_System SHALL 验证处理顺序的正确性（例如，卷积应在立体声扩展之前）
5. THE QA_System SHALL 检测算法选择问题（例如，使用朴素 FFT 粉红噪音而不是 Voss-McCartney）
6. WHEN 发现脚本逻辑错误时，THE QA_System SHALL 生成代码级别的修复建议（具体到行号和代码片段）

### 需求 15：技术可行性评估

**用户故事：** 作为音频教育者，我想评估某些音频处理方法的技术可行性，以便确定理论上可行的方法在实际中是否能达到预期效果。

#### 验收标准

1. WHEN 评估立体声扩展技术时，THE QA_System SHALL 测试不同扩展算法（Mid-Side、Haas、相位调制）的实际效果
2. THE QA_System SHALL 比较理论预期与实际听感（例如，150% 扩展是否真的产生"包裹全身"的感觉）
3. WHEN 某种技术方法效果不佳时，THE QA_System SHALL 建议替代方案（例如，"使用 Haas 效果代替简单的相位反转"）
4. THE QA_System SHALL 评估卷积混响的湿/干比例是否合理（避免双重干信号问题）
5. THE QA_System SHALL 测试反向人声和减慢滴答声的心理效果是否达到预期（"恐惧"而不是"滑稽"）
6. WHEN 技术可行性存疑时，THE QA_System SHALL 提供实验性测试方案（例如，"生成 3 个不同参数版本进行 A/B 测试"）

### 需求 16：心理声学设计验证

**用户故事：** 作为音频教育者，我想验证心理声学设计的有效性，以便确保音频元素达到预期的心理和情感效果。

#### 验收标准

1. WHEN 验证心跳音频时，THE QA_System SHALL 检测是否使用生物拟真方法（sine_sweep 模拟肌肉收缩 Lub-Dub）
2. THE QA_System SHALL 验证心跳是否应用低通滤波器模拟骨传导的沉闷感
3. WHEN 分析威胁音频时，THE QA_System SHALL 检测是否使用人类敏感频率（3000Hz 对应婴儿哭声）
4. THE QA_System SHALL 验证威胁音频的包络曲线是否使用高次幂（例如 `base_lfo ** 8`）制造尖锐突袭感
5. WHEN 评估空间布局时，THE QA_System SHALL 验证"内"（心跳）与"外"（威胁）的声像分离是否清晰
6. THE QA_System SHALL 检测动态声像移动是否增加焦虑值（移动的威胁比静止的更危险）
7. WHEN 心理声学设计不符合预期时，THE QA_System SHALL 提供基于生物学和心理学的修正建议（参考：04_stereo_panning 的验证依据）

### 需求 13：往返验证

**用户故事：** 作为开发者，我想验证合成是确定性和可重现的，以便课程材料保持一致。

#### 验收标准

1. WHEN 使用固定随机种子生成 Phase 4 音频时，THE QA_System SHALL 验证重复运行时的位相同输出
2. THE QA_System SHALL 验证重新生成所有组件会产生声学等效的结果（±1% 容差）
3. WHEN 比较多次合成运行时，THE QA_System SHALL 检测非确定性行为
4. THE QA_System SHALL 验证 Adobe Audition 会话文件引用正确的资产路径
5. FOR ALL Phase 4 组件，生成然后验证然后重新生成 SHALL 产生一致的质量指标

