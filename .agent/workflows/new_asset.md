---
description: Create a new audio asset module (Generator + Renderer)
---

# Create New Audio Asset

Follow this workflow to create a new asset under the `01_MVP_Demo` Modular Architecture.

## 1. Identify Context
- **Module ID**: Which S0x chapter does this belong to? (e.g., S03, S04)
- **Asset Name**: Short, descriptive snake_case name. (e.g., `alice_voice`, `reverb_impulse`)

## 2. Scaffold Scripts
Create the generator script in `01_MVP_Demo/_Pipeline/generators/`.

```bash
# Example Name: gen_S03_alice_voice.py
touch 01_MVP_Demo/_Pipeline/generators/gen_S[MODULE]_[NAME].py
```

**Template**:
```python
import numpy as np
from scipy.io import wavfile
import os
import sys

def main():
    # PATH SETUP
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(base_dir))
    output_dir = os.path.join(project_root, "_Library", "S[MODULE]_[NAME_GROUP]")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, "asset_S[MODULE]_[NAME].wav")

    # GENERATION LOGIC
    # ... (Your DSP Code Here) ...

    # SAVE
    # wavfile.write(output_path, 44100, data)
    print(f"Generated: {output_path}")

if __name__ == "__main__":
    main()
```

## 3. Execute & Verify
Run the script to generate the WAV file.

```bash
python 01_MVP_Demo/_Pipeline/generators/gen_S[MODULE]_[NAME].py
ls -l 01_MVP_Demo/_Library/S[MODULE]_[NAME_GROUP]/
```

## 4. Documentation
Update `01_MVP_Demo/Asset_Production_Guide.md` to include the new file in the Manifest table.
