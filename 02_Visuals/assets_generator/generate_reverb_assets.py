import numpy as np
from scipy.io import wavfile
import scipy.signal
import os

# CONFIGURATION
# ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
SOURCE_VOCAL = os.path.join(PROJECT_ROOT, "02_Visuals/assets_generator/_source/dry_voice_clean.wav")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "02_Visuals")
SAMPLE_RATE = 44100

def generate_pink_noise(samples):
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

def generate_reverb_ir(duration, decay_time, sample_rate, room_type="small"):
    samples = int(duration * sample_rate)

    # 1. Base Tail (Pink Noise)
    tail = generate_pink_noise(samples)

    # Envelope (RT60 decay)
    t = np.linspace(0, duration, samples, False)
    tau = decay_time / 6.9
    envelope = np.exp(-t / tau)
    tail = tail * envelope

    # 2. Spectral Shaping
    if room_type == "small":
        tail = apply_lowpass(tail, 3000, sample_rate) # 3kHz cutoff (Hard walls)
    else:
        tail = apply_lowpass(tail, 1500, sample_rate) # 1.5kHz cutoff (Air absorption)

    # 3. Early Reflections (ER)
    er = np.zeros(samples, dtype=np.float32)
    if room_type == "small":
        delays = [0.005, 0.012, 0.025, 0.04] 
        gains =  [0.8,   0.6,   0.4,   0.2]
    else:
        delays = [0.020, 0.045, 0.080, 0.150]
        gains =  [0.8,   0.7,   0.5,   0.3]

    for d, g in zip(delays, gains):
        idx = int(d * sample_rate)
        if idx < samples:
            width = 10 
            er[idx:idx+width] += np.random.normal(0, 1, width) * g

    # Normalize & Mix
    if np.max(np.abs(er)) > 0: er /= np.max(np.abs(er))
    if np.max(np.abs(tail)) > 0: tail /= np.max(np.abs(tail))

    # Fade in tail
    fade_in = int(0.05 * sample_rate)
    if fade_in < samples:
        tail[:fade_in] *= np.linspace(0, 1, fade_in)

    ir = (er * 0.4) + (tail * 0.6)
    return ir.astype(np.float32)

def save_wav(path, data, rate):
    max_val = np.max(np.abs(data))
    if max_val > 0: data = data / max_val
    output_data = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output_data)
    print(f"[Generate] Saved: {path}")

def main():
    print("--- Alice Asset Factory: Reverb ---")

    # 1. Generate Small Room IR (For contrast)
    ir_small = generate_reverb_ir(0.5, 0.4, SAMPLE_RATE, "small")
    save_wav(os.path.join(OUTPUT_DIR, "ir_room_small.wav"), ir_small, SAMPLE_RATE)

    # 2. Generate Large Hall IR (For The Abyss - S04)
    ir_large = generate_reverb_ir(3.0, 2.5, SAMPLE_RATE, "large")
    save_wav(os.path.join(OUTPUT_DIR, "ir_hall_large.wav"), ir_large, SAMPLE_RATE)

    print("Reverb assets generation complete.")

if __name__ == "__main__":
    main()
