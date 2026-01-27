"""Basic tests to verify core modules are set up correctly."""

import pytest
from pathlib import Path
import tempfile
import shutil

from core.file_ops import FileOperations
from core.yaml_handler import YAMLHandler
from core.content_merger import ContentMerger


class TestFileOperations:
    """Test FileOperations utility class."""
    
    def test_ensure_directory_creates_directory(self):
        """Test that ensure_directory creates a new directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_dir"
            assert not test_dir.exists()
            
            FileOperations.ensure_directory(test_dir)
            assert test_dir.exists()
            assert test_dir.is_dir()
    
    def test_ensure_directory_with_nested_path(self):
        """Test that ensure_directory creates nested directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "level1" / "level2" / "level3"
            assert not test_dir.exists()
            
            FileOperations.ensure_directory(test_dir)
            assert test_dir.exists()
            assert test_dir.is_dir()
    
    def test_read_write_file(self):
        """Test reading and writing files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            content = "Hello, World!"
            
            FileOperations.write_file(test_file, content)
            assert test_file.exists()
            
            read_content = FileOperations.read_file(test_file)
            assert read_content == content
    
    def test_read_nonexistent_file_raises_error(self):
        """Test that reading a nonexistent file raises FileNotFoundError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "nonexistent.txt"
            
            with pytest.raises(FileNotFoundError):
                FileOperations.read_file(test_file)
    
    def test_file_exists(self):
        """Test file existence checking."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            
            assert not FileOperations.file_exists(test_file)
            
            test_file.write_text("content")
            assert FileOperations.file_exists(test_file)
    
    def test_get_file_size(self):
        """Test getting file size."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.txt"
            content = "Hello, World!"
            test_file.write_text(content)
            
            size = FileOperations.get_file_size(test_file)
            assert size == len(content.encode('utf-8'))


class TestYAMLHandler:
    """Test YAMLHandler utility class."""
    
    def test_create_frontmatter_valid(self):
        """Test creating valid YAML frontmatter."""
        name = "Test Power"
        description = "A test power"
        keywords = ["test", "example"]
        
        frontmatter = YAMLHandler.create_frontmatter(name, description, keywords)
        
        assert frontmatter.startswith("---\n")
        assert frontmatter.endswith("---\n")
        assert "name: Test Power" in frontmatter
        assert "description: A test power" in frontmatter
        assert "- test" in frontmatter
        assert "- example" in frontmatter
    
    def test_create_frontmatter_missing_name_raises_error(self):
        """Test that missing name raises ValueError."""
        with pytest.raises(ValueError, match="name is required"):
            YAMLHandler.create_frontmatter("", "description", ["keyword"])
    
    def test_create_frontmatter_missing_description_raises_error(self):
        """Test that missing description raises ValueError."""
        with pytest.raises(ValueError, match="description is required"):
            YAMLHandler.create_frontmatter("name", "", ["keyword"])
    
    def test_create_frontmatter_missing_keywords_raises_error(self):
        """Test that missing keywords raises ValueError."""
        with pytest.raises(ValueError, match="keyword is required"):
            YAMLHandler.create_frontmatter("name", "description", [])
    
    def test_parse_frontmatter_valid(self):
        """Test parsing valid YAML frontmatter."""
        content = """---
name: Test Power
description: A test power
keywords:
  - test
  - example
---

# Content here
"""
        frontmatter = YAMLHandler.parse_frontmatter(content)
        
        assert frontmatter['name'] == "Test Power"
        assert frontmatter['description'] == "A test power"
        assert frontmatter['keywords'] == ["test", "example"]
    
    def test_parse_frontmatter_missing_raises_error(self):
        """Test that missing frontmatter raises ValueError."""
        content = "# Just content, no frontmatter"
        
        with pytest.raises(ValueError, match="No YAML frontmatter found"):
            YAMLHandler.parse_frontmatter(content)
    
    def test_validate_frontmatter_valid(self):
        """Test validating valid frontmatter."""
        frontmatter = {
            'name': 'Test Power',
            'description': 'A test power',
            'keywords': ['test', 'example']
        }
        
        assert YAMLHandler.validate_frontmatter(frontmatter) is True
    
    def test_validate_frontmatter_missing_field(self):
        """Test validating frontmatter with missing field."""
        frontmatter = {
            'name': 'Test Power',
            'description': 'A test power'
            # Missing keywords
        }
        
        assert YAMLHandler.validate_frontmatter(frontmatter) is False
    
    def test_validate_frontmatter_empty_keywords(self):
        """Test validating frontmatter with empty keywords."""
        frontmatter = {
            'name': 'Test Power',
            'description': 'A test power',
            'keywords': []
        }
        
        assert YAMLHandler.validate_frontmatter(frontmatter) is False


class TestContentMerger:
    """Test ContentMerger utility class."""
    
    def test_strip_frontmatter(self):
        """Test stripping YAML frontmatter from content."""
        content = """---
name: Test
---

# Content here
"""
        stripped = ContentMerger._strip_frontmatter(content)
        assert stripped == "# Content here"
        assert not stripped.startswith("---")
    
    def test_should_embed_file_small_file(self):
        """Test that small files should be embedded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "small.txt"
            test_file.write_text("Small content")
            
            assert ContentMerger.should_embed_file(test_file) is True
    
    def test_should_embed_file_large_file(self):
        """Test that large files should not be embedded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "large.txt"
            # Create a file larger than 50KB
            large_content = "x" * (51 * 1024)
            test_file.write_text(large_content)
            
            assert ContentMerger.should_embed_file(test_file) is False
    
    def test_create_file_reference(self):
        """Test creating a file reference."""
        file_path = Path(".agent/knowledge/test.md")
        description = "Test knowledge file"
        
        ref = ContentMerger.create_file_reference(file_path, description)
        
        assert description in ref
        assert str(file_path) in ref
        assert "**Location**" in ref
    
    def test_create_script_documentation(self):
        """Test creating script documentation."""
        doc = ContentMerger.create_script_documentation(
            script_name="test_script.py",
            purpose="Test script for validation",
            location=Path(".agent/scripts/test_script.py"),
            usage_example="python test_script.py --arg value",
            parameters={"--arg": "Test argument"},
            dependencies=["pytest"],
            execution_context="Run from project root"
        )
        
        assert "### test_script.py" in doc
        assert "**Purpose**" in doc
        assert "**Location**" in doc
        assert "**Usage**" in doc
        assert "**Parameters**" in doc
        assert "**Dependencies**" in doc
        assert "**Execution Context**" in doc
    
    def test_extract_code_blocks(self):
        """Test extracting code blocks from markdown."""
        content = """
# Title

Some text

```python
def hello():
    print("Hello")
```

More text

```bash
echo "test"
```
"""
        blocks = ContentMerger.extract_code_blocks(content)
        
        assert len(blocks) == 2
        assert 'def hello():' in blocks[0]
        assert 'echo "test"' in blocks[1]


def test_imports_work():
    """Test that all core modules can be imported."""
    from core import FileOperations, YAMLHandler, ContentMerger
    
    assert FileOperations is not None
    assert YAMLHandler is not None
    assert ContentMerger is not None
