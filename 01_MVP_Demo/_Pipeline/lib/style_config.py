"""
Auto-generated Style Config for Matplotlib
DO NOT EDIT. Update .agent/standards/visual_system.yaml instead.
"""

COLORS = {
    'bg_base': '#0a0a0f',
    'bg_surface': '#1a1a25',
    'bg_highlight': '#20202e',
    'primary': '#6366f1',
    'primary_glow': 'rgba(99, 102, 241, 0.4)',
    'accent': '#8b5cf6',
    'success': '#34d399',
    'warning': '#fbbf24',
    'error': '#f87171',
    'text_main': '#ffffff',
    'text_secondary': '#a0a0b0',
    'text_muted': '#606070',
    'border': '#2a2a3a',
}

RC_PARAMS = {
    'axes.facecolor': '#0a0a0f',
    'figure.facecolor': '#0a0a0f',
    'text.color': '#ffffff',
    'axes.labelcolor': '#a0a0b0',
    'xtick.color': '#606070',
    'ytick.color': '#606070',
    'grid.color': '#2a2a3a',
    'grid.alpha': 0.2,
    'lines.linewidth': 2.0,
    'axes.prop_cycle': "cycler('color', ['#6366f1', '#34d399', '#fbbf24', '#f87171', '#8b5cf6'])",
}


import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

def apply_style():
    """Apply the project style to the current plot"""
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

