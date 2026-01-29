"""
S05 声像可视化渲染器 (v3: Object-Based Radar)
-----------------------------------------------
可视化 S05 Demo Mix 中的动态声场。

Visualizes:
1. Heartbeat (Center) - Red pulsing dot
2. Shadow (Center) - White ghost
3. Needle (Spiral) - Yellow dot tracing an inward spiral
4. Wall (Approach) - Blue arc expanding from outer to inner ring

Output: visual_S05_spiral_radar.mp4
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection
from scipy.io import wavfile
import os
import sys

# --- Path Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../")) 
LIB_DIR = os.path.join(PROJECT_ROOT, "01_MVP_Demo/_Library/S05_Position")

# --- Visual Constants ---
COLORS = {
    'bg': '#121212',
    'grid': '#333333',
    'heart': '#FF3366',
    'shadow': '#AAAAAA',
    'needle': '#FFCC00',
    'wall': '#00A8E8',
    'text': '#DDDDDD'
}

# --- Data Loading ---
def load_audio(filename):
    path = os.path.join(LIB_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: {filename} not found.")
        return None, None
    fs, data = wavfile.read(path)
    data = data.astype(np.float32) / 32768.0
    return fs, data

# --- Trajectory Calculation (Mirroring DSP Logic) ---

def calculate_spiral_trajectory(duration, fps, rotations=4, start_r=0.9, end_r=0.15):
    """
    复现 apply_spiral_pan 的轨迹。
    Returns: (angles[], radii[]) for each frame
    """
    n_frames = int(duration * fps)
    t = np.linspace(0, 1, n_frames)
    angles = t * rotations * 2 * np.pi
    radii = start_r + t * (end_r - start_r)
    return angles, radii

def calculate_wall_expansion(duration, fps, start_r=0.95, end_r=0.3):
    """
    复现 apply_approaching_wall 的视觉效果。
    Wall is a wedge that grows inwards.
    Returns: (inner_radii[], outer_radii[]) for each frame
    """
    n_frames = int(duration * fps)
    t = np.linspace(0, 1, n_frames)
    # Outer edge stays fixed, inner edge moves inward
    outer_r = np.full(n_frames, start_r)
    inner_r = start_r - t * (start_r - end_r)
    return inner_r, outer_r

# --- Main Rendering ---

def render_spiral_radar():
    print("--- S05 Visual Renderer (v3: Object-Based Radar) ---")
    
    # Load audio for sync
    fs, mix_data = load_audio("demo_S05_spiral_mix.wav")
    if fs is None:
        print("Error: Demo mix not found. Run generator first.")
        return
    
    # Also load individual sources for amplitude tracking
    _, hb_data = load_audio("asset_S05_heartbeat_visceral.wav")
    _, shadow_data = load_audio("asset_S05_shadow_self.wav")
    _, needle_data = load_audio("asset_S05_threat_anxiety.wav")
    _, wall_data = load_audio("asset_S05_threat_pressure.wav")
    
    duration = len(mix_data) / fs
    fps = 30
    n_frames = int(duration * fps)
    samples_per_frame = fs // fps
    
    # Pre-calculate trajectories
    needle_angles, needle_radii = calculate_spiral_trajectory(duration, fps)
    wall_inner, wall_outer = calculate_wall_expansion(duration, fps)
    
    # Setup Figure
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(8, 8), dpi=100, facecolor=COLORS['bg'])
    ax = fig.add_subplot(111, projection='polar')
    ax.set_facecolor(COLORS['bg'])
    ax.set_ylim(0, 1.0)
    ax.set_yticklabels([])
    ax.grid(color=COLORS['grid'], linestyle='--', linewidth=0.5)
    ax.set_xticklabels([])  # Hide angle labels for cleaner look
    
    # --- Create Artists ---
    # 1. Center Objects (Heartbeat + Shadow)
    heart_dot, = ax.plot([], [], 'o', color=COLORS['heart'], markersize=20, label='Heartbeat')
    shadow_dot, = ax.plot([], [], 'o', color=COLORS['shadow'], markersize=15, alpha=0.5, label='Shadow')
    
    # 2. Needle (Spiral Dot + Trail)
    needle_dot, = ax.plot([], [], 'o', color=COLORS['needle'], markersize=10, label='Anxiety')
    needle_trail, = ax.plot([], [], '-', color=COLORS['needle'], alpha=0.3, linewidth=1)
    
    # 3. Wall (Wedge Patch) - Covering front 180 degrees
    # Initialize with zero width
    wall_patch = Wedge((0, 0), 0.95, -90, 90, width=0, facecolor=COLORS['wall'], alpha=0.4, transform=ax.transData + ax.transAxes)
    # Using ax.bar for polar wedge is simpler
    # Create a bar at 90 degrees (front), width covering 180 degrees
    wall_bar = ax.bar(np.radians(90), 0.01, width=np.radians(180), bottom=0.94, 
                       color=COLORS['wall'], alpha=0.5, label='Pressure')[0]
    
    # 4. Labels
    ax.text(np.radians(90), 0.1, "SELF", ha='center', va='center', color=COLORS['text'], fontsize=12, fontweight='bold')
    
    # Legend
    ax.legend(loc='upper right', framealpha=0.3)
    
    # Trail history
    trail_angles = []
    trail_radii = []
    
    # --- Update Function ---
    def update(frame):
        idx = frame * samples_per_frame
        chunk = 1000
        
        # Get amplitudes (RMS) for this frame
        def get_rms(data, idx, chunk):
            if data is None or len(data.shape) == 0: return 0
            if len(data.shape) > 1: data = data[:, 0]  # Mono
            if idx + chunk >= len(data): return 0
            return np.sqrt(np.mean(data[idx:idx+chunk]**2))
        
        hb_rms = get_rms(hb_data, idx, chunk) * 50  # Scale for visibility
        shadow_rms = get_rms(shadow_data, idx, chunk) * 30
        needle_rms = get_rms(needle_data, idx, chunk) * 20
        wall_rms = get_rms(wall_data, idx, chunk) * 10
        
        # Update Heartbeat (Center, size pulsates)
        heart_dot.set_data([np.radians(90)], [0.05])  # Fixed center-ish
        heart_dot.set_markersize(np.clip(15 + hb_rms * 10, 10, 40))
        
        # Update Shadow (Center)
        shadow_dot.set_data([np.radians(90)], [0.08])
        shadow_dot.set_alpha(np.clip(0.3 + shadow_rms * 0.5, 0.1, 1.0))
        
        # Update Needle (Spiral)
        if frame < len(needle_angles):
            angle = needle_angles[frame]
            radius = needle_radii[frame]
            needle_dot.set_data([angle], [radius])
            needle_dot.set_markersize(np.clip(8 + needle_rms * 5, 5, 25))
            
            # Update trail
            trail_angles.append(angle)
            trail_radii.append(radius)
            # Keep last 50 points for trail
            if len(trail_angles) > 50:
                trail_angles.pop(0)
                trail_radii.pop(0)
            needle_trail.set_data(trail_angles, trail_radii)
        
        # Update Wall (Expanding Wedge)
        if frame < len(wall_inner):
            # Height = outer - inner
            height = wall_outer[frame] - wall_inner[frame]
            wall_bar.set_height(height)
            wall_bar.set_y(wall_inner[frame])  # Bottom of bar
            # Alpha based on RMS (Clamped!)
            wall_bar.set_alpha(np.clip(0.3 + wall_rms * 0.3, 0.2, 0.9))
        
        return heart_dot, shadow_dot, needle_dot, needle_trail, wall_bar
    
    # --- Create Animation ---
    print(f"Rendering {n_frames} frames at {fps} FPS...")
    ani = animation.FuncAnimation(fig, update, frames=n_frames, blit=True, interval=1000//fps)
    
    # Save (Silent first, then merge audio)
    temp_mp4 = os.path.join(LIB_DIR, "visual_S05_spiral_radar_temp.mp4")
    final_mp4 = os.path.join(LIB_DIR, "visual_S05_spiral_radar.mp4")
    audio_wav = os.path.join(LIB_DIR, "demo_S05_spiral_mix.wav")
    
    print(f"  Saving video (silent)...")
    ani.save(temp_mp4, writer='ffmpeg', fps=fps)
    plt.close(fig)
    
    print(f"  Merging audio...")
    os.system(f"ffmpeg -y -i {temp_mp4} -i {audio_wav} -c:v copy -c:a aac -shortest {final_mp4} -hide_banner -loglevel error")
    
    if os.path.exists(temp_mp4):
        os.remove(temp_mp4)
    
    print(f"\n[Done] Output: {final_mp4}")

if __name__ == "__main__":
    render_spiral_radar()
