"""Tests for script scanning and documentation generation."""

import pytest
from pathlib import Path
import tempfile
import shutil
from migration_scripts.core.script_scanner import ScriptScanner, ScriptInfo


class TestScriptInfo:
    """Tests for ScriptInfo class."""
    
    def test_script_info_creation(self):
        """Test creating a ScriptInfo object."""
        script = ScriptInfo(
            name="test.py",
            path=Path("/path/to/test.py"),
            script_type="python",
            skill="test-skill"
        )
        
        assert script.name == "test.py"
        assert script.path == Path("/path/to/test.py")
        assert script.script_type == "python"
        assert script.skill == "test-skill"
        assert script.purpose is None
        assert script.parameters == {}
        assert script.dependencies == []
        assert script.execution_context is None
    
    def test_script_info_repr(self):
        """Test ScriptInfo string representation."""
        script = ScriptInfo(
            name="test.py",
            path=Path("/path/to/test.py"),
            script_type="python",
            skill="test-skill"
        )
        
        repr_str = repr(script)
        assert "test.py" in repr_str
        assert "python" in repr_str
        assert "test-skill" in repr_str


class TestScriptScanner:
    """Tests for ScriptScanner class."""
    
    @pytest.fixture
    def temp_agent_dir(self):
        """Create a temporary .agent directory structure for testing."""
        temp_dir = tempfile.mkdtemp()
        agent_path = Path(temp_dir) / ".agent"
        
        # Create skills directory structure
        skills_dir = agent_path / "skills"
        
        # Lab factory skill
        lab_factory = skills_dir / "lab-factory"
        lab_lib = lab_factory / "lib"
        lab_scripts = lab_factory / "scripts"
        lab_lib.mkdir(parents=True)
        lab_scripts.mkdir(parents=True)
        
        # Validation suite skill
        validation = skills_dir / "validation-suite"
        val_scripts = validation / "scripts"
        val_scripts.mkdir(parents=True)
        
        # Executors directory
        executors = agent_path / "executors"
        executors.mkdir(parents=True)
        
        # Create some test scripts
        (lab_lib / "Audition.jsx").write_text("// JSX library")
        (lab_lib / "time_utils.jsx").write_text("// Time utilities")
        (lab_scripts / "test_toolkit.jsx").write_text("// Test script")
        (val_scripts / "validate_links.py").write_text("# Validation script")
        (val_scripts / "validate_consistency.py").write_text("# Consistency check")
        (executors / "build_factory.py").write_text("# Build executor")
        
        yield agent_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_scan_skill_directory_with_lib_and_scripts(self, temp_agent_dir):
        """Test scanning a skill directory with both lib/ and scripts/ subdirectories."""
        lab_factory = temp_agent_dir / "skills" / "lab-factory"
        scripts = ScriptScanner.scan_skill_directory(lab_factory)
        
        assert len(scripts) == 3
        script_names = {s.name for s in scripts}
        assert "Audition.jsx" in script_names
        assert "time_utils.jsx" in script_names
        assert "test_toolkit.jsx" in script_names
        
        # Check script types
        for script in scripts:
            assert script.script_type == "jsx"
            assert script.skill == "lab-factory"
    
    def test_scan_skill_directory_scripts_only(self, temp_agent_dir):
        """Test scanning a skill directory with only scripts/ subdirectory."""
        validation = temp_agent_dir / "skills" / "validation-suite"
        scripts = ScriptScanner.scan_skill_directory(validation)
        
        assert len(scripts) == 2
        script_names = {s.name for s in scripts}
        assert "validate_links.py" in script_names
        assert "validate_consistency.py" in script_names
        
        # Check script types
        for script in scripts:
            assert script.script_type == "python"
            assert script.skill == "validation-suite"
    
    def test_scan_skill_directory_nonexistent(self):
        """Test scanning a non-existent skill directory."""
        fake_path = Path("/nonexistent/skill")
        scripts = ScriptScanner.scan_skill_directory(fake_path)
        
        assert scripts == []
    
    def test_scan_all_skills(self, temp_agent_dir):
        """Test scanning all skills in .agent directory."""
        all_scripts = ScriptScanner.scan_all_skills(temp_agent_dir)
        
        assert "lab-factory" in all_scripts
        assert "validation-suite" in all_scripts
        
        assert len(all_scripts["lab-factory"]) == 3
        assert len(all_scripts["validation-suite"]) == 2
    
    def test_scan_executors(self, temp_agent_dir):
        """Test scanning the executors directory."""
        scripts = ScriptScanner.scan_executors(temp_agent_dir)
        
        assert len(scripts) == 1
        assert scripts[0].name == "build_factory.py"
        assert scripts[0].script_type == "executor"
        assert scripts[0].skill == "executors"
    
    def test_scan_executors_nonexistent(self):
        """Test scanning non-existent executors directory."""
        fake_path = Path("/nonexistent")
        scripts = ScriptScanner.scan_executors(fake_path)
        
        assert scripts == []


