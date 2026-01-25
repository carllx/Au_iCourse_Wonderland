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
SOURCE_VOCAL = os.path.join(PROJECT_ROOT, "docs/course_materials/_shared_assets/dry_voice_clean.wav")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/course_materials/02_reverb")
SAMPLE_RATE = 44100

def generate_pink_noise(samples):
    """
    Generates Pink Noise (1/f) density for the reverb tail.
    """
    white = np.random.normal(0, 1, samples).astype(np.float32)
    # 10 Hz cutoff to soften
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
    # We want a dense tail but not harsh.
    tail = generate_pink_noise(samples)
    
    # Envelope
    t = np.linspace(0, duration, samples, False)
    # RT60 decay
    tau = decay_time / 6.9
    envelope = np.exp(-t / tau)
    tail = tail * envelope
    
    # 2. Spectral Shaping (Frequency Dependant Decay approximation)
    # Real rooms absorb highs faster. We'll simulate this by static LPF on the whole tail for now (simple)
    # or dynamic? Static is safer for clarity.
    if room_type == "small":
        # Small room: brighter, but still absorbed.
        tail = apply_lowpass(tail, 3000, sample_rate) # 3kHz cutoff
    else:
        # Large hall: darker, more air absorption.
        tail = apply_lowpass(tail, 1500, sample_rate) # 1.5kHz cutoff
        
    # 3. Pre-Delay & Early Reflections (ER)
    # Create an empty buffer for ER
    er = np.zeros(samples, dtype=np.float32)
    
    # Add varying discrete echoes based on room size
    if room_type == "small":
        # Walls are close: 5ms, 12ms, 25ms
        delays = [0.005, 0.012, 0.025, 0.04] 
        gains =  [0.8,   0.6,   0.4,   0.2]
    else:
        # Walls are far: 20ms, 45ms, 80ms, 150ms
        delays = [0.020, 0.045, 0.080, 0.150]
        gains =  [0.8,   0.7,   0.5,   0.3]
        
    for d, g in zip(delays, gains):
        idx = int(d * sample_rate)
        if idx < samples:
            # Simple impulse or spread impulse?
            # Let's make it a tiny burst of noise to diffuse it slightly
            width = 10 # 10 samples
            er[idx:idx+width] += np.random.normal(0, 1, width) * g

    # Combine ER and Tail
    # Tail usually starts building up after ER. Let's fade in the tail.
    
    # Normalize individual parts
    if np.max(np.abs(er)) > 0: er /= np.max(np.abs(er))
    if np.max(np.abs(tail)) > 0: tail /= np.max(np.abs(tail))
    
    # Mix: ER leads, Tail follows
    # We'll just add them. The tail envelop already decays from 0, maybe we should fade it in?
    
    # Fade in tail to avoid "instant wall of noise"
    fade_in = int(0.05 * sample_rate) # 50ms fade in
    if fade_in < samples:
        lin_fade = np.linspace(0, 1, fade_in)
        tail[:fade_in] *= lin_fade
        
    ir = (er * 0.4) + (tail * 0.6) # Balance ER and Tail
    
    return ir.astype(np.float32)

def generate_snare_burst(sample_rate):
    # Short burst
    return generate_pink_noise(int(0.2*sample_rate)) * np.linspace(1, 0, int(0.2*sample_rate))

def convolve_audio(source, ir):
    return scipy.signal.fftconvolve(source, ir, mode='full')[:len(source)]

def save_wav(path, data, rate):
    max_val = np.max(np.abs(data))
    if max_val > 0:
        data = data / max_val
    output_data = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output_data)
    print(f"Saved: {path}")

def main():
    print("Generating Reverb Assets (Improved)...")
    
    if not os.path.exists(SOURCE_VOCAL):
        print(f"Error: {SOURCE_VOCAL} not found.")
        return
        
    rate, source = wavfile.read(SOURCE_VOCAL)
    if source.dtype == np.int16:
        source = source.astype(np.float32) / 32768.0
    if len(source.shape) > 1:
        source = np.mean(source, axis=1)
    
    # 1. Generate Small Room IR
    print("Generating Small Room IR (LPF=3kHz, ERs)...")
    ir_small = generate_reverb_ir(0.5, 0.4, rate, "small")
    save_wav(os.path.join(OUTPUT_DIR, "ir_room_small.wav"), ir_small, rate)
    
    # 2. Generate Large Hall IR
    print("Generating Large Hall IR (LPF=1.5kHz, ERs)...")
    ir_large = generate_reverb_ir(3.0, 2.5, rate, "large")
    save_wav(os.path.join(OUTPUT_DIR, "ir_hall_large.wav"), ir_large, rate)
    
    # 3. Generate Snare
    print("Generating Test Snare...")
    snare = generate_snare_burst(rate)
    save_wav(os.path.join(OUTPUT_DIR, "test_snare.wav"), snare, rate)
    
    # 4. Process Vocals - REDUCED WET LEVELS
    print("Processing Vocals...")
    
    # Small Room
    wet_small = convolve_audio(source, ir_small)
    # Mix: 70% Dry, 20% Wet (Reduced from 30)
    mix_small = (source * 0.7) + (wet_small * 0.2)
    save_wav(os.path.join(OUTPUT_DIR, "vocal_small_room.wav"), mix_small, rate)
    
    # Large Hall
    wet_large = convolve_audio(source, ir_large)
    # Mix: 60% Dry, 35% Wet (Reduced from 50)
    mix_large = (source * 0.6) + (wet_large * 0.35)
    save_wav(os.path.join(OUTPUT_DIR, "vocal_cathedral.wav"), mix_large, rate)

    print("Done.")

if __name__ == "__main__":
    main()
