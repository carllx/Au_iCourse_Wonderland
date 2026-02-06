#!/usr/bin/env python3
"""
Style Sync Engine (Visual Director)
读取 .agent/standards/visual_system.yaml
生成 1. theme.css (H5)
生成 2. style_config.py (Matplotlib)
"""

import yaml
from pathlib import Path
import json

# paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
YAML_PATH = PROJECT_ROOT / ".agent/standards/visual_system.yaml"
CSS_OUTPUT = PROJECT_ROOT / "04_Delivery/h5_preview/src/styles/theme.css"
PY_OUTPUT = PROJECT_ROOT / "01_MVP_Demo/_Pipeline/lib/style_config.py"

def load_config():
    if not YAML_PATH.exists():
        print(f"❌ Config not found: {YAML_PATH}")
        exit(1)
    with open(YAML_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_css(data):
    palette = data.get('palette', {})
    css_content = ":root {\n"
    
    # Map YAML keys to CSS vars
    mapping = {
        'bg_base': '--color-bg-base',
        'bg_surface': '--color-bg-surface',
        'bg_highlight': '--color-bg-card',
        'primary': '--color-primary',
        'primary_glow': '--color-primary-glow',
        'accent': '--color-accent',
        'success': '--color-success',
        'warning': '--color-warning',
        'error': '--color-error',
        'text_main': '--color-text-main',
        'text_secondary': '--color-text-secondary',
        'text_muted': '--color-text-muted',
        'border': '--color-border',
    }
    
    for y_key, css_var in mapping.items():
        if y_key in palette:
            css_content += f"  {css_var}: {palette[y_key]};\n"
            
    # Legacy aliases
    css_content += "\n  /* Legacy Aliases (Auto-Generated) */\n"
    css_content += "  --bg-primary: var(--color-bg-base);\n"
    css_content += "  --bg-secondary: var(--color-bg-surface);\n"
    css_content += "  --text-primary: var(--color-text-main);\n"
    
    css_content += "}\n"
    
    CSS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CSS_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✅ Generated CSS: {CSS_OUTPUT.relative_to(PROJECT_ROOT)}")

def generate_python(data):
    palette = data.get('palette', {})
    mpl = data.get('matplotlib', {})
    
    py_content = "\"\"\"\nAuto-generated Style Config for Matplotlib\nDO NOT EDIT. Update .agent/standards/visual_system.yaml instead.\n\"\"\"\n\n"
    
    # Generate COLORS dictionary
    py_content += "COLORS = {\n"
    for k, v in palette.items():
        py_content += f"    '{k}': '{v}',\n"
    py_content += "}\n\n"
    
    # Generate RC_PARAMS
    py_content += "RC_PARAMS = {\n"
    py_content += f"    'axes.facecolor': '{palette.get('bg_base', '#000000')}',\n"
    py_content += f"    'figure.facecolor': '{palette.get('bg_base', '#000000')}',\n"
    py_content += f"    'text.color': '{palette.get('text_main', '#ffffff')}',\n"
    py_content += f"    'axes.labelcolor': '{palette.get('text_secondary', '#aaaaaa')}',\n"
    py_content += f"    'xtick.color': '{palette.get('text_muted', '#666666')}',\n"
    py_content += f"    'ytick.color': '{palette.get('text_muted', '#666666')}',\n"
    py_content += f"    'grid.color': '{palette.get('border', '#333333')}',\n"
    py_content += f"    'grid.alpha': {mpl.get('grid_alpha', 0.2)},\n"
    py_content += f"    'lines.linewidth': {mpl.get('linewidth', 2.0)},\n"
    
    # Prop Cycle
    colors = mpl.get('color_cycle', [])
    if colors:
        py_content += f"    'axes.prop_cycle': \"cycler('color', {colors})\",\n"
        
    py_content += "}\n\n"
    
    # Helper function
    py_content += """
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

def apply_style():
    \"\"\"Apply the project style to the current plot\"\"\"
    # Manual update for safe execution
    for k, v in RC_PARAMS.items():
        if k == 'axes.prop_cycle':
            # Safe eval for cycler
            try:
                # Extract list from string repr like "cycler('color', ['#a', '#b'])"
                # This is a bit hacky, better to reconstruct cycler
                pass 
            except:
                pass
        else:
            mpl.rcParams[k] = v
            
    # Re-apply cycler securely
    if 'axes.prop_cycle' in RC_PARAMS:
         # Hardcoded standard recovery since we generate the file
         c_list = RC_PARAMS['axes.prop_cycle'].replace("cycler('color', ", "").replace(")", "")
         # AST eval is safer but we trust our own generation
         import ast
         try:
            color_list = ast.literal_eval(c_list)
            mpl.rcParams['axes.prop_cycle'] = cycler(color=color_list)
         except:
            print("⚠️ Failed to apply color cycle")

"""

    PY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(PY_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(py_content)
    print(f"✅ Generated Python Config: {PY_OUTPUT.relative_to(PROJECT_ROOT)}")

def main():
    try:
        config = load_config()
        generate_css(config)
        generate_python(config)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
