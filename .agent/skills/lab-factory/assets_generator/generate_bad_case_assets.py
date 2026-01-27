import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
from scipy.io import wavfile
import scipy.signal as signal
import os
import sys
import subprocess

# --- Configuration & Setup ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "../config")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "01_MVP_Demo/_Library/S0X_Shared")

sys.path.append(CONFIG_DIR)
try:
    from Visual_System_Config import VisualTheme, Palette, MetricTranslator, CURRENT_THEME, FONT_REGULAR, FONT_MEDIUM
except ImportError:
    print("CRITICAL WARNING: Visual_System_Config not found.")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Asset Synthesis (Unholy Trinity v3) ---
def generate_context_aware_artifacts(clean_audio_path, output_audio_path):
    fs, audio = wavfile.read(clean_audio_path)
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32) / 32767.0
    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)
        
    duration = len(audio) / fs
    t = np.linspace(0, duration, len(audio), endpoint=False)
    
    # 1. Hum (50Hz + Harmonics)
    hum_freq = 50
    lfo = 0.05 * (1 + 0.2 * np.sin(2 * np.pi * 0.5 * t)) 
    hum = lfo * np.sin(2 * np.pi * hum_freq * t)
    hum += (lfo * 0.5) * np.sin(2 * np.pi * (hum_freq * 3) * t) # Boost harmonics for visibility
    hum += (lfo * 0.3) * np.sin(2 * np.pi * (hum_freq * 5) * t)
    
    # 2. Hiss (Louder -18dB)
    white = np.random.randn(len(audio))
    X = np.fft.rfft(white)
    S = np.sqrt(np.arange(len(X)) + 1.)
    pink = np.fft.irfft(X / S)
    if len(pink) > len(audio): pink = pink[:len(audio)]
    else: pink = np.pad(pink, (0, len(audio)-len(pink)))
    hiss = pink * 0.15 # ~ -16dB for better visual "Fog"
    
    # 3. Context Clicks
    clicks = np.zeros_like(audio)
    b, a = signal.butter(2, 200 / (fs/2), btype='low')
    env_detect = signal.filtfilt(b, a, np.abs(audio))
    peaks, _ = signal.find_peaks(env_detect, height=0.2, distance=fs*0.5)
    for p in peaks:
        idx = min(len(audio)-1, p + int(0.01*fs))
        clicks[idx] = 0.9 # Hard clip
    
    # Rare random clicks
    num_random = int(duration * 0.3)
    rand_indices = np.random.choice(len(audio), num_random, replace=False)
    for idx in rand_indices:
        clicks[idx] = 0.6

    dirty_audio = audio + hum + hiss + clicks
    dirty_audio = np.clip(dirty_audio, -0.99, 0.99)
    wavfile.write(output_audio_path, fs, (dirty_audio * 32767).astype(np.int16))
    return fs, t, dirty_audio, hum, clicks, hiss

