import matplotlib.pyplot as plt
import numpy as np

# Set dark theme and Bauhaus-inspired aesthetics
plt.style.use('dark_background')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='#0a0a0f')

# Colors from visual_system.yaml
cyan = "#34d399" # Emerald/Success
white = "#ffffff"
bg_color = "#0a0a0f"
head_color = "#1a1a25" # Surface color

# Circle (Head) settings
circle_radius = 0.35

for ax in [ax1, ax2]:
    ax.set_aspect('equal')
    ax.set_xlim(-1, 1.2)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    # Draw head (Circle)
    circle = plt.Circle((0, 0), circle_radius, color=head_color, ec=white, lw=2, zorder=5)
    ax.add_patch(circle)

# AX1: Low Freq (Diffraction) - "Water" metaphor
y_lines = np.linspace(-0.8, 0.8, 7)
x = np.linspace(-1, 1.2, 500)

for y_o in y_lines:
    # Create bending waves
    y_vals = []
    for xi in x:
        if xi < -circle_radius:
            y_vals.append(y_o)
        elif xi > circle_radius:
            y_vals.append(y_o)
        else:
            # Curve around circle
            # Using a simple displacement field
            dist = np.sqrt(xi**2 + y_o**2)
            if dist < circle_radius + 0.05:
                # Push outwards
                factor = (circle_radius + 0.1 - dist) * 1.5
                y_vals.append(y_o + factor * np.sign(y_o))
            else:
                y_vals.append(y_o)
    
    # Add sine wave pattern
    wave = 0.03 * np.sin(x * 12)
    ax1.plot(x, np.array(y_vals) + wave, color=cyan, lw=2, alpha=0.9, zorder=2)

ax1.text(0, -0.9, "Low Freq: Diffraction (Water)", color=cyan, ha='center', fontsize=12, fontweight='bold')

# AX2: High Freq (Shadow) - "Light" metaphor
for y_o in y_lines:
    if abs(y_o) > circle_radius:
        # Passes through
        ax2.plot([-1, 1.2], [y_o, y_o], color=white, lw=1.5, alpha=0.5, ls='--')
    else:
        # Blocked
        ax2.plot([-1, -circle_radius+0.05], [y_o, y_o], color=white, lw=2.5, alpha=1.0)
        # Shadow marker
        ax2.fill_between([circle_radius, 1.2], y_o-0.01, y_o+0.01, color='red', alpha=0.2)

ax2.text(0, -0.9, "High Freq: Head Shadow (Light)", color=white, ha='center', fontsize=12, fontweight='bold')

# Main title
plt.suptitle("Duplex Theory: Localization Mechanisms", color=white, fontsize=16, y=0.95)

plt.tight_layout()
output_path = "/Users/yamlam/Downloads/数字音频编辑Audition实用教程-混响2/02_Visuals/assets/S05_Phase4_Position/S05_Duplex_Theory_Visual_ai.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=bg_color)
print(f"✅ Image generated at: {output_path}")
