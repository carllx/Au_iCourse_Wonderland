# MVP Demo Architecture Guide

**Version**: 1.1 (2026-01-29)
**Scope**: `01_MVP_Demo` assets and tools.

## 1. Core Philosophy (核心理念)

*   **Modular (模块化)**: All resources must strictly correspond to the Course Structure (`00_Structure_Map.md`).
*   **Correlated (强对应)**: Scripts and Assets share a naming bond. `gen_X.py` produces `asset_X.wav`.
*   **Sustainable (可持续)**: No "temp", "test", or "backup" files in the main tree.

## 2. Directory Structure (目录结构)

```text
01_MVP_Demo/
├── _Pipeline/               # The "Factory" - Code only.
│   ├── generators/          # Scripts that CREATE audio (Input: Params/Raw -> Output: SFX)
│   ├── renderers/           # Scripts that VISUALIZE audio (Input: Audio -> Output: Video)
│   └── utils/               # Shared python modules (optional)
│
├── _Library/                # The "Warehouse" - Data only.
│   ├── S0x_[ModuleName]/    # Specific assets for a specific module
│   │   ├── asset_S0x_[Name].wav
│   │   └── asset_S0x_[Name].mp4
│   │
│   └── S0X_Shared/          # Reusable assets across modules
│       └── asset_S0X_[Name].wav
```

## 3. Naming Conventions (命名规范)

AI Agents **MUST** validate file names against these Regex patterns before saving.

### A. Scripts (`_Pipeline`)
*   **Generators**: `^gen_S\d{2}_[a-z0-9_]+\.py$`
    *   Example: `gen_S02_heartbeat.py`
    *   Example: `gen_S04_reverb_ir.py`
*   **Renderers**: `^render_S\d{2}_[a-z0-9_]+\.py$`
    *   Example: `render_S02_spectrum.py`

### B. Assets (`_Library`)
*   **Assets**: `^asset_S\d{2}_[a-z0-9_]+\.(wav|mp3|mp4)$`
    *   Example: `asset_S02_heartbeat_subtle.wav`
*   **Object-Based Naming (New in v1.1)**:
    *   For dynamic assets (moving in 3D space), name by **Character/Texture** (e.g., `_pressure`, `_anxiety`), NOT by location (`_L`, `_R`).
    *   Location is a *state*, not an *identity*.
*   **References**: `^ref_[a-z0-9_]+\.(wav|mp3|txt)$`
    *   Example: `ref_voice_tts_demo.wav`

## 4. Agent Rules (Agent 行为准则)

1.  **One Script, One Task**: Do not create generic `utils.py` or `main.py` unless strictly necessary for shared code. Each asset generation task needs its own script.
2.  **Self-Contained**: Scripts should ideally be runnable via CLI. `python gen_S02_heartbeat.py` should just work.
3.  **Path Awareness**: Scripts must use relative paths assuming execution from the project root OR handle `__file__` driven absolute paths.
4.  **No Hallucinations**: Do not reference assets that do not exist in `_Library`.
