---
description: Safely update a module's script, SRT, and timeline validation.
---

# Module Update Pipeline

**Trigger**: `/update_module [Module_ID]` (e.g. `/update_module S05`)

This workflow enforces the "Pre-Flight Check" protocol to prevent high-cost rework.

## Step 1: Pre-Flight Validation (🛡️ Safety First)
**Goal**: Ensure script integrity (Keys & Narratives) before expensive processing.
**Action 1.1**: Anchor Check (Visual Keys)
```bash
python .agent/skills/validation-suite/scripts/validate_anchors.py 03_Scripts/[Module_ID]_*.md
```

**Action 1.2**: INI Narrative Check (Invisible Instructions)
```bash
python .agent/skills/validation-suite/scripts/validate_narrative_integrity.py 03_Scripts/[Module_ID]_*.md
```
> **CRITICAL**: If EITHER step fails (returns exit code 1), **STOP IMMEDIATELY**. Do not proceed to SRT generation. Report the error to the user.

## Step 2: SRT Regeneration (🗣️ Alignment)
**Goal**: Generate high-precision SRT from script and audio.
**Action**: Locate the `.aac`/`.mp3` audio and `.txt` transcript in `03_Scripts/tts/`.
**Command**:
```bash
# Example for S05
python .agent/skills/aeneas-ng/scripts/align.py \
    --audio "03_Scripts/tts/[Module_ID]_*.aac" \
    --text "03_Scripts/tts/[Module_ID]_*.txt" \
    --output "03_Scripts/tts/[Module_ID]_*.srt"
```

## Step 3: Timeline Synchronization (⏱️ Sync)
**Goal**: Inject new timestamps into `timeline.json`.
**Command**:
```bash
python 04_Delivery/h5_preview/scripts/build_timeline.py [Module_ID]
```

## Step 4: Preview Deployment (🚀 Deploy)
**Goal**: Refresh H5 data.
**Command**:
```bash
./sync_preview.command
```
