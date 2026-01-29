import os
import sys
import subprocess
import time

def run_validator(script_name, description):
    """
    Runs a validation script and returns (success, output).
    """
    print(f"\n🚀 Running {description}...")
    print(f"   [Script]: {script_name}")
    
    start_time = time.time()
    
    # Scripts are in the same directory as this master script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, script_name)
    
    # We must run from project root for most scripts to work
    # Assuming this script is at .agent/skills/validation-suite/scripts/
    # Root is ../../../../
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    
    if not os.path.exists(script_path):
        print(f"   ❌ Script not found: {script_path}")
        return False

    try:
        # Run process
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=project_root, # CRITICAL: Run from root
            capture_output=True,
            text=True
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   ✅ PASSED ({duration:.2f}s)")
            # Optional: Print output if needed, or just summary
            # For pedagogy warnings, we might want to see output even on success?
            # But usually we keep it clean.
            return True
        else:
            print(f"   ❌ FAILED ({duration:.2f}s)")
            print("   --- Output ---")
            print(result.stdout)
            print("   --- Error ---")
            print(result.stderr)
            print("   --------------")
            return False

    except Exception as e:
        print(f"   ❌ EXECUTION ERROR: {str(e)}")
        return False

def main():
    print("🛡️  STARTING PROJECT VALIDATION SUITE 🛡️")
    print("========================================")
    
    validators = [
        ("validate_links.py", "Link & Asset Integrity Check"),
        ("validate_consistency.py", "Data Consistency Check"),
        ("validate_script_length.py", "Duration & Pacing Check"),
        ("validate_pedagogy.py", "Pedagogy & Narrative Check")
    ]
    
    results = []
    
    for script, desc in validators:
        success = run_validator(script, desc)
        results.append((desc, success))
        
    print("\n========================================")
    print("📊 VALIDATION SUMMARY")
    print("========================================")
    
    all_passed = True
    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {desc}")
        if not success:
            all_passed = False
            
    if all_passed:
        print("\n✨ All systems go! Project is healthy.")
        sys.exit(0)
    else:
        print("\n💥 Some checks failed. Please review logs above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
