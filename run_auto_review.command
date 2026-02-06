#!/bin/bash

# 获取当前脚本所在目录的绝对路径
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目根目录
cd "$DIR"

# 定义颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}   🚀 Wonderland 2.0 Auto-Review Protocol${NC}"
echo -e "${BLUE}   Standards: INI (Narrative) + Sync (Visuals)${NC}"
echo -e "${BLUE}==================================================${NC}"

# Add commons to PYTHONPATH so scripts can import markdown_parser
export PYTHONPATH=$PYTHONPATH:"$DIR/01_MVP_Demo/_Pipeline/commons"

# 0. 环境自检
echo -e "\n${YELLOW}[Step 0] Environment Pre-Flight${NC}"
if [ ! -d ".agent/skills/validation-suite" ]; then
    echo -e "${RED}❌ Critical Error: Validation Suite not found!${NC}"
    exit 1
fi
echo "✅ Environment OK"

# 1. 全局链接检查 (Global Link Integrity)
echo -e "\n${YELLOW}[Step 1] Global Structure & Link Integrity${NC}"
echo "Running validate_links.py..."
python3 .agent/skills/validation-suite/scripts/validate_links.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Link Validation Failed.${NC}"
else
    echo -e "${GREEN}✅ Link Validation Passed.${NC}"
fi

# 2. 详细脚本审计 (Detailed Script Audit)
echo -e "\n${YELLOW}[Step 2] Deep Scan (Anchors, Syntax, Narrative)${NC}"

# 遍历所有脚本
found_issues=0

for f in 03_Scripts/*.md; do
    [ -e "$f" ] || continue
    filename=$(basename "$f")
    # Filter for S0x, Sxx naming convention
    if [[ ! "$filename" =~ ^S ]]; then
         continue
    fi
    
    echo -e "\n${BLUE}👉 Auditing: $filename${NC}"
    
    # 2.1 幻影锚点 (Ghost Anchors)
    # 这一步极其重要，确保 Visuals 都有对应的 Timeline 锚点
    python3 .agent/skills/validation-suite/scripts/validate_anchors.py "$f"
    if [ $? -ne 0 ]; then
        echo -e "${RED}   ❌ Anchor Check Failed${NC}"
        found_issues=$((found_issues + 1))
    else
        echo -e "${GREEN}   ✅ Anchor Check Passed${NC}"
    fi

    # 2.2 语法合规 (Syntax)
    # 检查禁止的 Markdown 写法
    python3 .agent/skills/validation-suite/scripts/validate_syntax.py "$f"
    if [ $? -ne 0 ]; then
        echo -e "${RED}   ❌ Syntax Check Failed${NC}"
        found_issues=$((found_issues + 1))
    else
        echo -e "${GREEN}   ✅ Syntax Check Passed${NC}"
    fi

    # 2.3 叙事完整性 (INI - Narrative Integrity)
    # 检查 "隐形指令", "裸参数", "先讲后图"
    python3 .agent/skills/validation-suite/scripts/validate_narrative_integrity.py "$f"
    if [ $? -ne 0 ]; then
        echo -e "${RED}   ❌ Narrative Integrity Failed${NC}"
        found_issues=$((found_issues + 1))
    else
        echo -e "${GREEN}   ✅ Narrative Integrity Passed${NC}"
    fi

done

# 3. 统计数据 (Stats)
echo -e "\n${YELLOW}[Step 3] Production Stats${NC}"
python3 .agent/skills/validation-suite/scripts/validate_script_length.py --dump-text

# 3.1 机器人语言与泄漏扫描 (Robotic Speech & Leakage Scan)
echo -e "\n${YELLOW}[Step 3.1] Deep Content Scan${NC}"
leak_errors=0

# Check for brackets (Metadata Leakage)
if grep -r "\[.*\]" 03_Scripts/tts/*.txt > /dev/null; then
    echo -e "${RED}   ❌ Metadata Leakage Detected (Found '[...]'):${NC}"
    grep -r --color=always "\[.*\]" 03_Scripts/tts/*.txt | head -n 5
    leak_errors=$((leak_errors + 1))
fi

# Check for robotic headers (Action:/Reason:)
if grep -rE "(Action|Reason|Warning|Step [0-9]):" 03_Scripts/tts/*.txt > /dev/null; then
    echo -e "${RED}   ❌ Robotic Speech Detected (Found 'Action:', 'Reason:'...):${NC}"
    grep -rE --color=always "(Action|Reason|Warning|Step [0-9]):" 03_Scripts/tts/*.txt | head -n 5
    echo -e "${RED}   👉 Please rewrite these lines as natural conversation.${NC}"
    leak_errors=$((leak_errors + 1))
fi

if [ $leak_errors -eq 0 ]; then
    echo -e "${GREEN}   ✅ Content Quality Passed (No Leaks/Robotic Headers)${NC}"
else
    found_issues=$((found_issues + leak_errors))
fi

echo -e "\n${BLUE}==================================================${NC}"
if [ $found_issues -eq 0 ]; then
    echo -e "${GREEN}✨ ALL CHECKS PASSED. READY FOR RECORDING/RENDER.${NC}"
else
    echo -e "${RED}💥 Found $found_issues scripts with issues. Please fix before proceeding.${NC}"
fi
echo -e "${BLUE}==================================================${NC}"

# Pause to let user read
echo "Press any key to exit..."
read -n 1 -s -r
