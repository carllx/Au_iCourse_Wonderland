"""Unit tests for ContentExtractor class."""

import pytest
from pathlib import Path
import tempfile
import shutil
from migration_scripts.core.content_extractor import ContentExtractor


class TestContentExtractor:
    """Test suite for ContentExtractor functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        shutil.rmtree(temp_path)
    
    @pytest.fixture
    def sample_skill_md(self, temp_dir):
        """Create a sample SKILL.md file."""
        content = """---
name: Test Skill
id: test-skill
---

# Test Skill

## 概述

This is the overview section with core description.

## 核心架构：工具包

This section describes the core capabilities and features.

### API Functions

- `function1()`: Does something
- `function2()`: Does something else

## 使用策略

Usage instructions go here.

```javascript
// Example code
function example() {
    return "test";
}
```

## 📌 依赖文件

- lib/core.jsx
- lib/utils.jsx

## ⚠️ 已知局限

Known limitations:
1. Cannot do X
2. Cannot do Y

## 🛡️ 鲁棒性协议

Robustness protocols and best practices.
"""
        skill_file = temp_dir / "SKILL.md"
        skill_file.write_text(content)
        return skill_file
    
    def test_extract_skill_content_full(self, sample_skill_md):
        """Test extracting all sections from a SKILL.md file."""
        result = ContentExtractor.extract_skill_content(sample_skill_md)
        
        assert 'overview' in result
        assert 'capabilities' in result
        assert 'usage' in result
        assert 'dependencies' in result
        assert 'limitations' in result
        assert 'protocols' in result
        assert 'full_content' in result
        
        # Check that sections contain expected content
        assert "overview section" in result['overview']
        assert "core capabilities" in result['capabilities']
        assert "Usage instructions" in result['usage']
        assert "lib/core.jsx" in result['dependencies']
        assert "Cannot do X" in result['limitations']
        assert "Robustness protocols" in result['protocols']
        
        # Check that frontmatter is stripped from full_content
        assert "name: Test Skill" not in result['full_content']
        assert "# Test Skill" in result['full_content']
    
    def test_extract_skill_content_missing_file(self, temp_dir):
        """Test extracting from a non-existent file."""
        missing_file = temp_dir / "missing.md"
        result = ContentExtractor.extract_skill_content(missing_file)
        
        # Should return empty sections
        assert result['overview'] == ''
        assert result['capabilities'] == ''
        assert result['full_content'] == ''
    
    def test_extract_rule_content(self, temp_dir):
        """Test extracting content from a rule file."""
        rule_content = """---
trigger: glob
description: Test rule
---

# Test Rule

This is a rule that applies to specific contexts.

## Guidelines

- Follow convention A
- Follow convention B
"""
        rule_file = temp_dir / "rule_test.md"
        rule_file.write_text(rule_content)
        
        result = ContentExtractor.extract_rule_content(rule_file)
        
        assert "# Test Rule" in result
        assert "Follow convention A" in result
        assert "trigger: glob" not in result  # Frontmatter should be stripped
    
    def test_extract_knowledge_content_small_file(self, temp_dir):
        """Test extracting from a small knowledge file (should embed)."""
        knowledge_content = """# Knowledge Base

This is a small knowledge file with useful information.

## Section 1

Content here.

## Section 2

More content.
"""
        knowledge_file = temp_dir / "knowledge.md"
        knowledge_file.write_text(knowledge_content)
        
        result = ContentExtractor.extract_knowledge_content(knowledge_file)
        
        assert result['should_embed'] is True
        assert "Knowledge Base" in result['content']
        assert result['file_size_kb'] < 50
    
    def test_extract_knowledge_content_large_file(self, temp_dir):
        """Test extracting from a large knowledge file (should reference)."""
        # Create a file larger than 50KB
        large_content = "# Large Knowledge Base\n\n" + ("Large content line.\n" * 5000)
        knowledge_file = temp_dir / "large_knowledge.md"
        knowledge_file.write_text(large_content)
        
        result = ContentExtractor.extract_knowledge_content(knowledge_file, max_size_kb=50)
        
        assert result['should_embed'] is False
        assert result['file_size_kb'] > 50
        # Should contain a summary, not full content
        assert "[Content truncated" in result['content'] or len(result['content']) < len(large_content)
    
    def test_extract_style_content(self, temp_dir):
        """Test extracting content from a style guide."""
        style_content = """---