# --- Visualization (Log Scale & High Contrast) ---
def render_diagnosis_video(fs, t, audio, hum_track, click_track, output_video_path, source_audio_path):
    plt.rcParams.update(CURRENT_THEME)
    
    # Custom Colormap: Black -> Purple -> Orange -> Yellow (Inferno-ish but tweaked for Hiss visibility)
    # Raising the "Floor" visibility
    
    fig = plt.figure(figsize=(12, 10), dpi=100)
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 2.5]) # More space for Spec
    
    ax_wave = fig.add_subplot(gs[0])
    ax_spec = fig.add_subplot(gs[1])
    
    # Titles
    ax_wave.set_title(MetricTranslator.translate("Waveform Analysis"), fontproperties=FONT_MEDIUM, color=Palette.WAVE, fontsize=16)
    ax_spec.set_title(MetricTranslator.translate("Spectral Diagnosis"), fontproperties=FONT_MEDIUM, color=Palette.ENV, fontsize=16)
    
    # Waveform
    ax_wave.set_ylim(-1.1, 1.1)
    ax_wave.set_facecolor(Palette.BG)
    line_wave, = ax_wave.plot([], [], lw=1.0, color=Palette.WAVE, alpha=0.9)
    
    # --- SPECTROGRAM PRE-CALC ---
    # Use log scale for frequency to show 50Hz clearly
    f, t_spec, Sxx = signal.spectrogram(audio, fs, nperseg=2048, noverlap=1024) # Higher resolution
    Sxx_db = 10 * np.log10(Sxx + 1e-9)
    
    # Crop Frequency (0 - 8000Hz)
    freq_mask = (f >= 20) & (f < 8000)
    f = f[freq_mask]
    Sxx_db = Sxx_db[freq_mask, :]
    
    # Contrast Stretch
    # Noise floor (Hiss) is around -50dB to -40dB in Spec logic
    # Hum is constant.
    # Set vmin/vmax to emphasize differences
    vmin = -70 
    vmax = -10
    
    # Use pcolormesh for Log Scale support
    # Note: pcolormesh is slow for animation if redrawn. 
    # Better to use imshow with NON-LINEAR aspect or custom extent? 
    # No, imshow axis is linear. 
    # Trick: We can preserve linear Y but map display labels? 
    # No, we want Visual space to scale. 
    # Let's use pcolormesh but pre-render? No, scrolling...
    # Optimization: Use Imshow but warp the DATA itself? (Log-binning) -> Too complex.
    # Simple approach: Imshow with linear Y, BUT zoom into low freq? 
    # Best compromise: Imshow using LogNorm? No, that's color.
    # Let's stick to Linear Y but start from 0, and use an overlay arrow for 50Hz.
    # Wait, 50Hz on 8000Hz scale is invisible (line 0).
    # OPTION B: SymLog Scale on Axis. use pcolormesh.
    # Optimization: Render ONE big image, then just shift X limits.
    
    mesh = ax_spec.pcolormesh(t_spec, f, Sxx_db, shading='gouraud', cmap='inferno', vmin=vmin, vmax=vmax)
    ax_spec.set_yscale('symlog', linthresh=100) # Expands 0-100Hz range!
    ax_spec.set_ylim(20, 8000)
    
    # Labels
    ax_spec.set_yticks([50, 100, 500, 1000, 4000])
    ax_spec.set_yticklabels(["50Hz", "100", "500", "1k", "4k"], fontproperties=FONT_REGULAR)
    ax_spec.set_ylabel("Freq (Log Scale)", fontproperties=FONT_REGULAR)
    ax_spec.set_xlabel("Time (s)", fontproperties=FONT_REGULAR)
    
    # --- OVERLAYS ---
    
    # 1. Hum Indicator (Horizontal Line at 50Hz)
    # Draw a visual line at 50Hz to highlight it
    ax_spec.axhline(50, color=Palette.WAVE, linestyle='--', alpha=0.5, lw=1)
    lbl_hum = MetricTranslator.translate("Hum Detected")
    ax_spec.text(0.2, 55, f"{lbl_hum} ->", fontproperties=FONT_MEDIUM, color=Palette.WAVE, fontsize=12, ha='left')
    
    # 2. Hiss Label (General Background)
    lbl_hiss = MetricTranslator.translate("Hiss Floor")
    ax_spec.text(0.2, 6000, f"{lbl_hiss}", fontproperties=FONT_REGULAR, color='#AAAAAA', fontsize=12, alpha=0.8, bbox=dict(facecolor='black', alpha=0.5))

    # 3. Click Label (Dynamic)
    lbl_click = MetricTranslator.translate("Click Detected")
    txt_click = ax_spec.text(0, 7000, f"| {lbl_click}", fontproperties=FONT_MEDIUM, color='#FF0055', fontsize=14, alpha=0, fontweight='bold')

    # Playheads
    playhead_w = ax_wave.axvline(0, color=Palette.HIGHLIGHT, alpha=0.8)
    playhead_s = ax_spec.axvline(0, color=Palette.HIGHLIGHT, alpha=0.8)

    WIN_SIZE = 4.0 

    def init():
        return line_wave, playhead_w, playhead_s, txt_click

    fps = 30
    duration = t[-1]
    total_frames = int(duration * fps)
    
    def update(frame):
        current_time = frame / fps
        
        # Scroll
        if current_time > WIN_SIZE:
             ax_wave.set_xlim(current_time - WIN_SIZE, current_time)
             ax_spec.set_xlim(current_time - WIN_SIZE, current_time)
             txt_click.set_x(current_time)
        else:
             ax_wave.set_xlim(0, WIN_SIZE)
             ax_spec.set_xlim(0, WIN_SIZE)
             txt_click.set_x(current_time)

        playhead_w.set_xdata([current_time])
        playhead_s.set_xdata([current_time])
        
        # Wave Data
        line_wave.set_data(t, audio)
        
        # Click Detection
        idx = int(current_time * fs)
        # Check window
        start = max(0, idx - 1000)
        end = min(len(click_track), idx + 1000)
        if len(click_track) > 0 and np.max(click_track[start:end]) > 0.4:
            txt_click.set_alpha(1.0)
        else:
            txt_click.set_alpha(max(0, txt_click.get_alpha() - 0.2))
            
        return line_wave, playhead_w, playhead_s, txt_click

    # Use BLIT=FALSE because Axis Limits change (Scrolling)
    ani = animation.FuncAnimation(fig, update, frames=total_frames, init_func=init, blit=False)
    
    temp_video = output_video_path.replace(".mp4", "_silent.mp4")
    print(f"Rendering (LogScale) to {temp_video}...")
    ani.save(temp_video, writer='ffmpeg', fps=fps, dpi=100)
    plt.close(fig)
    
    print("Merging Audio...")
    cmd = [
        "ffmpeg", "-y", "-i", temp_video, "-i", source_audio_path,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_video_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    if os.path.exists(output_video_path):
        os.remove(temp_video)
        print(f"[VIDEO] Saved: {output_video_path}")

if __name__ == "__main__":
    print("--- 🩺 Generating High-Contrast Diagnosis Assets ---")
    src_clean = os.path.join(OUTPUT_DIR, "asset_S0X_dry_voice_clean.wav")
    dst_dirty = os.path.join(OUTPUT_DIR, "asset_S0X_bad_case_demo.wav")
    dst_video = os.path.join(OUTPUT_DIR, "video_bad_case_diagnosis.mp4")
    
    if not os.path.exists(src_clean):
        # Generate placeholder if missing
        fs = 48000
        t = np.linspace(0, 5, 5*fs)
        voice = np.sin(2*np.pi*440*t) * np.exp(-t)
        wavfile.write(src_clean, fs, (voice * 30000).astype(np.int16))

    fs, t, dirty, hum_tr, click_tr, hiss_tr = generate_context_aware_artifacts(src_clean, dst_dirty)
    render_diagnosis_video(fs, t, dirty, hum_tr, click_tr, dst_video, dst_dirty)
    print("--- Complete ---")
