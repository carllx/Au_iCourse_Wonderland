"""Full scan demo showing complete documentation generation."""

from pathlib import Path
from migration_scripts.core.script_scanner import ScriptScanner

def main():
    agent_path = Path(".agent")
    
    print("=" * 80)
    print("COMPLETE SCRIPT DOCUMENTATION GENERATION")
    print("=" * 80)
    
    # Scan all skills
    all_scripts = ScriptScanner.scan_all_skills(agent_path)
    
    # Scan executors
    executors = ScriptScanner.scan_executors(agent_path)
    
    # Generate documentation for each skill
    for skill_name, scripts in sorted(all_scripts.items()):
        print(f"\n{'=' * 80}")
        print(f"SKILL: {skill_name}")
        print(f"{'=' * 80}\n")
        
        # Generate documentation with metadata extraction
        docs = ScriptScanner.generate_all_documentation(scripts, extract_metadata=True)
        print(docs)
    
    # Generate documentation for executors
    if executors:
        print(f"\n{'=' * 80}")
        print(f"EXECUTORS")
        print(f"{'=' * 80}\n")
        
        docs = ScriptScanner.generate_all_documentation(executors, extract_metadata=True)
        print(docs)
    
    # Summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    total_scripts = sum(len(scripts) for scripts in all_scripts.values()) + len(executors)
    print(f"\nTotal scripts documented: {total_scripts}")
    print(f"  - lab-factory: {len(all_scripts.get('lab-factory', []))} scripts")
    print(f"  - validation-suite: {len(all_scripts.get('validation-suite', []))} scripts")
    print(f"  - executors: {len(executors)} scripts")

if __name__ == "__main__":
    main()
