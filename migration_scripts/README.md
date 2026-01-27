# Agent to Power Migration Scripts

This directory contains Python scripts for migrating the `.agent` directory architecture to Kiro Power format.

## Structure

- `core/` - Core utility modules
  - `file_ops.py` - File system operations
  - `yaml_handler.py` - YAML processing utilities
  - `content_merger.py` - Content merging and integration
- `migrate.py` - Main migration script
- `requirements.txt` - Python dependencies

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the migration script:
```bash
python migrate.py
```

For more options:
```bash
python migrate.py --help
```