name: Style Guide
---

# Style Guide

## Voice and Tone

Use a friendly, professional tone.

## Formatting

- Use bullet points
- Keep paragraphs short
"""
        style_file = temp_dir / "style.md"
        style_file.write_text(style_content)
        
        result = ContentExtractor.extract_style_content(style_file)
        
        assert "# Style Guide" in result
        assert "friendly, professional tone" in result
        assert "name: Style Guide" not in result  # Frontmatter stripped
    
    def test_get_relevant_rules(self, temp_dir):
        """Test getting relevant rules for a skill."""
        # Create rule files
        rules_dir = temp_dir / "rules"
        rules_dir.mkdir()
        
        (rules_dir / "rule_mvp_conventions.md").write_text("# MVP Conventions")
        (rules_dir / "rule_workflow_protocol.md").write_text("# Workflow Protocol")
        (rules_dir / "rule_other.md").write_text("# Other Rule")
        
        # Test lab-factory skill
        lab_rules = ContentExtractor.get_relevant_rules("lab-factory", rules_dir)
        assert len(lab_rules) == 1
        assert lab_rules[0].name == "rule_mvp_conventions.md"
        
        # Test transcript-compiler skill
        transcript_rules = ContentExtractor.get_relevant_rules("transcript-compiler", rules_dir)
        assert len(transcript_rules) == 1  # Only one exists
        assert transcript_rules[0].name == "rule_workflow_protocol.md"
        
        # Test validation-suite skill (no rules)
        validation_rules = ContentExtractor.get_relevant_rules("validation-suite", rules_dir)
        assert len(validation_rules) == 0
    
    def test_get_relevant_knowledge(self, temp_dir):
        """Test getting relevant knowledge files for a skill."""
        knowledge_dir = temp_dir / "knowledge"
        knowledge_dir.mkdir()
        
        (knowledge_dir / "Audition_Skills_Map.md").write_text("# Audition Skills")
        (knowledge_dir / "Textbook_Index.md").write_text("# Textbook Index")
        
        # Test lab-factory skill
        lab_knowledge = ContentExtractor.get_relevant_knowledge("lab-factory", knowledge_dir)
        assert len(lab_knowledge) == 1
        assert lab_knowledge[0].name == "Audition_Skills_Map.md"
        
        # Test transcript-compiler skill
        transcript_knowledge = ContentExtractor.get_relevant_knowledge("transcript-compiler", knowledge_dir)
        assert len(transcript_knowledge) == 1  # Only one exists
        assert transcript_knowledge[0].name == "Textbook_Index.md"
    
    def test_get_relevant_styles(self, temp_dir):
        """Test getting relevant style guides for a skill."""
        styles_dir = temp_dir / "styles"
        styles_dir.mkdir()
        
        (styles_dir / "LinXin_Voice.md").write_text("# LinXin Voice")
        (styles_dir / "Visual_Design_System.md").write_text("# Visual Design")
        
        # Test transcript-compiler skill
        transcript_styles = ContentExtractor.get_relevant_styles("transcript-compiler", styles_dir)
        assert len(transcript_styles) == 1
        assert transcript_styles[0].name == "LinXin_Voice.md"
        
        # Test lab-factory skill (no styles)
        lab_styles = ContentExtractor.get_relevant_styles("lab-factory", styles_dir)
        assert len(lab_styles) == 0
    
    def test_strip_frontmatter(self):
        """Test YAML frontmatter removal."""
        content_with_frontmatter = """---
