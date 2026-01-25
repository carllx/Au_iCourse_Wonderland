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
SOURCE_FILE = os.path.join(PROJECT_ROOT, "docs/course_materials/_shared_assets/dry_voice_clean.wav")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/course_materials/03_special_effects")

def load_audio(path):
    print(f"Loading: {path}")
    if not os.path.exists(path):
        print("Error: File not found.")
        return None, None
    rate, data = wavfile.read(path)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)
    return rate, data

def save_wav(path, data, rate):
    data = np.clip(data, -1.0, 1.0)
    output = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output)
    print(f"Saved: {path}")

# ==========================================
# Effect 1: Telephone (Bandpass + Distortion)
# ==========================================
def apply_telephone_eq(audio, rate):
    # Standard Telephone Bandwidth: 300Hz - 3400Hz
    nyquist = rate / 2
    low = 300 / nyquist
    high = 3400 / nyquist
    b, a = scipy.signal.butter(4, [low, high], btype='band')
    return scipy.signal.lfilter(b, a, audio)

def apply_distortion(audio, gain=5.0, mix=0.8):
    # Soft Clipping (Tanh)
    # 1. Drive
    driven = audio * gain
    # 2. Waveshaping
    distorted = np.tanh(driven)
    # 3. Mix
    output = (distorted * mix) + (audio * (1-mix))
    # 4. Cleanup output gain roughly
    return output * 0.5

# ==========================================
# Effect 2: Monster (Pitch Shift via Resampling)
# ==========================================
def apply_monster_pitch(audio, rate, semitones=-4):
    factor = 2 ** (semitones / 12.0)
    new_length = int(len(audio) / factor)
    processed = scipy.signal.resample(audio, new_length)
    return processed

# ==========================================
# Effect 3: Bad Signal (Dropouts & Static)
# ==========================================
def apply_bad_signal(audio, rate):
    samples = len(audio)
    broken = audio.copy()
    
    # 1. Random Dropouts (Reduced frequency)
    # 2 dropouts per second (was 8)
    num_dropouts = int(samples / rate * 2) 
    
    for _ in range(num_dropouts):
        start = np.random.randint(0, samples - 1000)
        # Length: 20ms to 100ms
        duration = np.random.randint(int(0.02 * rate), int(0.1 * rate))
        end = min(start + duration, samples)
        broken[start:end] = 0.0
        
        # 2. Add Static Burst (Softer)
        if start < samples:
            broken[start] += 0.2 # Reduced click
            
    # 3. Background Static (Much Softer)
    static = np.random.normal(0, 0.005, samples).astype(np.float32) # Reduced from 0.05
    
    return broken + static

def main():
    print("Generating SFX Assets...")
    
    rate, audio = load_audio(SOURCE_FILE)
    if audio is None: return

    # 1. Telephone Voice
    print("Creating Telephone Voice (EQ + Distortion)...")
    phone = apply_telephone_eq(audio, rate)
    phone_dist = apply_distortion(phone, gain=10.0)
    save_wav(os.path.join(OUTPUT_DIR, "vocal_telephone.wav"), phone_dist, rate)
    
    # 1.5 Telephone Broken (New Request)
    print("Creating Broken Telephone (Signal Instability)...")
    # Apply bad signal logic ON TOP of the telephone EQ
    phone_broken = apply_bad_signal(phone_dist, rate)
    save_wav(os.path.join(OUTPUT_DIR, "vocal_telephone_broken.wav"), phone_broken, rate)
    
    # 2. Monster Voice
    print("Creating Monster Voice (Pitch -5 semitones)...")
    # -5 semitones slows it down significantly, making it sound huge
    monster = apply_monster_pitch(audio, rate, -5)
    save_wav(os.path.join(OUTPUT_DIR, "vocal_monster.wav"), monster, rate)
    
    print("Done.")

if __name__ == "__main__":
    main()
