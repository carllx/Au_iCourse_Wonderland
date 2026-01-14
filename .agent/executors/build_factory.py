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
SCRIPTS_DIR = os.path.join(BASE_DIR, "01_Scripts")
DEMO_DIR = os.path.join(BASE_DIR, "03_MVP_Demo")

def read_file(path):
    """Reads a file and returns its content. Returns error string if not found."""
    if not os.path.exists(path):
        # [Security Fix] V-02: Prevent silent failure
        print(f"[FATAL ERROR] Critical component missing: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def build_writer_prompt(section):
    """Assembles the prompt for the Writer Agent."""
    
    # 1. Load Components
    persona = read_file(os.path.join(STYLES_DIR, "LinXin_Voice.md"))
    skill = read_file(os.path.join(SKILLS_DIR, "compile_transcript.md"))
    knowledge_index = read_file(os.path.join(KNOWLEDGE_DIR, "Textbook_Index.md"))
    structure = read_file(os.path.join(SCRIPTS_DIR, "00_Structure_Map.md"))
    actions = read_file(os.path.join(DEMO_DIR, "Action_Map.md"))
    
    # 2. Extract Specific Section from Structure (Naive text search for demo)
    # real impl might parse markdown properly, but here we dump the whole structure 
    # and ask LLM to focus on the specific section.
    
    # 3. Assemble
    # 3. Assemble
    prompt = f"""
# SYSTEM PROMPT: COURSEWARE WRITER AGENT (课件写作 Agent)

## 1. IDENTITY & STYLE (身份与风格)
{persona}

## 2. THE MISSION (任务目标)
你现在的任务是为 **{section}** 章节编写逐字稿。
你的指令定义在以下的技能文档中：

{skill}

## 3. CONTEXT & KNOWLEDGE (上下文与知识库)
### A. Course Structure (课程结构与教学逻辑)
{structure}

### B. Action Dictionary (演示动作映射表)
{actions}

### C. Textbook Index (教材知识库 - 唯一真理源)
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
    skill = read_file(os.path.join(SKILLS_DIR, "pedagogy_auditor.md"))
    
    # 2. Load Target Content
    target_content = read_file(target_file)
    
    # 3. Assemble
    prompt = f"""
# SYSTEM PROMPT: PEDAGOGY AUDITOR AGENT (教学审查 Agent)

## 1. THE MISSION (任务目标)
你是质量控制审计员。你的工作是根据严格的教育标准审查以下逐字稿。

## 2. AUDIT CRITERIA (审查标准)
{skill}

## 3. DOCUMENT TO AUDIT (待审查文档)
{target_content}

## 4. IMMEDIATE EXECUTION TRIGGER (立即执行指令)
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
