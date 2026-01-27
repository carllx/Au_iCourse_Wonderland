# Task 4.1 Summary: Markdown Content Merger

## Task Description
Create/enhance the Markdown content merger to support merging multiple Markdown files while handling section title conflicts, preserving code blocks and formatting.

**Requirements**: 2.1, 2.2, 2.3, 2.4, 2.6

## Implementation Summary

### Enhanced ContentMerger Class
Location: `migration_scripts/core/content_merger.py`

The ContentMerger class was already implemented with most core functionality. This task added the following enhancements:

#### New Methods Added:

1. **`add_section_suffix(content, suffix)`**
   - Adds a suffix to all section headers in content
   - Complements the existing `add_section_prefix()` method
   - Useful for conflict resolution with "(from Source)" style suffixes

2. **`detect_heading_conflicts(contents)`**
   - Detects conflicting headings across multiple content pieces
   - Takes a list of (content, source_name) tuples
   - Returns a dictionary mapping heading text to list of sources where it appears
   - Only returns actual conflicts (headings appearing in multiple sources)

3. **`resolve_heading_conflicts(files, strategy)`**
   - Merges files while resolving heading conflicts
   - Supports both "prefix" and "suffix" strategies
   - Takes list of (file_path, section_title, modifier) tuples
   - Returns processed content ready for final merge
   - Handles missing files gracefully

#### Existing Functionality (Already Implemented):

1. **`merge_markdown_files(files)`**
   - Merges multiple markdown files into a single document
   - Handles missing files with error notes
   - Strips YAML frontmatter from source files

2. **`_strip_frontmatter(content)`**
   - Removes YAML frontmatter from markdown content
   - Preserves the actual content

3. **`should_embed_file(file_path)`**
   - Determines if a file should be embedded or referenced based on size
   - Uses 50KB threshold

4. **`create_file_reference(file_path, description)`**
   - Creates markdown reference to external files
   - Includes file size information

5. **`create_script_documentation(...)`**
   - Creates standardized documentation for scripts
   - Includes purpose, location, usage, parameters, dependencies, execution context
   - Fully supports requirements 3.3, 3.4, 3.5, 3.6

6. **`extract_code_blocks(content)`**
   - Extracts all code blocks from markdown content
   - Preserves code block contents

7. **`preserve_formatting(content)`**
   - Ensures markdown formatting is preserved during merging
   - Proper spacing around headers and code blocks
   - Removes excessive blank lines

8. **`add_section_prefix(content, prefix)`**
   - Adds a prefix to all section headers
   - Useful for conflict resolution

## Test Coverage

Created comprehensive test suite: `migration_scripts/tests/test_content_merger.py`

### Test Results: ✅ 23/23 tests passing

#### Test Categories:

1. **Basic Merging Tests** (2 tests)
   - Basic merging of multiple files
   - Handling missing files

2. **Frontmatter Tests** (2 tests)
   - Stripping YAML frontmatter
   - Handling content without frontmatter

3. **File Size Tests** (3 tests)
   - Small files should be embedded
   - Large files should be referenced
   - Missing files return False

4. **File Reference Tests** (1 test)
   - Creating file references with descriptions

5. **Script Documentation Tests** (2 tests)
   - Full documentation with all parameters
   - Minimal documentation

6. **Code Block Tests** (2 tests)
   - Extracting code blocks
   - Handling content without code blocks

7. **Formatting Tests** (1 test)
   - Preserving markdown formatting

8. **Prefix/Suffix Tests** (2 tests)
   - Adding prefixes to headers
   - Adding suffixes to headers

9. **Conflict Detection Tests** (2 tests)
   - No conflicts scenario
   - Multiple conflicts scenario

10. **Conflict Resolution Tests** (3 tests)
    - Prefix strategy
    - Suffix strategy
    - No modifier scenario

11. **Content Preservation Tests** (3 tests)
    - Code blocks preservation
    - Inline code preservation
    - Special characters preservation

## Requirements Coverage

### ✅ Requirement 2.1: Merge SKILL.md content
- `merge_markdown_files()` handles merging multiple markdown files
- `_strip_frontmatter()` removes YAML frontmatter from source files

### ✅ Requirement 2.2: Integrate rules
- `resolve_heading_conflicts()` can merge rules with conflict resolution
- `add_section_prefix()` can add "Rules: " prefix to distinguish sources

### ✅ Requirement 2.3: Integrate knowledge
- `should_embed_file()` determines embed vs reference based on size
- `create_file_reference()` creates references for large knowledge files

### ✅ Requirement 2.4: Integrate styles
- Same merging capabilities as rules and knowledge
- `add_section_suffix()` can add "(from Styles)" suffix

### ✅ Requirement 2.6: Maintain code examples
- `extract_code_blocks()` identifies code blocks
- `preserve_formatting()` ensures code blocks are preserved
- Tests verify code blocks, inline code, and special characters are maintained

## Key Features

1. **Flexible Conflict Resolution**
   - Automatic conflict detection
   - Multiple resolution strategies (prefix/suffix)
   - Graceful handling of missing files

2. **Format Preservation**
   - Code blocks preserved
   - Inline code preserved
   - Special markdown characters preserved
   - Proper spacing maintained

3. **Smart File Handling**
   - Size-based embed vs reference decisions
   - File size reporting in references
   - Error handling for missing/unreadable files

4. **Script Documentation**
   - Standardized format for all scripts
   - Complete parameter documentation
   - Dependencies and execution context

## Usage Examples

### Basic Merging
```python
from pathlib import Path
from migration_scripts.core.content_merger import ContentMerger

files = [
    (Path(".agent/skills/lab-factory/SKILL.md"), "Core Capabilities"),
    (Path(".agent/rules/rule_mvp_conventions.md"), "Rules and Protocols")
]

merged = ContentMerger.merge_markdown_files(files)
```

### Conflict Resolution
```python
# Detect conflicts first
contents = [
    (file1_content, "SKILL.md"),
    (file2_content, "rules.md")
]
conflicts = ContentMerger.detect_heading_conflicts(contents)

# Resolve with prefixes
files = [
    (Path("file1.md"), "Section 1", "Core: "),
    (Path("file2.md"), "Section 2", "Rules: ")
]
results = ContentMerger.resolve_heading_conflicts(files, strategy="prefix")
```

### Script Documentation
```python
doc = ContentMerger.create_script_documentation(
    script_name="validate_links.py",
    purpose="Validate all links in markdown files",
    location=Path(".agent/skills/validation-suite/scripts/validate_links.py"),
    usage_example="python3 .agent/skills/validation-suite/scripts/validate_links.py",
    dependencies=["requests", "beautifulsoup4"]
)
```

## Next Steps

This task completes the content merger implementation. The next task (4.2) will implement content extraction and filtering functionality to identify and extract relevant parts from rules, knowledge, and style files.

## Status: ✅ COMPLETE

All requirements met:
- ✅ Reads and merges multiple Markdown files
- ✅ Handles section title conflicts (prefix/suffix strategies)
- ✅ Preserves code blocks and formatting
- ✅ 23/23 tests passing
- ✅ No diagnostic issues
- ✅ Comprehensive test coverage