name: Test
description: Test description
keywords: [test, example]
---

# Main Content

This is the actual content."""
        
        result = ContentExtractor._strip_frontmatter(content_with_frontmatter)
        
        assert "---" not in result
        assert "name: Test" not in result
        assert "# Main Content" in result
        assert "This is the actual content" in result
    
    def test_strip_frontmatter_no_frontmatter(self):
        """Test content without frontmatter is unchanged."""
        content = "# Main Content\n\nThis is content."
        result = ContentExtractor._strip_frontmatter(content)
        assert result == content.strip()
    
    def test_extract_sections(self):
        """Test extracting sections from markdown."""
        content = """# Main Title

Introduction text.

## Section 1

Content for section 1.

### Subsection 1.1

Subsection content.

## Section 2

Content for section 2.
"""
        
        sections = ContentExtractor._extract_sections(content)
        
        assert "Main Title" in sections
        assert "Section 1" in sections
        assert "Subsection 1.1" in sections
        assert "Section 2" in sections
        
        assert "Introduction text" in sections["Main Title"]
        assert "Content for section 1" in sections["Section 1"]
    
    def test_find_section(self):
        """Test finding sections by keywords."""
        sections = {
            "Overview": "This is the overview.",
            "Core Features": "These are the features.",
            "Usage Instructions": "How to use it."
        }
        
        # Test finding by exact match
        result = ContentExtractor._find_section(sections, ["Overview"])
        assert result == "This is the overview."
        
        # Test finding by partial match
        result = ContentExtractor._find_section(sections, ["Features"])
        assert result == "These are the features."
        
        # Test finding by multiple keywords
        result = ContentExtractor._find_section(sections, ["Usage", "Instructions"])
        assert result == "How to use it."
        
        # Test not finding
        result = ContentExtractor._find_section(sections, ["Nonexistent"])
        assert result == ""
    
    def test_extract_summary(self):
        """Test extracting summary from content."""
        content = """# Title

First paragraph.

Second paragraph.

## Section 1

Content 1.

## Section 2

Content 2.

## Section 3

Content 3.
"""
        
        summary = ContentExtractor._extract_summary(content, max_lines=10)
        
        # Should include first section but not all
        assert "# Title" in summary
        assert "First paragraph" in summary
        assert "Section 1" in summary
        # Should indicate truncation
        assert "[Content truncated" in summary or "Section 3" not in summary
    
    def test_extract_code_examples(self):
        """Test extracting code examples from markdown."""
        content = """# Documentation

Some text.

```python
def hello():
    print("Hello")
```

More text.

```javascript
function test() {
    return true;
}
```

```
Plain code block
```
"""
        
        examples = ContentExtractor.extract_code_examples(content)
        
        assert len(examples) == 3
        
        # Check Python example
        assert examples[0]['language'] == 'python'
        assert 'def hello():' in examples[0]['code']
        
        # Check JavaScript example
        assert examples[1]['language'] == 'javascript'
        assert 'function test()' in examples[1]['code']
        
        # Check plain code block
        assert examples[2]['language'] == 'text'
        assert 'Plain code block' in examples[2]['code']
    
    def test_filter_relevant_content(self):
        """Test filtering content by keywords."""
        content = """# Document

Line 1: Introduction
Line 2: More intro
Line 3: Important keyword here
Line 4: Following line
Line 5: Another line
Line 6: Unrelated content
Line 7: More unrelated
Line 8: Another keyword mention
Line 9: Final line
"""
        
        filtered = ContentExtractor.filter_relevant_content(
            content,
            keywords=["keyword"],
            context_lines=1
        )
        
        # Should include lines with keyword and 1 line of context
        assert "Line 2" in filtered  # Context before
        assert "Line 3" in filtered  # Match
        assert "Line 4" in filtered  # Context after
        assert "Line 7" in filtered  # Context before
        assert "Line 8" in filtered  # Match
        assert "Line 9" in filtered  # Context after
        
        # Should not include unrelated lines far from matches
        # (Note: Line 6 might be included if it's within context of either match)
    
    def test_filter_relevant_content_no_keywords(self):
        """Test filtering with no keywords returns full content."""
        content = "# Test\n\nFull content here."
        filtered = ContentExtractor.filter_relevant_content(content, keywords=[])
        assert filtered == content
    
    def test_identify_script_references(self):
        """Test identifying script references in content."""
        content = """# Documentation

