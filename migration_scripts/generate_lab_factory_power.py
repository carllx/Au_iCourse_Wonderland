#!/usr/bin/env python3
"""
Generate lab-factory-power/power.md using all migration tools.

This script demonstrates the complete migration workflow:
1. PowerSetup - Create directory structure
2. PowerMetadata - Generate YAML frontmatter
3. ContentExtractor - Extract content from SKILL.md, rules, knowledge
4. ScriptScanner - Document all JSX scripts
5. ContentMerger - Merge everything together
"""

from pathlib import Path
import sys

# Add migration_scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from core.power_setup import PowerSetup
from core.power_metadata import generate_frontmatter_for_power
from core.content_extractor import ContentExtractor
from core.script_scanner import ScriptScanner
from core.content_merger import ContentMerger
from core.file_ops import FileOperations


def generate_lab_factory_power():
    """Generate the complete lab-factory-power/power.md file."""
    
    # Get base paths
    base_path = Path.cwd()
    agent_path = base_path / ".agent"
    
    print("🚀 Starting Lab Factory Power generation...")
    print(f"   Base path: {base_path}")
    print(f"   Agent path: {agent_path}")
    
    # Step 1: Create Power directory structure
    print("\n📁 Step 1: Creating Power directory structure...")
    power_paths = PowerSetup.create_power_directory(
        skill_name="lab-factory",
        base_path=base_path,
        create_steering=True
    )
    power_dir = power_paths['power_dir']
    print(f"   ✓ Created: {power_dir}")
    print(f"   ✓ Created: {power_paths['steering_dir']}")
    
    # Step 2: Generate YAML frontmatter
    print("\n📝 Step 2: Generating YAML frontmatter...")
    frontmatter = generate_frontmatter_for_power('lab-factory-power')
    print(f"   ✓ Generated frontmatter with keywords: audition, automation, audio, jsx, extendscript, asset-generation")
    
    # Step 3: Extract content from SKILL.md
    print("\n📖 Step 3: Extracting content from SKILL.md...")
    skill_md_path = agent_path / "skills" / "lab-factory" / "SKILL.md"
    skill_content = ContentExtractor.extract_skill_content(skill_md_path)
    print(f"   ✓ Extracted from: {skill_md_path}")
    print(f"   ✓ Found sections: overview, capabilities, usage, dependencies, limitations, protocols")
    
    # Step 4: Extract rule content
    print("\n📋 Step 4: Extracting rule content...")
    rules_dir = agent_path / "rules"
    rule_mvp_path = rules_dir / "rule_mvp_conventions.md"
    rule_content = ContentExtractor.extract_rule_content(rule_mvp_path)
    print(f"   ✓ Extracted from: {rule_mvp_path}")
    
    # Step 5: Extract knowledge content
    print("\n🧠 Step 5: Extracting knowledge content...")
    knowledge_dir = agent_path / "knowledge"
    audition_skills_path = knowledge_dir / "Audition_Skills_Map.md"
    knowledge_content = ContentExtractor.extract_knowledge_content(audition_skills_path)
    print(f"   ✓ Extracted from: {audition_skills_path}")
    print(f"   ✓ Should embed: {knowledge_content['should_embed']}")
    print(f"   ✓ File size: {knowledge_content['file_size_kb']:.1f} KB")
    
    # Step 6: Scan and document JSX scripts
    print("\n🔍 Step 6: Scanning JSX library scripts...")
    skill_path = agent_path / "skills" / "lab-factory"
    scripts = ScriptScanner.scan_skill_directory(skill_path)
    print(f"   ✓ Found {len(scripts)} scripts")
    
    # Extract metadata from scripts
    for script in scripts:
        ScriptScanner.extract_script_metadata(script)
    
    # Generate documentation for all scripts
    scripts_doc = ScriptScanner.generate_all_documentation(scripts, extract_metadata=False)
    print(f"   ✓ Generated documentation for all scripts")
    
    # Step 7: Merge everything together
    print("\n🔧 Step 7: Merging all content...")
    
    # Build the complete power.md content
    content_parts = []
    
    # Add title
    content_parts.append("# Lab Factory\n\n")
    
    # Add overview - use the full_content which already has frontmatter stripped
    # But we need to remove any remaining frontmatter blocks and the duplicate title
    overview_content = skill_content['full_content']
    
    # Remove any remaining frontmatter blocks (there might be multiple)
    while '---\n' in overview_content:
        # Find the start of a frontmatter block
        start_idx = overview_content.find('---\n')
        if start_idx != -1:
            # Find the end of the frontmatter block
            end_idx = overview_content.find('---\n', start_idx + 4)
            if end_idx != -1:
                # Remove the frontmatter block
                overview_content = overview_content[:start_idx] + overview_content[end_idx + 4:]
            else:
                break
        else:
            break
    
    # Remove the first H1 title if it exists (since we already added our own)
    lines = overview_content.split('\n')
    filtered_lines = []
    skip_next_empty = False
    for i, line in enumerate(lines):
        if i == 0 and line.startswith('# '):
            skip_next_empty = True
            continue
        if skip_next_empty and line.strip() == '':
            skip_next_empty = False
            continue
        filtered_lines.append(line)
    
    overview_content = '\n'.join(filtered_lines).lstrip()
    
    content_parts.append("## Overview\n\n")
    content_parts.append(overview_content)
    content_parts.append("\n\n")
    
    # Add script references section
    content_parts.append("## Script References\n\n")
    content_parts.append("The Lab Factory Power uses external JSX libraries that remain in their original locations. ")
    content_parts.append("These scripts are referenced here with complete usage instructions.\n\n")
    content_parts.append(scripts_doc)
    content_parts.append("\n\n")
    
    # Add rules section
    if rule_content:
        content_parts.append("## Rules and Conventions\n\n")
        content_parts.append("### MVP Demo Architecture Guidelines\n\n")
        content_parts.append(rule_content)
        content_parts.append("\n\n")
    
    # Add knowledge base section
    if knowledge_content['content']:
        content_parts.append("## Knowledge Base\n\n")
        content_parts.append("### Audition Technical Skills Index\n\n")
        if knowledge_content['should_embed']:
            content_parts.append(knowledge_content['content'])
        else:
            content_parts.append(f"**Location**: `{audition_skills_path}`\n\n")
            content_parts.append(knowledge_content['content'])
        content_parts.append("\n\n")
    
    # Add troubleshooting section
    content_parts.append("## Troubleshooting\n\n")
    content_parts.append("### Common Issues\n\n")
    content_parts.append("1. **Import failures**: If `Audition.IO.importFile()` fails, the script will generate a `MANUAL_GUIDE.md` ")
    content_parts.append("with instructions for manual import. This is part of the Traffic Light protocol (4xx status).\n\n")
    content_parts.append("2. **Track creation failures**: If `Audition.Track.getOrCreate()` returns null, ")
    content_parts.append("this indicates an Audition 2024 API bug. Handle this gracefully in your scripts.\n\n")
    content_parts.append("3. **Fast debug**: Use `fast_run.sh` with `Audition.Log.sentinel()` to avoid alert popups ")
    content_parts.append("and blind sleep waits during development.\n\n")
    
    # Combine all parts
    full_content = frontmatter + "\n" + "".join(content_parts)
    
    # Apply formatting preservation
    full_content = ContentMerger.preserve_formatting(full_content)
    
    # Step 8: Write power.md file
    print("\n💾 Step 8: Writing power.md file...")
    power_md_path = power_dir / "power.md"
    FileOperations.write_file(power_md_path, full_content)
    print(f"   ✓ Written to: {power_md_path}")
    
    # Step 9: Verify the file
    print("\n✅ Step 9: Verifying generated file...")
    if power_md_path.exists():
        size = power_md_path.stat().st_size
        print(f"   ✓ File exists: {power_md_path}")
        print(f"   ✓ File size: {size / 1024:.1f} KB")
        
        # Verify YAML frontmatter
        from core.yaml_handler import YAMLHandler
        is_valid, error = YAMLHandler.validate_power_md(power_md_path)
        if is_valid:
            print(f"   ✓ YAML frontmatter is valid")
        else:
            print(f"   ✗ YAML frontmatter validation failed: {error}")
    else:
        print(f"   ✗ File was not created!")
        return False
    
    print("\n🎉 Lab Factory Power generation complete!")
    print(f"\n📄 Generated file: {power_md_path}")
    print(f"📊 Total scripts documented: {len(scripts)}")
    print(f"📚 Integrated content:")
    print(f"   - SKILL.md (lab-factory)")
    print(f"   - rule_mvp_conventions.md")
    print(f"   - Audition_Skills_Map.md")
    print(f"   - {len(scripts)} JSX library scripts")
    
    return True


if __name__ == "__main__":
    try:
        success = generate_lab_factory_power()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
