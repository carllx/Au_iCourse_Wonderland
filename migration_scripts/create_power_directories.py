#!/usr/bin/env python3
"""Script to create Power directories for the migration."""

from pathlib import Path
from core.power_setup import PowerSetup


def main():
    """Create all Power directories."""
    # Get the project root (parent of migration_scripts)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    print("Creating Power directories...")
    print(f"Project root: {project_root}")
    
    # Create all Power directories
    results = PowerSetup.create_all_power_directories(project_root)
    
    print("\nCreated directories:")
    for skill_name, paths in results.items():
        print(f"\n{skill_name}:")
        print(f"  Power directory: {paths['power_dir']}")
        if 'steering_dir' in paths:
            print(f"  Steering directory: {paths['steering_dir']}")
    
    # Verify the structure
    print("\nVerifying structure...")
    verification = PowerSetup.verify_power_structure(project_root)
    
    all_valid = all(verification.values())
    
    print("\nVerification results:")
    for skill_name, is_valid in verification.items():
        status = "✓" if is_valid else "✗"
        print(f"  {status} {skill_name}: {'Valid' if is_valid else 'Invalid'}")
    
    if all_valid:
        print("\n✓ All Power directories created successfully!")
        return 0
    else:
        print("\n✗ Some Power directories are invalid!")
        return 1


if __name__ == "__main__":
    exit(main())
