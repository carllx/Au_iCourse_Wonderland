"""Tests for script reference template functionality."""

import pytest
from pathlib import Path
from migration_scripts.core.content_merger import ContentMerger


class TestScriptDocumentationTemplate:
    """Test suite for script documentation template."""
    
    def test_minimal_script_documentation(self):
        """Test creating script documentation with only required fields."""
        doc = ContentMerger.create_script_documentation(
            script_name="test_script.py",
            purpose="Test script for validation",
            location=Path(".agent/scripts/test_script.py"),
            usage_example="python3 .agent/scripts/test_script.py"
        )
        
        # Verify required sections are present
        assert "### test_script.py" in doc
        assert "**Purpose**: Test script for validation" in doc
        assert "**Location**: `.agent/scripts/test_script.py`" in doc
        assert "**Usage**:" in doc
        assert "```bash" in doc
        assert "python3 .agent/scripts/test_script.py" in doc
    
    def test_full_script_documentation(self):
        """Test creating script documentation with all fields."""
        doc = ContentMerger.create_script_documentation(
            script_name="validate_links.py",
            purpose="Validates all internal and external links in markdown files",
            location=Path(".agent/skills/validation-suite/scripts/validate_links.py"),
            usage_example="python3 .agent/skills/validation-suite/scripts/validate_links.py",
            parameters={
                "--file": "Specific file to validate (optional)",
                "--verbose": "Enable verbose output"
            },
            dependencies=[
                "Python 3.8+",
                "requests library",
                "markdown parser"
            ],
            execution_context="Run from project root directory"
        )
        
        # Verify all sections are present
        assert "### validate_links.py" in doc
        assert "**Purpose**: Validates all internal and external links" in doc
        assert "**Location**: `.agent/skills/validation-suite/scripts/validate_links.py`" in doc
        assert "**Usage**:" in doc
        assert "**Parameters**:" in doc
        assert "`--file`: Specific file to validate" in doc
        assert "`--verbose`: Enable verbose output" in doc
        assert "**Dependencies**:" in doc
        assert "Python 3.8+" in doc
        assert "requests library" in doc
        assert "markdown parser" in doc
        assert "**Execution Context**: Run from project root directory" in doc
    
    def test_jsx_script_documentation(self):
        """Test documenting a JSX library file."""
        doc = ContentMerger.create_script_documentation(
            script_name="Audition.jsx",
            purpose="Core library providing Adobe Audition automation API",
            location=Path(".agent/skills/lab-factory/lib/Audition.jsx"),
            usage_example='// Include in manifest.json\n{"includes": [".agent/skills/lab-factory/lib/Audition.jsx"]}',
            dependencies=[
                "Adobe Audition CC 2019 or later",
                "ExtendScript engine"
            ],
            execution_context="Loaded via Adobe Audition's ExtendScript manifest system"
        )
        
        assert "### Audition.jsx" in doc
        assert "Adobe Audition automation API" in doc
        assert ".agent/skills/lab-factory/lib/Audition.jsx" in doc
        assert "Adobe Audition CC 2019" in doc
        assert "ExtendScript manifest system" in doc
    
    def test_executor_script_documentation(self):
        """Test documenting an executor script with multiple parameters."""
        doc = ContentMerger.create_script_documentation(
            script_name="build_factory.py",
            purpose="Automates transcript compilation and quality auditing",
            location=Path(".agent/executors/build_factory.py"),
            usage_example="python3 .agent/executors/build_factory.py --task writer --section S02",
            parameters={
                "--task": "Task mode (writer, auditor)",
                "--section": "Section identifier (e.g., S02)",
                "--file": "File path for auditor mode"
            },
            dependencies=[
                "Python 3.8+",
                "OpenAI API key (set in environment)",
                "Project structure files (Structure_Map, Performance_Map)"
            ],
            execution_context="Run from project root directory with proper environment variables set"
        )
        
        assert "### build_factory.py" in doc
        assert "transcript compilation and quality auditing" in doc
        assert "`--task`: Task mode (writer, auditor)" in doc
        assert "`--section`: Section identifier" in doc
        assert "`--file`: File path for auditor mode" in doc
        assert "OpenAI API key" in doc
        assert "environment variables" in doc
    
    def test_script_documentation_format(self):
        """Test that documentation follows markdown format correctly."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test purpose",
            location=Path("test/path.py"),
            usage_example="python test/path.py"
        )
        
        # Check markdown structure
        lines = doc.split('\n')
        assert lines[0] == "### test.py"
        assert lines[2] == "**Purpose**: Test purpose"
        assert lines[4] == "**Location**: `test/path.py`"
        assert lines[6] == "**Usage**:"
        assert lines[7] == "```bash"
        assert lines[8] == "python test/path.py"
        assert lines[9] == "```"
    
    def test_parameters_formatting(self):
        """Test that parameters are formatted as a list."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example="python test.py",
            parameters={
                "--param1": "First parameter",
                "--param2": "Second parameter",
                "--param3": "Third parameter"
            }
        )
        
        # Check parameters section
        assert "**Parameters**:" in doc
        assert "- `--param1`: First parameter" in doc
        assert "- `--param2`: Second parameter" in doc
        assert "- `--param3`: Third parameter" in doc
    
    def test_dependencies_formatting(self):
        """Test that dependencies are formatted as a list."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example="python test.py",
            dependencies=[
                "Dependency 1",
                "Dependency 2",
                "Dependency 3"
            ]
        )
        
        # Check dependencies section
        assert "**Dependencies**:" in doc
        assert "- Dependency 1" in doc
        assert "- Dependency 2" in doc
        assert "- Dependency 3" in doc
    
    def test_no_optional_sections_when_not_provided(self):
        """Test that optional sections are not included when not provided."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example="python test.py"
        )
        
        # Optional sections should not be present
        assert "**Parameters**:" not in doc
        assert "**Dependencies**:" not in doc
        assert "**Execution Context**:" not in doc
    
    def test_empty_parameters_dict(self):
        """Test handling of empty parameters dictionary."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example="python test.py",
            parameters={}
        )
        
        # Empty dict should not create parameters section
        assert "**Parameters**:" not in doc
    
    def test_empty_dependencies_list(self):
        """Test handling of empty dependencies list."""
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example="python test.py",
            dependencies=[]
        )
        
        # Empty list should not create dependencies section
        assert "**Dependencies**:" not in doc
    
    def test_multiline_usage_example(self):
        """Test that multiline usage examples are preserved."""
        usage = """python3 script.py \\
    --param1 value1 \\
    --param2 value2 \\
    --param3 value3"""
        
        doc = ContentMerger.create_script_documentation(
            script_name="test.py",
            purpose="Test",
            location=Path("test.py"),
            usage_example=usage
        )
        
        assert "python3 script.py" in doc
        assert "--param1 value1" in doc
        assert "--param2 value2" in doc
        assert "--param3 value3" in doc
    
    def test_special_characters_in_path(self):
        """Test handling of special characters in file paths."""
        doc = ContentMerger.create_script_documentation(
            script_name="test-script_v2.py",
            purpose="Test",
            location=Path(".agent/skills/test-suite/scripts/test-script_v2.py"),
            usage_example="python test.py"
        )
        
        assert ".agent/skills/test-suite/scripts/test-script_v2.py" in doc
    
    def test_requirements_coverage(self):
        """Test that template covers all requirements 3.3, 3.4, 3.5, 3.6."""
        doc = ContentMerger.create_script_documentation(
            script_name="comprehensive_test.py",
            purpose="Comprehensive test script",
            location=Path(".agent/scripts/comprehensive_test.py"),  # Req 3.3: path
            usage_example="python3 .agent/scripts/comprehensive_test.py --arg value",  # Req 3.4: usage
            parameters={"--arg": "Test argument"},
            dependencies=["Python 3.8+", "pytest"],  # Req 3.5: dependencies
            execution_context="Run from project root"  # Req 3.6: execution context
        )
        
        # Requirement 3.3: Script locations with paths
        assert "**Location**:" in doc
        assert ".agent/scripts/comprehensive_test.py" in doc
        
        # Requirement 3.4: Usage instructions with command-line examples
        assert "**Usage**:" in doc
        assert "```bash" in doc
        assert "python3 .agent/scripts/comprehensive_test.py --arg value" in doc
        
        # Requirement 3.5: Script dependencies and prerequisites
        assert "**Dependencies**:" in doc
        assert "Python 3.8+" in doc
        assert "pytest" in doc
        
        # Requirement 3.6: Required execution context
        assert "**Execution Context**:" in doc
        assert "Run from project root" in doc


class TestScriptTemplateIntegration:
    """Integration tests for script template usage in migration."""
    
    def test_multiple_scripts_documentation(self):
        """Test documenting multiple scripts for a Power."""
        scripts = []
        
        # Document validation scripts
        scripts.append(ContentMerger.create_script_documentation(
            script_name="validate_links.py",
            purpose="Validates all internal and external links",
            location=Path(".agent/skills/validation-suite/scripts/validate_links.py"),
            usage_example="python3 .agent/skills/validation-suite/scripts/validate_links.py"
        ))
        
        scripts.append(ContentMerger.create_script_documentation(
            script_name="validate_script_length.py",
            purpose="Checks script length against standards",
            location=Path(".agent/skills/validation-suite/scripts/validate_script_length.py"),
            usage_example="python3 .agent/skills/validation-suite/scripts/validate_script_length.py --file path/to/script.md",
            parameters={"--file": "Path to script file to validate"}
        ))
        
        # Combine into a section
        combined = "\n## Script References\n\n" + "\n".join(scripts)
        
        # Verify both scripts are documented
        assert "### validate_links.py" in combined
        assert "### validate_script_length.py" in combined
        assert combined.count("**Purpose**:") == 2
        assert combined.count("**Location**:") == 2
        assert combined.count("**Usage**:") == 2
    
    def test_script_documentation_in_power_context(self):
        """Test that script documentation fits well in a Power's power.md."""
        # Simulate a section of power.md
        power_content = """# Validation Suite Power

## Overview
This Power provides validation tools for project health checks.

## Script References

"""
        
        # Add script documentation
        script_doc = ContentMerger.create_script_documentation(
            script_name="validate_consistency.py",
            purpose="Validates consistency across project files",
            location=Path(".agent/skills/validation-suite/scripts/validate_consistency.py"),
            usage_example="python3 .agent/skills/validation-suite/scripts/validate_consistency.py",
            dependencies=["Python 3.8+"],
            execution_context="Run from project root directory"
        )
        
        power_content += script_doc
        
        # Verify structure
        assert "# Validation Suite Power" in power_content
        assert "## Script References" in power_content
        assert "### validate_consistency.py" in power_content
        # Count headers more precisely
        assert power_content.count("\n## ") == 2  # Two level-2 headers
        assert power_content.count("\n### ") == 1  # One level-3 header


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
