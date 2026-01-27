"""Demo script to test the scanner on actual .agent directory."""

from pathlib import Path
from migration_scripts.core.script_scanner import ScriptScanner

def main():
    agent_path = Path(".agent")
    
    print("=" * 80)
    print("SCANNING ALL SKILLS")
    print("=" * 80)
    
    all_scripts = ScriptScanner.scan_all_skills(agent_path)
    
    for skill_name, scripts in all_scripts.items():
        print(f"\n{skill_name}:")
        print(f"  Found {len(scripts)} scripts")
        for script in scripts:
            print(f"    - {script.name} ({script.script_type})")
    
    print("\n" + "=" * 80)
    print("SCANNING EXECUTORS")
    print("=" * 80)
    
    executors = ScriptScanner.scan_executors(agent_path)
    print(f"\nFound {len(executors)} executor(s)")
    for script in executors:
        print(f"  - {script.name}")
    
    print("\n" + "=" * 80)
    print("GENERATING DOCUMENTATION FOR LAB-FACTORY SCRIPTS")
    print("=" * 80)
    
    if "lab-factory" in all_scripts:
        lab_scripts = all_scripts["lab-factory"]
        # Extract metadata and generate docs for first script
        if lab_scripts:
            script = lab_scripts[0]
            script = ScriptScanner.extract_script_metadata(script)
            doc = ScriptScanner.generate_script_documentation(script)
            print(f"\nSample documentation for {script.name}:")
            print(doc)
    
    print("\n" + "=" * 80)
    print("GENERATING DOCUMENTATION FOR VALIDATION-SUITE SCRIPTS")
    print("=" * 80)
    
    if "validation-suite" in all_scripts:
        val_scripts = all_scripts["validation-suite"]
        # Generate all docs
        all_docs = ScriptScanner.generate_all_documentation(val_scripts, extract_metadata=True)
        print("\nAll validation scripts documentation:")
        print(all_docs[:500] + "..." if len(all_docs) > 500 else all_docs)

if __name__ == "__main__":
    main()
