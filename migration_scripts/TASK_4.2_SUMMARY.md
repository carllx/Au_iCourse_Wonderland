# Task 4.2 Summary: Content Extraction and Filtering

## Overview

Implemented comprehensive content extraction and filtering functionality for the agent-to-power migration system. This module intelligently extracts and filters content from various source files (SKILL.md, rules, knowledge, styles) based on relevance to each Power.

## Implementation Details

### Core Module: `content_extractor.py`

Created `migration_scripts/core/content_extractor.py` with the `ContentExtractor` class that provides:

#### 1. SKILL.md Content Extraction
- **Method**: `extract_skill_content(skill_md_path)`
- **Functionality**: Extracts structured content from SKILL.md files
- **Returns**: Dictionary with sections:
  - `overview`: Overview/description section
  - `capabilities`: Core capabilities/features
  - `usage`: Usage instructions
  - `dependencies`: Dependencies and file references
  - `limitations`: Known limitations
  - `protocols`: Robustness protocols or best practices
  - `full_content`: Complete content without frontmatter

#### 2. Rules Content Extraction
- **Method**: `extract_rule_content(rule_path, skill_context)`
- **Functionality**: Extracts content from rule files, stripping frontmatter
- **Returns**: Clean rule content ready for integration

#### 3. Knowledge Base Content Extraction
- **Method**: `extract_knowledge_content(knowledge_path, skill_context, max_size_kb)`
- **Functionality**: Intelligently handles knowledge files based on size
  - Small files (<50KB): Returns full content for embedding
  - Large files (≥50KB): Returns summary with reference
- **Returns**: Dictionary with:
  - `content`: Full content or summary
  - `should_embed`: Boolean indicating embedding strategy
  - `file_size_kb`: File size for reporting

#### 4. Style Guide Content Extraction
- **Method**: `extract_style_content(style_path)`
- **Functionality**: Extracts style guide content without frontmatter
- **Returns**: Clean style guide content

#### 5. Relevance Mapping
Pre-configured mappings for each skill:

**Lab Factory**:
- Rules: `rule_mvp_conventions.md`
- Knowledge: `Audition_Skills_Map.md`
- Styles: None

**Validation Suite**:
- Rules: None
- Knowledge: None
- Styles: None

**Transcript Compiler**:
- Rules: `rule_workflow_protocol.md`, `rule_pedagogy_scaffolding.md`, `rule_script_standards.md`, `rule_narrative_consistency.md`
- Knowledge: `Textbook_Index.md`, `Chapter_Mapping.md`
- Styles: `LinXin_Voice.md`

#### 6. Helper Methods
- `get_relevant_rules(skill_id, rules_dir)`: Get relevant rule files for a skill
- `get_relevant_knowledge(skill_id, knowledge_dir)`: Get relevant knowledge files
- `get_relevant_styles(skill_id, styles_dir)`: Get relevant style guides
- `_strip_frontmatter(content)`: Remove YAML frontmatter
- `_extract_sections(content)`: Parse markdown into sections
- `_find_section(sections, keywords)`: Find sections by keyword matching
- `_extract_summary(content, max_lines)`: Create summaries for large files
- `extract_code_examples(content)`: Extract code blocks with language tags
- `filter_relevant_content(content, keywords, context_lines)`: Filter by keywords
- `identify_script_references(content)`: Find .py and .jsx file references

## Testing

### Unit Tests (`test_content_extractor.py`)
Created 24 comprehensive unit tests covering:
- ✅ SKILL.md content extraction (full and missing files)
- ✅ Rule content extraction
- ✅ Knowledge content extraction (small and large files)
- ✅ Style guide extraction
- ✅ Relevance mapping (rules, knowledge, styles)
- ✅ Frontmatter stripping
- ✅ Section extraction and finding
- ✅ Summary generation
- ✅ Code example extraction
- ✅ Content filtering by keywords
- ✅ Script reference identification
- ✅ Emoji header support
- ✅ Code block preservation
- ✅ Mapping completeness validation

**Result**: All 24 tests pass ✅

