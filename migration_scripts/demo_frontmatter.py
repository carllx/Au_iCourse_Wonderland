#!/usr/bin/env python3
"""
Demonstration script for YAML frontmatter generation.

This script shows how to use the power_metadata module to generate
YAML frontmatter for the three Powers.
"""

from core.power_metadata import (
    generate_frontmatter_for_power,
    generate_all_frontmatters,
    get_all_power_names
)


def main():
    """Demonstrate frontmatter generation."""
    print("=" * 70)
    print("YAML Frontmatter Generator Demo")
    print("=" * 70)
    print()
    
    # Show all power names
    print("Available Powers:")
    for name in get_all_power_names():
        print(f"  - {name}")
    print()
    
    # Generate frontmatter for each power individually
    print("=" * 70)
    print("Individual Frontmatter Generation")
    print("=" * 70)
    print()
    
    for power_name in get_all_power_names():
        print(f"Power: {power_name}")
        print("-" * 70)
        frontmatter = generate_frontmatter_for_power(power_name)
        print(frontmatter)
        print()
    
    # Generate all frontmatters at once
    print("=" * 70)
    print("Batch Frontmatter Generation")
    print("=" * 70)
    print()
    
    all_frontmatters = generate_all_frontmatters()
    print(f"Generated frontmatters for {len(all_frontmatters)} Powers")
    print()
    
    # Show summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    for power_name, frontmatter in all_frontmatters.items():
        lines = frontmatter.strip().split('\n')
        print(f"\n{power_name}:")
        print(f"  Lines: {len(lines)}")
        print(f"  Size: {len(frontmatter)} bytes")


if __name__ == '__main__':
    main()