Use the script at `.agent/scripts/test.py` for validation.

The JSX library is located at `lib/Audition.jsx`.

Run `python3 .agent/executors/build_factory.py --task writer`.

Also see [another_script.jsx](path/to/another_script.jsx).
"""
        
        scripts = ContentExtractor.identify_script_references(content)
        
        # Should find all script references
        script_paths = [s['path'] for s in scripts]
        
        assert any('test.py' in path for path in script_paths)
        assert any('Audition.jsx' in path for path in script_paths)
        assert any('build_factory.py' in path for path in script_paths)
        assert any('another_script.jsx' in path for path in script_paths)
        
        # Check script types
        py_scripts = [s for s in scripts if s['type'] == 'python']
        jsx_scripts = [s for s in scripts if s['type'] == 'jsx']
        
        assert len(py_scripts) >= 2  # test.py and build_factory.py
        assert len(jsx_scripts) >= 2  # Audition.jsx and another_script.jsx
    
    def test_identify_script_references_no_duplicates(self):
        """Test that duplicate script references are removed."""
        content = """
Use `script.py` here.
And also use `script.py` there.
The same `script.py` again.
"""
        
        scripts = ContentExtractor.identify_script_references(content)
        
        # Should only have one entry for script.py
        assert len(scripts) == 1
        assert scripts[0]['path'] == 'script.py'
    
    def test_extract_sections_with_emoji_headers(self):
        """Test extracting sections with emoji in headers."""
        content = """# Main

## 📌 Dependencies

List of dependencies.

## ⚠️ Warnings

Important warnings.

## 🛡️ Protocols

Security protocols.
"""
        
        sections = ContentExtractor._extract_sections(content)
        
        assert "📌 Dependencies" in sections
        assert "⚠️ Warnings" in sections
        assert "🛡️ Protocols" in sections
        
        assert "List of dependencies" in sections["📌 Dependencies"]
    
    def test_extract_skill_content_with_code_blocks(self, temp_dir):
        """Test that code blocks are preserved in extracted content."""
        content = """---
name: Test
---

# Skill

## Usage

Example:

```python
def example():
    return "test"
```

More text.
"""
        skill_file = temp_dir / "skill.md"
        skill_file.write_text(content)
        
        result = ContentExtractor.extract_skill_content(skill_file)
        
        # Code blocks should be preserved
        assert "```python" in result['full_content']
        assert "def example():" in result['full_content']
        assert "```" in result['full_content']
    
    def test_skill_rules_map_completeness(self):
        """Test that SKILL_RULES_MAP covers all expected skills."""
        expected_skills = ["lab-factory", "validation-suite", "transcript-compiler"]
        
        for skill in expected_skills:
            assert skill in ContentExtractor.SKILL_RULES_MAP
    
    def test_skill_knowledge_map_completeness(self):
        """Test that SKILL_KNOWLEDGE_MAP covers all expected skills."""
        expected_skills = ["lab-factory", "validation-suite", "transcript-compiler"]
        
        for skill in expected_skills:
            assert skill in ContentExtractor.SKILL_KNOWLEDGE_MAP
    
    def test_skill_styles_map_completeness(self):
        """Test that SKILL_STYLES_MAP covers all expected skills."""
        expected_skills = ["lab-factory", "validation-suite", "transcript-compiler"]
        
        for skill in expected_skills:
            assert skill in ContentExtractor.SKILL_STYLES_MAP


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
