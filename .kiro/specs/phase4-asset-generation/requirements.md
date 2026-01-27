# 需求文档：Phase 4 音频素材生成器

## 简介

本规范用于生成爱丽丝声音剧场项目中 Phase 4（定位 - 镜中双生）所需的所有音频素材。Phase 4 是音频旅程的高潮，通过多轨空间混音创造"爱丽丝在深渊中遇见她的影子自我"的场景。

**故事背景**：在深渊底部，爱丽丝遇到了唯一的"对手"——那个被异化了的自我。

**核心体验**：感受 **150% 的世界荒野** 与 **0% 的自我心跳** 之间的撕裂感，在反向的呓语中，听见时间的枯竭。

## 术语表

- **Phase_4（第四阶段）**: 爱丽丝声音剧场的"定位"阶段，通过立体声定位创建多轨空间混音
- **Track（轨道）**: 多轨混音中的单个音频通道
- **Stereo_Width（立体声宽度）**: 音频的感知空间范围，以百分比衡量（0% = 单声道，100% = 正常立体声，150%+ = 扩展）
- **Visceral_Heartbeat（内脏心跳）**: 沉重、贴耳、干涩的心跳音频，定位在中心
- **Shadow_Self（影子自我）**: 反向人声 + 减慢滴答声的混合音频，代表异化的自我
- **Void_IR（虚空脉冲响应）**: 代表无限深渊空间的脉冲响应（T60 ≥ 5s）
- **Convolution（卷积）**: 将干声与 IR 卷积，创造空间混响效果
- **Mid_Side_Processing（中侧处理）**: 立体声扩展技术，通过调整 Mid 和 Side 信号的比例改变立体声宽度

## 需求

### 需求 1：生成 Track 1 - 处理后的人声

**用户故事：** 作为音频制作者，我想生成经过完整处理的爱丽丝人声轨道，以便在 Phase 4 多轨混音中使用。

#### 验收标准

1. THE Generator SHALL 加载干净的人声文件（`asset_S0X_dry_voice_clean.wav`）
2. THE Generator SHALL 应用 Phase 1 降噪处理（Reduction: 75%, Reduce by: 35dB）
3. THE Generator SHALL 应用 Phase 2 塑形处理（Stretch: 135%, Pitch: -4 semitones）
4. THE Generator SHALL 应用 Phase 3 混响处理（使用 void_ir.wav, Mix: 75%, Room Size: 150%）
5. THE Generator SHALL 输出处理后的人声到 `_Library/S05_Position/asset_S05_voice_processed.wav`
6. THE Generator SHALL 验证输出文件的采样率为 48kHz，位深度为 16-bit

### 需求 2：生成 Track 2 - 内脏心跳

**用户故事：** 作为音频制作者，我想生成沉重、贴耳、干涩的心跳音频，以便作为 Phase 4 的情感锚点。

#### 验收标准

1. THE Generator SHALL 生成 10 秒的心跳音频
2. THE Generator SHALL 使用生物拟真方法（sine_sweep 模拟肌肉收缩 Lub-Dub）
3. THE Generator SHALL 应用低通滤波器模拟骨传导的沉闷感（截止频率 ≤ 500Hz）
4. THE Generator SHALL 确保心跳为单声道（立体声相关性 ≈ 1.0）
5. THE Generator SHALL 设置心率为 60 BPM（每秒 1 次心跳）
6. THE Generator SHALL 输出到 `_Library/S05_Position/asset_S05_heartbeat_visceral.wav`
7. THE Generator SHALL 验证输出的 RMS 能量适中（不过响也不过弱）

### 需求 3：生成 Track 3 - 影子自我

**用户故事：** 作为音频制作者，我想生成反向人声 + 减慢滴答声的混合音频，以便创造"异化自我"的心理效果。

#### 验收标准

1. THE Generator SHALL 加载干净的人声文件并反向播放
2. THE Generator SHALL 生成逐渐变慢的滴答声（起始间隔 0.5s，每次增加 15%）
3. THE Generator SHALL 使用带通滤波器（2500-3500Hz）模拟金属机械声
4. THE Generator SHALL 混合反向人声（60%）和滴答声（40%）
5. THE Generator SHALL 确保混合后的音频产生"恐惧"而非"滑稽"的心理效果
6. THE Generator SHALL 输出到 `_Library/S05_Position/asset_S05_shadow_self.wav`
7. THE Generator SHALL 验证滴答声的频率成分集中在 3000Hz 附近（人类敏感频率）

### 需求 4：生成 Track 4 - 虚空环境（扩展立体声）

**用户故事：** 作为音频制作者，我想生成极宽的立体声虚空环境音频，以便创造"世界荒野"的包裹感。

#### 验收标准

1. THE Generator SHALL 加载或生成虚空 IR（`asset_S04_void_ir.wav`）
2. THE Generator SHALL 验证虚空 IR 的 T60 ≥ 5.0s
3. THE Generator SHALL 应用立体声扩展处理（目标宽度 150%-200%）
4. THE Generator SHALL 使用 Mid-Side 处理技术实现立体声扩展
5. THE Generator SHALL 验证扩展后的立体声相关性 < 0.5（表示宽立体声场）
6. THE Generator SHALL 输出到 `_Library/S05_Position/asset_S05_void_expanded.wav`
7. THE Generator SHALL 确保扩展后的音频不产生相位问题或单声道兼容性问题

