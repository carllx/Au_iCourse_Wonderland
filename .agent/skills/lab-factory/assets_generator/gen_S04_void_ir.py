import numpy as np
from scipy.io import wavfile
import scipy.signal
import os

# Configuration
def get_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != "/":
        if os.path.exists(os.path.join(current, ".agent")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = get_project_root()
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "_Library/S04_Space")
SAMPLE_RATE = 44100

def generate_pink_noise(samples):
    """Generates Pink Noise (1/f) density for the reverb tail."""
    white = np.random.normal(0, 1, samples).astype(np.float32)
    b, a = scipy.signal.butter(1, 0.4) 
    pink = scipy.signal.lfilter(b, a, white)
    return pink

def apply_lowpass(audio, cutoff_freq, rate):
    nyquist = rate / 2
    norm_cutoff = cutoff_freq / nyquist
    b, a = scipy.signal.butter(2, norm_cutoff, btype='low', analog=False)
    filtered = scipy.signal.lfilter(b, a, audio)
    return filtered

def generate_void_ir(duration, decay_time, sample_rate):
    samples = int(duration * sample_rate)

    # 1. Base Tail (Pink Noise) - Dense but dark
    tail = generate_pink_noise(samples)

    # Envelope: RT60 decay
    t = np.linspace(0, duration, samples, False)
    tau = decay_time / 6.9
    envelope = np.exp(-t / tau)
    tail = tail * envelope

    # 2. Spectral Shaping (The "Void" Character)
    # Void is an infinite dark space. High frequencies are absorbed instantly.
    # We apply a drastic Low Pass Filter.
    tail = apply_lowpass(tail, 800, sample_rate) # 800Hz Cutoff (Very Dark)

    # 3. No Early Reflections (ER)
    # A void has no walls, so no discrete echoes. Just the tail fading into nothing.
    
    # Fade in to soften the attack (no wall impact)
    fade_in = int(0.05 * sample_rate) # 50ms fade in
    if fade_in < samples:
        lin_fade = np.linspace(0, 1, fade_in)
        tail[:fade_in] *= lin_fade

    # Normalize
    if np.max(np.abs(tail)) > 0: 
        tail /= np.max(np.abs(tail))

    return tail.astype(np.float32)

def save_wav(path, data, rate):
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val
    output_data = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output_data)
    print(f"Saved: {path}")

def main():
    print("Generating S04 Void IR (Abyss)...")

    # Generate Void IR
    # Duration: 3.0s, Decay: 2.5s
    print("Synthesizing Void IR (2.5s Decay, Dark)...")
    ir_void = generate_void_ir(3.0, 2.5, SAMPLE_RATE)
    
    save_wav(os.path.join(OUTPUT_DIR, "asset_S04_void_ir.wav"), ir_void, SAMPLE_RATE)

    print("Done.")

if __name__ == "__main__":
    main()
