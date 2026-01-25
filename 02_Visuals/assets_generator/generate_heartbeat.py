import numpy as np
from scipy.io import wavfile
import scipy.signal
import os

# CONFIGURATION
# ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "02_Visuals")
SAMPLE_RATE = 44100
BPM = 100 # Anxious Alice

def generate_heart_transient(duration, freq_start, freq_end, noise_mix=0.0):
    t_h = np.linspace(0, duration, int(duration*SAMPLE_RATE), False)
    
    # 1. Tonal (Muscle) - Sine Sweep
    # Logarithmic chirp for natural decay
    freqs = np.logspace(np.log10(freq_start), np.log10(freq_end), len(t_h))
    phases = np.cumsum(freqs) * 2 * np.pi / SAMPLE_RATE
    tone = np.sin(phases)
    
    # Envelope: Fast attack, exponential decay
    env = np.exp(-t_h * 15)
    tone *= env
    
    # 2. Texture (Fluid) - Filtered Noise
    noise = np.random.normal(0, 1, len(t_h))
    sos_bp = scipy.signal.butter(2, [100, 400], 'bp', fs=SAMPLE_RATE, output='sos')
    texture = scipy.signal.sosfilt(sos_bp, noise) * env
    
    return (tone * (1-noise_mix) + texture * noise_mix)

def save_wav(path, data, rate):
    max_val = np.max(np.abs(data))
    if max_val > 0: data = data / max_val
    output_data = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output_data)
    print(f"[Generate] Saved: {path}")

def main():
    print("--- Alice Asset Factory: Heartbeat ---")
    
    # Parameters for realistic heart (S1/S2)
    # S1 (Lub): Deeper 70->40z
    lub = generate_heart_transient(0.15, 70, 40, noise_mix=0.4)
    # S2 (Dub): Sharper 90->50Hz
    dub = generate_heart_transient(0.12, 90, 50, noise_mix=0.3)
    
    # Sequence
    beat_dur = 60.0 / BPM
    bar_dur = beat_dur * 4 # 4/4 bar
    full_bar = np.zeros(int(bar_dur * SAMPLE_RATE), dtype=np.float32)
    
    def add_sound(canvas, sound, pos_sec, gain=1.0):
        idx = int(pos_sec * SAMPLE_RATE)
        l = min(len(sound), len(canvas) - idx)
        if l > 0: canvas[idx:idx+l] += sound[:l] * gain

    # Beat 1 (Only one pulse per bar for dramatic effect? Or regular?)
    # Let's do regular pulse for now.
    for i in range(4):
        offset = i * beat_dur
        add_sound(full_bar, lub, offset + 0.0, 1.0)
        add_sound(full_bar, dub, offset + 0.28, 0.9)
    
    # Bone Conduction Filter (The "Internal" Effect)
    # LPF 250Hz - Simulating hearing from inside chest
    sos_bone = scipy.signal.butter(2, 250, 'lp', fs=SAMPLE_RATE, output='sos')
    internal_heart = scipy.signal.sosfilt(sos_bone, full_bar)
    
    # Loop it 4 times
    final_track = np.tile(internal_heart, 4)
    
    save_wav(os.path.join(OUTPUT_DIR, "Alice_Heartbeat_Internal.wav"), final_track, SAMPLE_RATE)
    print("Heartbeat generation complete.")

if __name__ == "__main__":
    main()
