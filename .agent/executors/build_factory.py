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
        return f"[ERROR: File not found: {path}]"
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
    prompt = f"""
# SYSTEM PROMPT: COURSEWARE WRITER AGENT

## 1. IDENTITY & STYLE (The "Who")
{persona}

## 2. THE MISSION (The "What")
You are tasked to write the transcript for **{section}**.
Your instructions are defined in the Skill below:

{skill}

## 3. CONTEXT & KNOWLEDGE (The "Brain")
### A. Course Structure (The Master Plan)
{structure}

### B. Action Dictionary (The Moves)
{actions}

### C. Textbook Index (The Truth)
{knowledge_index}

## 4. IMMEDIATE EXECUTION TRIGGER
> Please write the full verbatim transcript for module: **{section}**.
> Adhere strictly to the "Style" and "Deep Listening" rules defined above.
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
# SYSTEM PROMPT: PEDAGOGY AUDITOR AGENT

## 1. THE MISSION
You are the Quality Control Auditor. Your job is to verify the following transcript against strict educational standards.

## 2. AUDIT CRITERIA (The Rules)
{skill}

## 3. DOCUMENT TO AUDIT
{target_content}

## 4. IMMEDIATE EXECUTION TRIGGER
> Please output the "Audit Report" as defined in the rules above.
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
