import os
import argparse
import sys

# Define Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
AGENT_DIR = os.path.join(BASE_DIR, ".agent")
STYLES_DIR = os.path.join(AGENT_DIR, "styles")
SKILLS_DIR = os.path.join(AGENT_DIR, "skills")
KNOWLEDGE_DIR = os.path.join(AGENT_DIR, "knowledge")
RULES_DIR = os.path.join(AGENT_DIR, "rules")
SCRIPTS_DIR = os.path.join(BASE_DIR, "03_Scripts")
DEMO_DIR = os.path.join(BASE_DIR, "01_MVP_Demo")

def read_file(path):
    """Reads a file and returns its content. Returns error string if not found."""
    if not os.path.exists(path):
        # [Security Fix] V-02: Prevent silent failure
        print(f"[FATAL ERROR] Critical component missing: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_section(content, section_id):
    """
    [Fix V-03/V-05] Context Slicing
    Extracts only the relevant section from the markdown content (plus global header).
    """
    lines = content.split('\n')
    header_lines = []
    section_lines = []

    # 1. Capture Global Header (Metadata before first H2)
    for line in lines:
        if line.startswith('## '):
            break
        header_lines.append(line)

    # 2. Capture Target Section
    capturing = False
    found = False

    for line in lines:
        # Start capturing when we find the Section ID in an H2 header
        if line.startswith('## ') and section_id in line:
            capturing = True
            found = True
            section_lines.append(line)
            continue

        # Stop capturing when we hit the next H2 header
        if capturing and line.startswith('## '):
            break

        if capturing:
            section_lines.append(line)

    if not found:
        # Fallback for safety, though V-02 enforces file existence, this handles missing ID
        return f"[WARNING] Section '{section_id}' not found. Returning full content.\n\n" + content

    return '\n'.join(header_lines + ["\n"] + section_lines)

def build_writer_prompt(section):
    """Assembles the prompt for the Writer Agent."""

    # 1. Load Components
    persona = read_file(os.path.join(STYLES_DIR, "LinXin_Voice.md"))
    skill = read_file(os.path.join(SKILLS_DIR, "transcript_compiler/SKILL.md"))
    knowledge_index = read_file(os.path.join(KNOWLEDGE_DIR, "Textbook_Index.md"))
    structure = read_file(os.path.join(SCRIPTS_DIR, "00_Structure_Map.md"))
    design_spec = read_file(os.path.join(DEMO_DIR, "00_Design_Spec_Alice.md"))

    # 2. [Safe Slice] Extract Specific Section
    # Fix V-03: Only inject the relevant section of the structure map
    sliced_structure = extract_section(structure, section)

    # 3. Assemble
    prompt = f"""
# SYSTEM PROMPT: COURSEWARE WRITER AGENT (课件写作 Agent)

## 1. IDENTITY & STYLE (身份与风格)
{persona}

## 2. THE MISSION (任务目标)
你现在的任务是为 **{section}** 章节编写逐字稿。
你的指令定义在以下的技能文档中：

{skill}

### D. Design Specification (设计真理 - 核心参数源)
{design_spec}

## 3. CONTEXT & KNOWLEDGE (上下文与知识库)
### A. Course Structure (课程结构与教学逻辑 - Current Slice)
{sliced_structure}

### B. Textbook Index (教材知识库 - 唯一真理源)
{knowledge_index}

## 4. IMMEDIATE EXECUTION TRIGGER (立即执行指令)
> 请为章节 **{section}** 编写完整的、逐字的讲稿。
> **关键约束**：
> 1. **语言**：必须严格使用 **简体中文**。
> 2. **风格**：严格遵循 "LinXin_Voice" (林昕) 的导演口吻。
> 3. **留白**：必须包含 "Deep Listening" (深听) 环节。
"""
    return prompt

def build_auditor_prompt(target_file):
    """Assembles the prompt for the Auditor Agent."""

    # 1. Load Components
    # [Fix V-02] Corrected path to validation suite
    skill = read_file(os.path.join(SKILLS_DIR, "validation-suite/docs/pedagogy_auditor.md"))
    
    # [Fix V-02] Load Truth Sources
    design_spec = read_file(os.path.join(DEMO_DIR, "00_Design_Spec_Alice.md"))

    # 2. Load Target Content
    target_content = read_file(target_file)

    # 3. Assemble
    prompt = f"""
# SYSTEM PROMPT: PEDAGOGY AUDITOR AGENT (教学审查 Agent)

## 1. THE MISSION (任务目标)
你是质量控制审计员。你的工作是根据 stric t的教育标准和**技术真理**审查以下逐字稿。

## 2. AUDIT CRITERIA (审查标准)
{skill}

## 3. TECHNICAL TRUTH (技术真理 - 核心参数源)
> 所有的脚本参数必须与以下设计规范完全一致。任何偏差 (e.g. +3 vs +5) 都视为 BUG。

{design_spec}

## 4. DOCUMENT TO AUDIT (待审查文档)
{target_content}

## 5. IMMEDIATE EXECUTION TRIGGER (立即执行指令)
> 请根据上述规则输出 "审计报告 (Audit Report)"。
> **语言要求**：所有评价和建议必须使用 **简体中文**。
"""
    return prompt

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agent Prompt Factory")
    parser.add_argument("--task", choices=["writer", "auditor"], required=True, help="Which agent to build?")
    parser.add_argument("--section", help="For Writer: Which section ID to generate? (e.g. S02)")
    parser.add_argument("--file", help="For Auditor: Which file path to audit?")

    args = parser.parse_args()

    if args.task == "writer":
        if not args.section:
            print("Error: Writer task requires --section")
            sys.exit(1)
        print(build_writer_prompt(args.section))

    elif args.task == "auditor":
        if not args.file:
            print("Error: Auditor task requires --file")
            sys.exit(1)
        print(build_auditor_prompt(args.file))