class TestMetadataExtraction:
    """Tests for script metadata extraction."""
    
    def test_extract_python_docstring(self, tmp_path):
        """Test extracting purpose from Python docstring."""
        script_file = tmp_path / "test.py"
        script_file.write_text('''"""
This script validates links in markdown files.

It checks both internal and external links.
"""

import requests

def main():
    pass
''')
        
        script_info = ScriptInfo(
            name="test.py",
            path=script_file,
            script_type="python",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        assert result.purpose == "This script validates links in markdown files."
    
    def test_extract_python_argparse(self, tmp_path):
        """Test extracting parameters from argparse."""
        script_file = tmp_path / "test.py"
        script_file.write_text('''
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='File to process')
parser.add_argument('--verbose', help='Enable verbose output')
parser.add_argument('--output', help='Output directory')
''')
        
        script_info = ScriptInfo(
            name="test.py",
            path=script_file,
            script_type="python",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        assert '--file' in result.parameters
        assert result.parameters['--file'] == 'File to process'
        assert '--verbose' in result.parameters
        assert '--output' in result.parameters
    
    def test_extract_python_imports(self, tmp_path):
        """Test extracting dependencies from imports."""
        script_file = tmp_path / "test.py"
        script_file.write_text('''
import os
import sys
import requests
import yaml
from pathlib import Path
from markdown import markdown
''')
        
        script_info = ScriptInfo(
            name="test.py",
            path=script_file,
            script_type="python",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        # Should filter out standard library modules
        assert 'requests' in result.dependencies
        assert 'yaml' in result.dependencies
        assert 'markdown' in result.dependencies
        # Should not include standard library
        assert 'os' not in result.dependencies
        assert 'sys' not in result.dependencies
        assert 'pathlib' not in result.dependencies
    
    def test_extract_jsx_block_comment(self, tmp_path):
        """Test extracting purpose from JSX block comment."""
        script_file = tmp_path / "test.jsx"
        script_file.write_text('''/**
 * Audition API wrapper library
 * @description Provides high-level API for Adobe Audition automation
 */

function main() {
    // code
}
''')
        
        script_info = ScriptInfo(
            name="test.jsx",
            path=script_file,
            script_type="jsx",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        assert result.purpose == "Provides high-level API for Adobe Audition automation"
    
    def test_extract_jsx_includes(self, tmp_path):
        """Test extracting dependencies from JSX includes."""
        script_file = tmp_path / "test.jsx"
        script_file.write_text('''
#include "env_context.jsx"
#include "time_utils.jsx"

function main() {
    // code
}
''')
        
        script_info = ScriptInfo(
            name="test.jsx",
            path=script_file,
            script_type="jsx",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        assert "env_context.jsx" in result.dependencies
        assert "time_utils.jsx" in result.dependencies
    
    def test_extract_metadata_file_not_found(self):
        """Test metadata extraction with non-existent file."""
        script_info = ScriptInfo(
            name="test.py",
            path=Path("/nonexistent/test.py"),
            script_type="python",
            skill="test"
        )
        
        result = ScriptScanner.extract_script_metadata(script_info)
        
        # Should return original script_info without errors
        assert result.purpose is None
        assert result.parameters == {}


class TestUsageGeneration:
    """Tests for usage example generation."""
    
    def test_generate_usage_python_no_params(self):
        """Test generating usage for Python script without parameters."""
        script_info = ScriptInfo(
            name="test.py",
            path=Path(".agent/scripts/test.py"),
            script_type="python",
            skill="test"
        )
        
        usage = ScriptScanner.generate_usage_example(script_info)
        
        assert "python3" in usage
        assert ".agent/scripts/test.py" in usage
    
    def test_generate_usage_python_with_params(self):
        """Test generating usage for Python script with parameters."""
        script_info = ScriptInfo(
            name="test.py",
            path=Path(".agent/scripts/test.py"),
            script_type="python",
            skill="test"
        )
        script_info.parameters = {
            '--file': 'File to process',
            '--verbose': 'Enable verbose output',
            '--output': 'Output directory'
        }
        
        usage = ScriptScanner.generate_usage_example(script_info)
        
        assert "python3" in usage
        assert ".agent/scripts/test.py" in usage
        # Should include first 2 parameters as examples
        assert "--file" in usage or "--verbose" in usage
    
    def test_generate_usage_jsx(self):
        """Test generating usage for JSX script."""
        script_info = ScriptInfo(
            name="Audition.jsx",
            path=Path(".agent/lib/Audition.jsx"),
            script_type="jsx",
            skill="lab-factory"
        )
        
        usage = ScriptScanner.generate_usage_example(script_info)
        
        assert "Adobe Audition" in usage or "manifest" in usage
        assert ".agent/lib/Audition.jsx" in usage
    
    def test_generate_usage_executor(self):
        """Test generating usage for executor script."""
        script_info = ScriptInfo(
            name="build_factory.py",
            path=Path(".agent/executors/build_factory.py"),
            script_type="executor",
            skill="executors"
        )
        script_info.parameters = {
            '--task': 'Task to execute',
            '--section': 'Section to process'
        }
        
        usage = ScriptScanner.generate_usage_example(script_info)
        
        assert "python3" in usage
        assert "build_factory.py" in usage
        assert "--task" in usage or "--section" in usage


class TestDocumentationGeneration:
    """Tests for complete documentation generation."""
    
    def test_generate_script_documentation_minimal(self):
        """Test generating documentation with minimal information."""
        script_info = ScriptInfo(
            name="test.py",
            path=Path(".agent/scripts/test.py"),
            script_type="python",
            skill="test"
        )
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        assert "### test.py" in doc
        assert "**Purpose**:" in doc
        assert "**Location**:" in doc
        assert "**Usage**:" in doc
        assert ".agent/scripts/test.py" in doc
    
    def test_generate_script_documentation_full(self):
        """Test generating documentation with all fields."""
        script_info = ScriptInfo(
            name="validate_links.py",
            path=Path(".agent/scripts/validate_links.py"),
            script_type="python",
            skill="validation"
        )
        script_info.purpose = "Validates all links in markdown files"
        script_info.parameters = {
            '--file': 'Specific file to validate',
            '--verbose': 'Enable verbose output'
        }
        script_info.dependencies = ['requests', 'markdown']
        script_info.execution_context = "Run from project root"
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        assert "### validate_links.py" in doc
        assert "Validates all links in markdown files" in doc
        assert "**Parameters**:" in doc
        assert "--file" in doc
        assert "--verbose" in doc
        assert "**Dependencies**:" in doc
        assert "requests" in doc
        assert "markdown" in doc
        assert "**Execution Context**:" in doc
        assert "Run from project root" in doc
    
    def test_generate_all_documentation_empty(self):
        """Test generating documentation for empty script list."""
        doc = ScriptScanner.generate_all_documentation([])
        
        assert doc == ""
    
    def test_generate_all_documentation_multiple(self):
        """Test generating documentation for multiple scripts."""
        scripts = [
            ScriptInfo(
                name="test1.py",
                path=Path(".agent/scripts/test1.py"),
                script_type="python",
                skill="test"
            ),
            ScriptInfo(
                name="test2.py",
                path=Path(".agent/scripts/test2.py"),
                script_type="python",
                skill="test"
            )
        ]
        
        doc = ScriptScanner.generate_all_documentation(scripts, extract_metadata=False)
        
        assert "### test1.py" in doc
        assert "### test2.py" in doc
        assert doc.count("**Purpose**:") == 2
        assert doc.count("**Location**:") == 2


class TestRequirementsCoverage:
    """Tests verifying requirements coverage."""
    
    def test_requirement_3_3_script_locations(self):
        """
        Requirement 3.3: Document script locations with paths.
        
        Validates: Requirements 3.3
        """
        script_info = ScriptInfo(
            name="test.py",
            path=Path(".agent/skills/validation-suite/scripts/test.py"),
            script_type="python",
            skill="validation-suite"
        )
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must include location with path
        assert "**Location**:" in doc
        assert ".agent/skills/validation-suite/scripts/test.py" in doc
    
    def test_requirement_3_4_usage_instructions(self):
        """
        Requirement 3.4: Include usage instructions with command-line examples.
        
        Validates: Requirements 3.4
        """
        script_info = ScriptInfo(
            name="validate_links.py",
            path=Path(".agent/scripts/validate_links.py"),
            script_type="python",
            skill="validation"
        )
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must include usage section with command-line example
        assert "**Usage**:" in doc
        assert "```bash" in doc
        assert "python3" in doc
        assert "```" in doc
    
    def test_requirement_3_5_script_dependencies(self):
        """
        Requirement 3.5: Document script dependencies.
        
        Validates: Requirements 3.5
        """
        script_info = ScriptInfo(
            name="test.py",
            path=Path(".agent/scripts/test.py"),
            script_type="python",
            skill="test"
        )
        script_info.dependencies = ['requests', 'yaml', 'markdown']
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must include dependencies section
        assert "**Dependencies**:" in doc
        assert "requests" in doc
        assert "yaml" in doc
        assert "markdown" in doc
    
    def test_requirement_10_2_executor_usage_examples(self):
        """
        Requirement 10.2: Include full command-line usage examples for executors.
        
        Validates: Requirements 10.2
        """
        script_info = ScriptInfo(
            name="build_factory.py",
            path=Path(".agent/executors/build_factory.py"),
            script_type="executor",
            skill="executors"
        )
        script_info.parameters = {
            '--task': 'Task to execute (writer/auditor)',
            '--section': 'Section to process'
        }
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must include complete usage example
        assert "**Usage**:" in doc
        assert "python3" in doc
        assert "build_factory.py" in doc
        assert "```bash" in doc
    
    def test_requirement_10_3_executor_parameters(self):
        """
        Requirement 10.3: Document executor parameters and options.
        
        Validates: Requirements 10.3
        """
        script_info = ScriptInfo(
            name="build_factory.py",
            path=Path(".agent/executors/build_factory.py"),
            script_type="executor",
            skill="executors"
        )
        script_info.parameters = {
            '--task': 'Task to execute',
            '--section': 'Section to process',
            '--output': 'Output directory'
        }
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must document all parameters
        assert "**Parameters**:" in doc
        assert "--task" in doc
        assert "--section" in doc
        assert "--output" in doc
    
    def test_requirement_10_5_executor_dependencies(self):
        """
        Requirement 10.5: Document executor dependencies and prerequisites.
        
        Validates: Requirements 10.5
        """
        script_info = ScriptInfo(
            name="build_factory.py",
            path=Path(".agent/executors/build_factory.py"),
            script_type="executor",
            skill="executors"
        )
        script_info.dependencies = ['yaml', 'jinja2']
        script_info.execution_context = "Requires Python 3.8+ and project structure"
        
        doc = ScriptScanner.generate_script_documentation(script_info)
        
        # Must document dependencies and execution context
        assert "**Dependencies**:" in doc
        assert "yaml" in doc
        assert "jinja2" in doc
        assert "**Execution Context**:" in doc
        assert "Python 3.8+" in doc


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
