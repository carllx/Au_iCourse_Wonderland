"""
脚本分析引擎
============

分析生成器脚本的参数配置、处理逻辑和算法选择。

核心功能:
- 参数提取（使用 AST 解析）
- 参数范围验证
- 算法检测（Voss-McCartney、频率相关衰减等）
- 处理顺序验证
- 代码级别修复建议生成
"""

import ast
import os
from typing import Dict, List, Any, Optional, Tuple
import re

# 处理相对导入和绝对导入
try:
    from .config import Issue, PARAMETER_RANGES
except ImportError:
    from config import Issue, PARAMETER_RANGES


class ScriptAnalyzer:
    """
    脚本分析引擎
    
    分析生成器脚本的参数配置、处理逻辑和算法选择。
    
    属性:
        script_path: 脚本文件路径
        script_content: 脚本内容
        ast_tree: 抽象语法树
        parameters: 提取的参数字典
    """
    
    def __init__(self, script_path: str):
        """
        初始化脚本分析器
        
        参数:
            script_path: 生成器脚本文件路径
        
        异常:
            FileNotFoundError: 脚本文件不存在
            SyntaxError: 脚本语法错误
        """
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        self.script_path = script_path
        
        # 读取脚本内容
        with open(script_path, 'r', encoding='utf-8') as f:
            self.script_content = f.read()
        
        # 解析 AST
        try:
            self.ast_tree = ast.parse(self.script_content)
        except SyntaxError as e:
            raise SyntaxError(f"脚本语法错误: {e}")
        
        # 提取参数
        self.parameters = {}
        self._extract_parameters()
    
    # ========================================================================
    # 参数提取
    # ========================================================================
    
    def _extract_parameters(self):
        """
        从脚本中提取关键参数
        
        提取策略:
        1. 查找配置字典（如 VOID_CONFIG, HEARTBEAT_CONFIG）
        2. 查找函数调用参数
        3. 查找全局变量赋值
        """
        # 遍历 AST
        for node in ast.walk(self.ast_tree):
            # 查找字典赋值（配置字典）
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # 检查是否是配置字典
                        if 'CONFIG' in var_name.upper() or 'PARAM' in var_name.upper():
                            if isinstance(node.value, ast.Dict):
                                config_dict = self._extract_dict_values(node.value)
                                self.parameters[var_name] = config_dict
    
    def _extract_dict_values(self, dict_node: ast.Dict) -> Dict[str, Any]:
        """
        从 AST Dict 节点提取值
        
        参数:
            dict_node: AST Dict 节点
        
        返回:
            字典，键为字符串，值为提取的值
        """
        result = {}
        
        for key, value in zip(dict_node.keys, dict_node.values):
            # 提取键
            if isinstance(key, ast.Constant):
                key_str = key.value
            elif isinstance(key, ast.Str):  # Python 3.7 兼容
                key_str = key.s
            else:
                continue
            
            # 提取值
            result[key_str] = self._extract_value(value)
        
        return result
    
    def _extract_value(self, node: ast.AST) -> Any:
        """
        从 AST 节点提取值
        
        参数:
            node: AST 节点
        
        返回:
            提取的值（int, float, str, bool, None）
        """
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Num):  # Python 3.7 兼容
            return node.n
        elif isinstance(node, ast.Str):  # Python 3.7 兼容
            return node.s
        elif isinstance(node, ast.NameConstant):  # Python 3.7 兼容
            return node.value
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            # 负数
            return -self._extract_value(node.operand)
        else:
            return None
    
    def extract_parameters(self) -> Dict[str, Any]:
        """
        获取提取的参数
        
        返回:
            参数字典
        """
        return self.parameters
    
    # ========================================================================
    # 参数验证
    # ========================================================================
    
    def validate_parameter_ranges(self) -> List[Issue]:
        """
        验证参数值是否在合理范围内
        
        返回:
            问题列表
        """
        issues = []
        
        for config_name, config_dict in self.parameters.items():
            if not isinstance(config_dict, dict):
                continue
            
            # 验证 T60
            if 't60' in config_dict:
                t60 = config_dict['t60']
                if t60 is not None:
                    min_t60, max_t60 = PARAMETER_RANGES['t60']
                    if not (min_t60 <= t60 <= max_t60):
                        issues.append(Issue(
                            issue_type="parameter",
                            severity="high",
                            location=f"{self.script_path}:{config_name}['t60']",
                            description=f"T60 值 {t60}s 超出合理范围 [{min_t60}, {max_t60}]",
                            fix_suggestion=f"建议将 T60 调整到 {min_t60}-{max_t60}s 范围内。"
                                          f"对于虚空空间，建议使用 6.0s 或更长。"
                        ))
            
            # 验证预延迟
            if 'pre_delay_ms' in config_dict:
                pre_delay = config_dict['pre_delay_ms']
                if pre_delay is not None:
                    min_delay, max_delay = PARAMETER_RANGES['pre_delay_ms']
                    if not (min_delay <= pre_delay <= max_delay):
                        issues.append(Issue(
                            issue_type="parameter",
                            severity="medium",
                            location=f"{self.script_path}:{config_name}['pre_delay_ms']",
                            description=f"预延迟 {pre_delay}ms 超出合理范围 [{min_delay}, {max_delay}]",
                            fix_suggestion=f"建议将预延迟调整到 {min_delay}-{max_delay}ms 范围内。"
                        ))
            
            # 验证采样率
            if 'sample_rate' in config_dict:
                sr = config_dict['sample_rate']
                if sr is not None:
                    min_sr, max_sr = PARAMETER_RANGES['sample_rate']
                    if not (min_sr <= sr <= max_sr):
                        issues.append(Issue(
                            issue_type="parameter",
                            severity="critical",
                            location=f"{self.script_path}:{config_name}['sample_rate']",
                            description=f"采样率 {sr}Hz 超出合理范围 [{min_sr}, {max_sr}]",
                            fix_suggestion=f"建议使用标准采样率：48000Hz（推荐）或 44100Hz。"
                        ))
        
        return issues
    
    # ========================================================================
    # 算法检测
    # ========================================================================
    
    def detect_algorithm_issues(self) -> List[Issue]:
        """
        检测算法选择问题
        
        检测内容:
        1. 是否使用 Voss-McCartney 粉红噪音算法
        2. 是否实现频率相关衰减
        3. 是否使用正确的滤波器设计
        
        返回:
            问题列表
        """
        issues = []
        
        # 检测 Voss-McCartney 算法
        has_voss_mccartney = self._detect_voss_mccartney()
        if not has_voss_mccartney:
            # 检查是否使用了粉红噪音
            if 'pink' in self.script_content.lower() or 'noise' in self.script_content.lower():
                issues.append(Issue(
                    issue_type="algorithm",
                    severity="high",
                    location=self.script_path,
                    description="未检测到 Voss-McCartney 粉红噪音算法，可能使用了朴素 FFT 方法",
                    fix_suggestion="建议使用 Voss-McCartney 算法生成粉红噪音，"
                                  "该方法比 FFT 整形更准确，产生真正的 -3dB/octave 频谱斜率。"
                                  "参考 gen_S04_void_ir.py 中的 generate_pink_noise_voss() 函数。"
                ))
        
        # 检测频率相关衰减
        has_freq_dependent_decay = self._detect_frequency_dependent_decay()
        if not has_freq_dependent_decay:
            # 检查是否生成了 IR
            if 'ir' in self.script_content.lower() or 'impulse' in self.script_content.lower():
                issues.append(Issue(
                    issue_type="algorithm",
                    severity="medium",
                    location=self.script_path,
                    description="未检测到频率相关衰减实现",
                    fix_suggestion="建议实现频率相关衰减，模拟空气吸收和材料阻尼。"
                                  "高频应该比低频衰减更快。"
                                  "参考 gen_S04_void_ir.py 中的 apply_frequency_dependent_decay() 函数。"
                ))
        
        return issues
    
    def _detect_voss_mccartney(self) -> bool:
        """
        检测是否使用 Voss-McCartney 算法
        
        返回:
            是否使用
        """
        # 检查函数名
        if 'voss' in self.script_content.lower() or 'mccartney' in self.script_content.lower():
            return True
        
        # 检查特征代码模式（二进制计数器方法）
        patterns = [
            r'update_mask\s*=\s*i\s*&\s*-i',  # update_mask = i & -i
            r'np\.log2\(update_mask\)',  # np.log2(update_mask)
            r'sources\[source_idx\]\s*=\s*np\.random\.randn\(\)',  # 更新源
        ]
        
        for pattern in patterns:
            if re.search(pattern, self.script_content):
                return True
        
        return False
    
    def _detect_frequency_dependent_decay(self) -> bool:
        """
        检测是否实现频率相关衰减
        
        返回:
            是否实现
        """
        # 检查函数名
        if 'frequency_dependent_decay' in self.script_content.lower():
            return True
        
        # 检查特征代码模式（多频段滤波）
        patterns = [
            r'butter.*btype\s*=\s*[\'"]low[\'"]',  # 低通滤波器
            r'butter.*btype\s*=\s*[\'"]band[\'"]',  # 带通滤波器
            r'butter.*btype\s*=\s*[\'"]high[\'"]',  # 高通滤波器
            r't60_low.*t60_high',  # 不同频段的 T60
        ]
        
        match_count = 0
        for pattern in patterns:
            if re.search(pattern, self.script_content):
                match_count += 1
        
        # 如果匹配到多个特征，认为实现了频率相关衰减
        return match_count >= 2
    
    # ========================================================================
    # 处理顺序验证
    # ========================================================================
    
    def validate_processing_order(self) -> List[Issue]:
        """
        验证处理顺序的正确性
        
        检查内容:
        1. 卷积是否在立体声扩展之前
        2. 归一化是否在最后
        
        返回:
            问题列表
        """
        issues = []
        
        # 查找关键处理步骤的位置
        convolution_pos = self._find_operation_position('convolve')
        stereo_expand_pos = self._find_operation_position('stereo')
        normalize_pos = self._find_operation_position('normalize')
        
        # 验证卷积 -> 立体声扩展顺序
        if convolution_pos is not None and stereo_expand_pos is not None:
            if convolution_pos > stereo_expand_pos:
                issues.append(Issue(
                    issue_type="processing_order",
                    severity="high",
                    location=self.script_path,
                    description="处理顺序错误：立体声扩展应该在卷积之后",
                    fix_suggestion="建议先进行卷积处理，然后再进行立体声扩展。"
                                  "这样可以避免双重干信号问题。"
                ))
        
        # 验证归一化在最后
        if normalize_pos is not None:
            # 检查归一化之后是否还有其他处理
            last_processing_pos = max(
                convolution_pos or 0,
                stereo_expand_pos or 0
            )
            if normalize_pos < last_processing_pos:
                issues.append(Issue(
                    issue_type="processing_order",
                    severity="medium",
                    location=self.script_path,
                    description="归一化应该在所有处理步骤之后",
                    fix_suggestion="建议将归一化移到最后，确保最终输出不会削波。"
                ))
        
        return issues
    
    def _find_operation_position(self, operation: str) -> Optional[int]:
        """
        查找操作在脚本中的位置（行号）
        
        参数:
            operation: 操作关键词（如 'convolve', 'stereo', 'normalize'）
        
        返回:
            行号（从0开始），如果未找到则返回 None
        """
        lines = self.script_content.split('\n')
        
        for i, line in enumerate(lines):
            if operation.lower() in line.lower():
                # 排除注释
                if not line.strip().startswith('#'):
                    return i
        
        return None
    
    # ========================================================================
    # 修复建议生成
    # ========================================================================
    
    def generate_fix_suggestions(self, issues: List[Issue]) -> List[Issue]:
        """
        为问题生成代码级别的修复建议
        
        参数:
            issues: 问题列表
        
        返回:
            增强的问题列表（包含代码片段）
        """
        enhanced_issues = []
        
        for issue in issues:
            # 为参数问题生成代码片段
            if issue.issue_type == "parameter":
                if "T60" in issue.description:
                    issue.code_snippet = self._generate_t60_fix_code(issue)
                elif "预延迟" in issue.description:
                    issue.code_snippet = self._generate_pre_delay_fix_code(issue)
            
            # 为算法问题生成代码片段
            elif issue.issue_type == "algorithm":
                if "Voss-McCartney" in issue.description:
                    issue.code_snippet = self._generate_voss_mccartney_code()
                elif "频率相关衰减" in issue.description:
                    issue.code_snippet = self._generate_freq_decay_code()
            
            enhanced_issues.append(issue)
        
        return enhanced_issues
    
    def _generate_t60_fix_code(self, issue: Issue) -> str:
        """生成 T60 修复代码"""
        return """# 修复建议：调整 T60 参数
VOID_CONFIG = {
    't60': 6.0,  # 修改为 6.0s（虚空空间推荐值）
    # ... 其他参数
}
"""
    
    def _generate_pre_delay_fix_code(self, issue: Issue) -> str:
        """生成预延迟修复代码"""
        return """# 修复建议：调整预延迟参数
VOID_CONFIG = {
    'pre_delay_ms': 100,  # 修改为 100ms（推荐值）
    # ... 其他参数
}
"""
    
    def _generate_voss_mccartney_code(self) -> str:
        """生成 Voss-McCartney 算法代码"""
        return """# 修复建议：使用 Voss-McCartney 算法生成粉红噪音
def generate_pink_noise_voss(n_samples, num_sources=16, random_seed=None):
    if random_seed is not None:
        np.random.seed(random_seed)
    
    sources = np.random.randn(num_sources)
    output = np.zeros(n_samples)
    
    for i in range(n_samples):
        update_mask = i & -i
        if update_mask > 0:
            source_idx = int(np.log2(update_mask)) % num_sources
            sources[source_idx] = np.random.randn()
        output[i] = np.sum(sources)
    
    output = output / np.max(np.abs(output))
    return output

# 参考: gen_S04_void_ir.py
"""
    
    def _generate_freq_decay_code(self) -> str:
        """生成频率相关衰减代码"""
        return """# 修复建议：实现频率相关衰减
def apply_frequency_dependent_decay(signal_input, sample_rate, t60_low, t60_high):
    n_samples = len(signal_input)
    duration = n_samples / sample_rate
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # 定义频段
    LOW_CUTOFF = 500
    HIGH_CUTOFF = 4000
    
    # 设计滤波器
    sos_low = scipy_signal.butter(4, LOW_CUTOFF, btype='low', fs=sample_rate, output='sos')
    sos_mid = scipy_signal.butter(4, [LOW_CUTOFF, HIGH_CUTOFF], btype='band', fs=sample_rate, output='sos')
    sos_high = scipy_signal.butter(4, HIGH_CUTOFF, btype='high', fs=sample_rate, output='sos')
    
    # 分离频段
    band_low = scipy_signal.sosfilt(sos_low, signal_input)
    band_mid = scipy_signal.sosfilt(sos_mid, signal_input)
    band_high = scipy_signal.sosfilt(sos_high, signal_input)
    
    # 应用不同的衰减
    t60_mid = (t60_low + t60_high) / 2
    alpha_low = -np.log(0.001) / t60_low
    alpha_mid = -np.log(0.001) / t60_mid
    alpha_high = -np.log(0.001) / t60_high
    
    env_low = np.exp(-t * alpha_low)
    env_mid = np.exp(-t * alpha_mid)
    env_high = np.exp(-t * alpha_high)
    
    band_low *= env_low
    band_mid *= env_mid
    band_high *= env_high
    
    return band_low + band_mid + band_high

# 参考: gen_S04_void_ir.py
"""