### Integration Tests (`test_content_extractor_integration.py`)
Created 12 integration tests using real .agent files:
- ✅ Extract lab-factory SKILL.md
- ✅ Extract validation-suite SKILL.md
- ✅ Extract transcript-compiler SKILL.md
- ✅ Extract MVP conventions rule
- ✅ Extract workflow protocol rule
- ✅ Extract Audition Skills Map knowledge
- ✅ Extract Textbook Index knowledge
- ✅ Extract LinXin Voice style guide
- ✅ Get lab-factory relevant files
- ✅ Get transcript-compiler relevant files
- ✅ Identify scripts in lab-factory SKILL.md
- ✅ Extract code examples from SKILL.md

**Result**: All 12 integration tests pass ✅

## Key Features

### 1. Intelligent Size Handling
- Automatically detects file size
- Embeds small files (<50KB) directly
- Creates summaries for large files (≥50KB)
- Provides file size metadata for reporting

### 2. Structured Extraction
- Parses markdown into logical sections
- Supports keyword-based section finding
- Handles emoji in headers (📌, ⚠️, 🛡️)
- Preserves code blocks and formatting

### 3. Content Filtering
- Filters content by keywords with context
- Extracts code examples with language tags
- Identifies script references (.py, .jsx)
- Removes duplicates from script lists

### 4. Frontmatter Handling
- Strips YAML frontmatter from all content
- Preserves main content structure
- Handles missing or malformed frontmatter

### 5. Error Resilience
- Gracefully handles missing files
- Returns empty/default values on errors
- Provides clear error context
- Never crashes on invalid input

## Requirements Validation

This implementation satisfies the following requirements:

- ✅ **Requirement 2.1**: Extract SKILL.md core content
- ✅ **Requirement 2.2**: Identify and extract relevant rules
- ✅ **Requirement 2.3**: Identify and extract relevant knowledge
- ✅ **Requirement 2.4**: Identify and extract relevant styles
- ✅ **Requirement 2.5**: Preserve technical details and constraints
- ✅ **Requirement 2.6**: Maintain code examples and usage patterns
- ✅ **Requirement 9.5**: Handle large files with references

## Usage Example

```python
from pathlib import Path
from migration_scripts.core.content_extractor import ContentExtractor

# Extract SKILL.md content
skill_path = Path(".agent/skills/lab-factory/SKILL.md")
skill_content = ContentExtractor.extract_skill_content(skill_path)

print(skill_content['overview'])
print(skill_content['capabilities'])
print(skill_content['full_content'])

# Get relevant files for a skill
rules_dir = Path(".agent/rules")
knowledge_dir = Path(".agent/knowledge")
styles_dir = Path(".agent/styles")

rules = ContentExtractor.get_relevant_rules("lab-factory", rules_dir)
knowledge = ContentExtractor.get_relevant_knowledge("lab-factory", knowledge_dir)
styles = ContentExtractor.get_relevant_styles("lab-factory", styles_dir)

# Extract content from each file
for rule_path in rules:
    rule_content = ContentExtractor.extract_rule_content(rule_path)
    print(f"Rule: {rule_path.name}")
    print(rule_content)

# Extract knowledge with size handling
for knowledge_path in knowledge:
    knowledge_data = ContentExtractor.extract_knowledge_content(knowledge_path)
    if knowledge_data['should_embed']:
        print(f"Embedding: {knowledge_path.name}")
    else:
        print(f"Referencing: {knowledge_path.name} ({knowledge_data['file_size_kb']:.1f} KB)")
```

## Files Created

1. `migration_scripts/core/content_extractor.py` - Main implementation (400+ lines)
2. `migration_scripts/tests/test_content_extractor.py` - Unit tests (24 tests)
3. `migration_scripts/tests/test_content_extractor_integration.py` - Integration tests (12 tests)
4. `migration_scripts/TASK_4.2_SUMMARY.md` - This summary document

## Next Steps

This content extraction module is now ready to be used by:
- Task 6.1: Lab Factory Power migration
- Task 7.1: Validation Suite Power migration
- Task 8.1: Transcript Compiler Power migration

The module provides all necessary functionality to intelligently extract and filter content from the .agent directory for integration into Power documentation.

## Test Results

```
Unit Tests: 24/24 passed ✅
Integration Tests: 12/12 passed ✅
Total: 36/36 tests passing ✅
```

## Status

✅ **Task 4.2 Complete**

All requirements met, all tests passing, ready for integration with Power generation tasks.
