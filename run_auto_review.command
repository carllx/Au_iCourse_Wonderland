#!/bin/bash

# 获取当前脚本所在目录的绝对路径
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目根目录
cd "$DIR"

echo "=================================================="
echo "   Auto Review - Project Health Check"
echo "   正在运行自动化审查..."
echo "=================================================="

# 1. 运行全项目检查脚本 (CI/CD Health Check)
# 使用 README 中指定的 validate_project.py
python .agent/skills/validation-suite/scripts/validate_project.py

echo "--------------------------------------------------"
echo "📊 生成详细字数统计 (Word Count Stats)"
# 2. 显示详细字数统计表
python .agent/skills/validation-suite/scripts/validate_script_length.py

echo "--------------------------------------------------"
echo "📝 自动提取口播稿 (Auto Dump Text)"
# 3. 自动生成纯文本稿件 (--dump-text)
python .agent/skills/validation-suite/scripts/validate_script_length.py --dump-text

echo "--------------------------------------------------"
echo "🎭 叙事完整性检查 (INI Narrative Integrity Check)"
echo "正在检查 '元数据黑洞' (Invisible Instructions)..."
# 4. 运行叙事完整性检查
for f in 03_Scripts/*.md; do
    [ -e "$f" ] || continue
    # Skip non-script files if any
    if [[ "$f" != *"S0x"* && "$f" != *"Sxx"* && "$f" != *"S0"* ]]; then
        continue
    fi
    echo "Checking: $f"
    python .agent/skills/validation-suite/scripts/validate_narrative_integrity.py "$f"
done

echo "=================================================="
echo "✅ 审查完成 (Review Completed)"
echo "按任意键退出..."
read -n 1 -s -r
