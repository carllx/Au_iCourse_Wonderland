"""Unit tests for ContentMerger class."""

import pytest
from pathlib import Path
import tempfile
import shutil
from migration_scripts.core.content_merger import ContentMerger


class TestContentMerger:
    """Test suite for ContentMerger functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for test files."""
        temp_path = Path(tempfile.mkdtemp())
        yield temp_path
        shutil.rmtree(temp_path)
    
    def test_merge_markdown_files_basic(self, temp_dir):
        """Test basic merging of multiple markdown files."""
        # Create test files
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        
        file1.write_text("# File 1\n\nContent from file 1.")
        file2.write_text("# File 2\n\nContent from file 2.")
        
        # Merge files
        files = [
            (file1, "Section 1"),
            (file2, "Section 2")
        ]
        result = ContentMerger.merge_markdown_files(files)
        
        # Verify both sections are present
        assert "## Section 1" in result
        assert "## Section 2" in result
        assert "Content from file 1" in result
        assert "Content from file 2" in result
    
    def test_merge_markdown_files_missing_file(self, temp_dir):
        """Test merging when a file is missing."""
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "missing.md"
        
        file1.write_text("# File 1\n\nContent from file 1.")
        
        files = [
            (file1, "Section 1"),
            (file2, "Section 2")
        ]
        result = ContentMerger.merge_markdown_files(files)
        
        # Verify file1 content is present
        assert "Content from file 1" in result
        # Verify missing file is noted
        assert "Source file not found" in result
        assert str(file2) in result
    
    def test_strip_frontmatter(self):
        """Test YAML frontmatter removal."""
        content_with_frontmatter = """---
name: Test
description: Test description
---

# Main Content

This is the actual content."""
        
        result = ContentMerger._strip_frontmatter(content_with_frontmatter)
        
        assert "---" not in result
        assert "name: Test" not in result
        assert "# Main Content" in result
        assert "This is the actual content" in result
    
    def test_strip_frontmatter_no_frontmatter(self):
        """Test content without frontmatter is unchanged."""
        content = "# Main Content\n\nThis is content."
        result = ContentMerger._strip_frontmatter(content)
        assert result == content.strip()
    
    def test_should_embed_file_small(self, temp_dir):
        """Test that small files should be embedded."""
        small_file = temp_dir / "small.md"
        small_file.write_text("Small content" * 100)  # ~1.3KB
        
        assert ContentMerger.should_embed_file(small_file) is True
    
    def test_should_embed_file_large(self, temp_dir):
        """Test that large files should not be embedded."""
        large_file = temp_dir / "large.md"
        # Create a file larger than 50KB
        large_file.write_text("Large content " * 5000)  # ~65KB
        
        assert ContentMerger.should_embed_file(large_file) is False
    
    def test_should_embed_file_missing(self, temp_dir):
        """Test that missing files return False."""
        missing_file = temp_dir / "missing.md"
        assert ContentMerger.should_embed_file(missing_file) is False
    
    def test_create_file_reference(self, temp_dir):
        """Test file reference creation."""
        test_file = temp_dir / "test.md"
        test_file.write_text("Test content")
        
        result = ContentMerger.create_file_reference(
            test_file,
            "This is a test file"
        )
        
        assert "This is a test file" in result
        assert f"`{test_file}`" in result
        assert "File size:" in result
    
    def test_create_script_documentation_full(self):
        """Test script documentation with all parameters."""
        result = ContentMerger.create_script_documentation(
            script_name="test_script.py",
            purpose="Test script for validation",
            location=Path(".agent/scripts/test_script.py"),
            usage_example="python3 .agent/scripts/test_script.py --file test.md",
            parameters={
                "--file": "Path to the file to validate",
                "--verbose": "Enable verbose output"
            },
            dependencies=["pytest", "pyyaml"],
            execution_context="Must be run from project root"
        )
        
        assert "### test_script.py" in result
        assert "**Purpose**: Test script for validation" in result
        assert "**Location**:" in result
        assert "**Usage**:" in result
        assert "```bash" in result
        assert "--file" in result
        assert "--verbose" in result
        assert "**Dependencies**:" in result
        assert "pytest" in result
        assert "**Execution Context**: Must be run from project root" in result
    
    def test_create_script_documentation_minimal(self):
        """Test script documentation with minimal parameters."""
        result = ContentMerger.create_script_documentation(
            script_name="simple.py",
            purpose="Simple script",
            location=Path("simple.py"),
            usage_example="python3 simple.py"
        )
        
        assert "### simple.py" in result
        assert "**Purpose**: Simple script" in result
        assert "**Usage**:" in result
        # Should not have optional sections
        assert "**Parameters**:" not in result
        assert "**Dependencies**:" not in result
        assert "**Execution Context**:" not in result
    
    def test_extract_code_blocks(self):
        """Test extraction of code blocks from markdown."""
        content = """
# Test Document

Some text here.

```python
def hello():
    print("Hello")
```

More text.

```bash
echo "test"
```

Final text.
"""
        
        blocks = ContentMerger.extract_code_blocks(content)
        
        assert len(blocks) == 2
        assert 'def hello():' in blocks[0]
        assert 'echo "test"' in blocks[1]
    
    def test_extract_code_blocks_no_blocks(self):
        """Test extraction when no code blocks present."""
        content = "# Test\n\nJust regular text."
        blocks = ContentMerger.extract_code_blocks(content)
        assert len(blocks) == 0
    
    def test_preserve_formatting(self):
        """Test that formatting is preserved correctly."""
        content = """
# Header


## Subheader
Text here.


```python
code
```


More text.
"""
        
        result = ContentMerger.preserve_formatting(content)
        
        # Should have proper spacing around headers
        assert "# Header" in result
        assert "\n\n## Subheader" in result
        # Should have proper spacing around code blocks
        assert "\n\n```python" in result
        # Should not have more than 2 consecutive newlines
        assert "\n\n\n" not in result
    
    def test_add_section_prefix(self):
        """Test adding prefix to section headers."""
        content = """# Main Title

## Subsection

### Deep Section

Regular text."""
        
        result = ContentMerger.add_section_prefix(content, "Rules: ")
        
        assert "# Rules: Main Title" in result
        assert "## Rules: Subsection" in result
        assert "### Rules: Deep Section" in result
        assert "Regular text." in result
    
    def test_add_section_suffix(self):
        """Test adding suffix to section headers."""
        content = """# Main Title

## Subsection

Regular text."""
        
        result = ContentMerger.add_section_suffix(content, " (from Knowledge)")
        
        assert "# Main Title (from Knowledge)" in result
        assert "## Subsection (from Knowledge)" in result
        assert "Regular text." in result
    
    def test_detect_heading_conflicts_no_conflicts(self):
        """Test conflict detection when no conflicts exist."""
        contents = [
            ("# Unique Header 1\n\n## Subsection A", "file1"),
            ("# Unique Header 2\n\n## Subsection B", "file2")
        ]
        
        conflicts = ContentMerger.detect_heading_conflicts(contents)
        
        assert len(conflicts) == 0
    
    def test_detect_heading_conflicts_with_conflicts(self):
        """Test conflict detection when conflicts exist."""
        contents = [
            ("# Overview\n\n## Setup", "file1"),
            ("# Overview\n\n## Configuration", "file2"),
            ("# Different\n\n## Setup", "file3")
        ]
        
        conflicts = ContentMerger.detect_heading_conflicts(contents)
        
        # "Overview" appears in file1 and file2
        assert "Overview" in conflicts
        assert set(conflicts["Overview"]) == {"file1", "file2"}
        
        # "Setup" appears in file1 and file3
        assert "Setup" in conflicts
        assert set(conflicts["Setup"]) == {"file1", "file3"}
        
        # "Different" and "Configuration" are unique
        assert "Different" not in conflicts
        assert "Configuration" not in conflicts
    
    def test_resolve_heading_conflicts_with_prefix(self, temp_dir):
        """Test resolving heading conflicts using prefix strategy."""
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        
        file1.write_text("# Overview\n\nContent 1")
        file2.write_text("# Overview\n\nContent 2")
        
        files = [
            (file1, "Section 1", "File1: "),
            (file2, "Section 2", "File2: ")
        ]
        
        results = ContentMerger.resolve_heading_conflicts(files, strategy="prefix")
        
        assert len(results) == 2
        assert "# File1: Overview" in results[0][0]
        assert "Content 1" in results[0][0]
        assert "# File2: Overview" in results[1][0]
        assert "Content 2" in results[1][0]
    
    def test_resolve_heading_conflicts_with_suffix(self, temp_dir):
        """Test resolving heading conflicts using suffix strategy."""
        file1 = temp_dir / "file1.md"
        file2 = temp_dir / "file2.md"
        
        file1.write_text("# Setup\n\nSetup content")
        file2.write_text("# Setup\n\nDifferent setup")
        
        files = [
            (file1, "Section 1", " (Rules)"),
            (file2, "Section 2", " (Knowledge)")
        ]
        
        results = ContentMerger.resolve_heading_conflicts(files, strategy="suffix")
        
        assert len(results) == 2
        assert "# Setup (Rules)" in results[0][0]
        assert "Setup content" in results[0][0]
        assert "# Setup (Knowledge)" in results[1][0]
        assert "Different setup" in results[1][0]
    
    def test_resolve_heading_conflicts_no_modifier(self, temp_dir):
        """Test resolving when no modifier is provided."""
        file1 = temp_dir / "file1.md"
        
        file1.write_text("# Title\n\nContent")
        
        files = [
            (file1, "Section 1")  # No modifier
        ]
        
        results = ContentMerger.resolve_heading_conflicts(files)
        
        assert len(results) == 1
        # Should not modify headers when no modifier provided
        assert "# Title" in results[0][0]
        assert "Content" in results[0][0]
    
    def test_merge_preserves_code_blocks(self, temp_dir):
        """Test that code blocks are preserved during merging."""
        file1 = temp_dir / "file1.md"
        
        content = """# Documentation

Example code:

```python
def example():
    return "test"
```

More text."""
        
        file1.write_text(content)
        
        files = [(file1, "Code Example")]
        result = ContentMerger.merge_markdown_files(files)
        
        # Verify code block is preserved
        assert "```python" in result
        assert 'def example():' in result
        assert 'return "test"' in result
        assert "```" in result
    
    def test_merge_preserves_inline_code(self, temp_dir):
        """Test that inline code is preserved during merging."""
        file1 = temp_dir / "file1.md"
        
        content = "Use the `merge_files()` function to combine documents."
        file1.write_text(content)
        
        files = [(file1, "Instructions")]
        result = ContentMerger.merge_markdown_files(files)
        
        assert "`merge_files()`" in result
    
    def test_merge_handles_special_characters(self, temp_dir):
        """Test that special characters are preserved."""
        file1 = temp_dir / "file1.md"
        
        content = """# Special Characters

- Bullet points
- With *emphasis* and **bold**
- And [links](http://example.com)

> Blockquote text

1. Numbered list
2. Second item"""
        
        file1.write_text(content)
        
        files = [(file1, "Formatting")]
        result = ContentMerger.merge_markdown_files(files)
        
        assert "*emphasis*" in result
        assert "**bold**" in result
        assert "[links](http://example.com)" in result
        assert "> Blockquote" in result
        assert "1. Numbered list" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
