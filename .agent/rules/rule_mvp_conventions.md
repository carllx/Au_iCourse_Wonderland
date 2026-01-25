---
trigger: glob
description: Naming and structural conventions for MVP Demo.
globs: 03_MVP_Demo/**
---

# MVP Demo Architecture Guidelines

When working within `03_MVP_Demo`, you **MUST** follow the architecture and naming conventions defined in:
`03_MVP_Demo/ARCHITECTURE_GUIDE.md`

Key highlights:
- **Scripts**: `_Pipeline/generators/` (e.g. `gen_S02_heartbeat.py`)
- **Assets**: `_Library/S0x_ModuleName/` (e.g. `asset_S02_heartbeat.wav`)
- **No generic names**: Avoid `utils.py`, `assets/`, `tools/`.
