# Script Reference Template

This template defines the standard format for documenting external scripts in Power documentation.

## Template Structure

Each script should be documented with the following sections:

### Script Name

**Purpose**: Brief description of what the script does

**Location**: `path/to/script.ext`

**Usage**:
```bash
command path/to/script.ext [parameters]
```

**Parameters**:
- `--param1`: Description of parameter 1
- `--param2`: Description of parameter 2

**Dependencies**:
- Dependency 1
- Dependency 2

**Execution Context**: Required working directory or environment setup

**Example**:
```bash
# Concrete usage example
command path/to/script.ext --param1 value1 --param2 value2
```

## Template Fields

### Required Fields

1. **Script Name**: The name of the script (used as section header)
2. **Purpose**: A brief, clear description of what the script does
3. **Location**: Absolute or relative path to the script file
4. **Usage**: Command-line usage pattern with syntax

### Optional Fields

5. **Parameters**: Dictionary of parameter names to descriptions (optional)
6. **Dependencies**: List of required libraries, tools, or prerequisites (optional)
7. **Execution Context**: Required working directory or environment (optional)

## Usage in ContentMerger

The `ContentMerger.create_script_documentation()` method implements this template:

```python
from pathlib import Path
from migration_scripts.core.content_merger import ContentMerger

# Example: Document a Python validation script
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
```

## Examples

### Python Script Example

```markdown
### validate_links.py

**Purpose**: Validates all internal and external links in markdown files

**Location**: `.agent/skills/validation-suite/scripts/validate_links.py`

**Usage**:
```bash
python3 .agent/skills/validation-suite/scripts/validate_links.py
```

**Parameters**:
- `--file`: Specific file to validate (optional)
- `--verbose`: Enable verbose output

**Dependencies**:
- Python 3.8+
- requests library
- markdown parser

**Execution Context**: Run from project root directory
```

### JSX Script Example

```markdown
### Audition.jsx

**Purpose**: Core library providing Adobe Audition automation API

**Location**: `.agent/skills/lab-factory/lib/Audition.jsx`

**Usage**:
```bash
# Include in manifest.json for ExtendScript execution
{
  "includes": [".agent/skills/lab-factory/lib/Audition.jsx"]
}
```

**Parameters**:
- N/A (Library file, not directly executed)

**Dependencies**:
- Adobe Audition CC 2019 or later
- ExtendScript engine

**Execution Context**: Loaded via Adobe Audition's ExtendScript manifest system
```

### Executor Script Example

```markdown
### build_factory.py

**Purpose**: Automates transcript compilation and quality auditing

**Location**: `.agent/executors/build_factory.py`

**Usage**:
```bash
python3 .agent/executors/build_factory.py --task writer --section S02
```

**Parameters**:
- `--task`: Task mode (writer, auditor)
- `--section`: Section identifier (e.g., S02)
- `--file`: File path for auditor mode

**Dependencies**:
- Python 3.8+
- OpenAI API key (set in environment)
- Project structure files (Structure_Map, Design_Spec)

**Execution Context**: Run from project root directory with proper environment variables set
```

## Validation Checklist

When documenting a script, ensure:

- [ ] Script name is clear and matches the actual filename
- [ ] Purpose is concise (one sentence) and describes the main function
- [ ] Location path is accurate and uses consistent format (relative from project root)
- [ ] Usage example shows the complete command with proper syntax
- [ ] All parameters are documented with clear descriptions
- [ ] All dependencies are listed (runtime, libraries, tools)
- [ ] Execution context specifies required working directory or environment
- [ ] Example usage is concrete and can be copy-pasted

## Requirements Mapping

This template satisfies the following requirements:

- **Requirement 3.3**: Document script locations with absolute or relative paths
- **Requirement 3.4**: Include usage instructions with full command-line examples
- **Requirement 3.5**: Document script dependencies and prerequisites
- **Requirement 3.6**: Document required execution context