### 需求 5：生成最终混音（可选）

**用户故事：** 作为音频制作者，我想生成 4 轨混合的最终混音，以便快速预览 Phase 4 的整体效果。

#### 验收标准

1. THE Generator SHALL 加载所有 4 个轨道（Voice, Heart, Shadow, Void）
2. THE Generator SHALL 确保所有轨道长度一致（填充或裁剪）
3. THE Generator SHALL 应用适当的混音比例（Voice: 主导，Heart: 可听但不压制，Shadow: 背景，Void: 环境）
4. THE Generator SHALL 验证最终混音不削波（峰值 < 0.95）
5. THE Generator SHALL 验证心跳在虚空背景之上可听（SNR ≥ 6dB）
6. THE Generator SHALL 输出到 `_Library/S05_Position/asset_S05_final_mix.wav`

### 需求 6：声学验证

**用户故事：** 作为音频制作者，我想自动验证生成的素材是否符合声学要求，以便确保质量。

#### 验收标准

1. THE Generator SHALL 测量 Track 2（心跳）的立体声相关性，验证 > 0.95
2. THE Generator SHALL 测量 Track 4（虚空）的立体声相关性，验证 < 0.5
3. THE Generator SHALL 测量 Track 4 的 T60，验证 ≥ 5.0s
4. THE Generator SHALL 测量 Track 3（影子）的频谱质心，验证包含 3000Hz 成分
5. THE Generator SHALL 测量 Track 2 的频谱，验证高频衰减 > 20dB @ 500Hz
6. WHEN 任何验证失败时，THE Generator SHALL 输出警告信息并提供修复建议
7. THE Generator SHALL 生成验证报告（Markdown 格式）

### 需求 7：参数配置

**用户故事：** 作为音频制作者，我想通过配置文件调整生成参数，以便快速实验不同的效果。

#### 验收标准

1. THE Generator SHALL 支持通过配置文件（YAML 或 JSON）设置所有关键参数
2. THE Generator SHALL 提供默认配置，符合设计规范的要求
3. THE Generator SHALL 验证配置参数的合理性（范围检查）
4. WHEN 配置参数无效时，THE Generator SHALL 输出错误信息并使用默认值
5. THE Generator SHALL 在输出报告中记录使用的配置参数

### 需求 8：错误处理

**用户故事：** 作为音频制作者，我想在生成过程中遇到错误时得到清晰的提示，以便快速修复问题。

#### 验收标准

1. WHEN 输入文件不存在时，THE Generator SHALL 输出清晰的错误信息并退出
2. WHEN 音频格式不正确时，THE Generator SHALL 输出格式要求并退出
3. WHEN 生成过程中发生异常时，THE Generator SHALL 记录详细的错误日志
4. THE Generator SHALL 在每个关键步骤输出进度信息
5. THE Generator SHALL 在生成完成后输出摘要信息（生成的文件列表、验证结果）

### 需求 9：性能要求

**用户故事：** 作为音频制作者，我想快速生成所有素材，以便高效迭代。

#### 验收标准

1. THE Generator SHALL 在 30 秒内完成所有 4 个轨道的生成（不包括最终混音）
2. THE Generator SHALL 支持并行生成多个轨道（如果可能）
3. THE Generator SHALL 缓存中间结果（如卷积结果），避免重复计算
4. THE Generator SHALL 提供 --quick 模式，跳过验证步骤以加快速度

### 需求 10：集成 QA 系统

**用户故事：** 作为音频制作者，我想在生成后自动运行 QA 验证，以便确保素材质量。

#### 验收标准

1. THE Generator SHALL 在生成完成后自动调用 QA 系统（如果可用）
2. THE Generator SHALL 将 QA 验证结果包含在生成报告中
3. WHEN QA 验证失败时，THE Generator SHALL 输出详细的诊断信息
4. THE Generator SHALL 支持 --skip-qa 选项，跳过 QA 验证
5. THE Generator SHALL 使用 QA 系统的声学验证函数（复用代码）

### 需求 11：可重复性

**用户故事：** 作为音频制作者，我想确保生成结果可重复，以便课程材料保持一致。

#### 验收标准

1. THE Generator SHALL 使用固定的随机种子（可配置）
2. WHEN 使用相同的配置和输入时，THE Generator SHALL 生成位相同的输出
3. THE Generator SHALL 在报告中记录随机种子和所有配置参数
4. THE Generator SHALL 支持 --seed 参数，允许用户指定随机种子

### 需求 12：文档和示例

**用户故事：** 作为音频制作者，我想有清晰的文档和示例，以便快速上手。

#### 验收标准

1. THE Generator SHALL 提供 README.md，包含安装说明和快速开始指南
2. THE Generator SHALL 提供使用示例（命令行示例）
3. THE Generator SHALL 提供配置文件示例（带注释）
4. THE Generator SHALL 在代码中包含详细的 docstrings
5. THE Generator SHALL 提供故障排除指南（常见问题和解决方案）
