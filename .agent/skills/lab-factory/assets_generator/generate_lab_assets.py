import numpy as np
from scipy.io import wavfile
import scipy.signal
import os
import random
import re

# Configuration
def get_project_root():
    """Recursively finds the project root by looking for .agent"""
    current = os.path.dirname(os.path.abspath(__file__))
    while current != "/":
        if os.path.exists(os.path.join(current, ".agent")):
            return current
        current = os.path.dirname(current)
    return os.path.dirname(os.path.abspath(__file__)) # Fallback

PROJECT_ROOT = get_project_root()
SOURCE_FILE = os.path.join(PROJECT_ROOT, "docs/course_materials/_shared_assets/dry_voice_clean.wav")
SRT_FILE = os.path.join(PROJECT_ROOT, "docs/course_materials/_shared_assets/dry_voice_clean.srt")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/course_materials/01_noise_reduction")

# Tuned Parameters (Subtler, more atmospheric)
WIND_LEVEL = 0.12    # Increased to be audible
HUM_FREQ = 60.0      
HUM_LEVEL = 0.15     # Increased to be a clear problem
CLICK_INTENSITY = 0.9 # Sharp clicks

def parse_srt(srt_path):
    if not os.path.exists(srt_path):
        print(f"Warning: SRT file not found at {srt_path}")
        return []

    timestamps = []
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) -->')
    matches = pattern.findall(content)
    for h, m, s, ms in matches:
        seconds = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0
        timestamps.append(seconds)

    return timestamps

def load_audio(path):
    print(f"Loading source: {path}")
    if not os.path.exists(path):
        print("Error: Source file not found!")
        return None, None, None

    sample_rate, data = wavfile.read(path)

    is_int16 = data.dtype == np.int16
    if is_int16:
        audio = data.astype(np.float32) / 32768.0
    else:
        audio = data.astype(np.float32)

    if len(audio.shape) > 1:
        audio = np.mean(audio, axis=1)

    return sample_rate, audio, is_int16

def save_audio(path, sample_rate, audio, is_int16):
    print(f"Saving to: {path}")
    audio = np.clip(audio, -1.0, 1.0)

    if is_int16:
        output_data = (audio * 32767).astype(np.int16)
    else:
        output_data = audio

    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, sample_rate, output_data)

def generate_dynamic_wind(shape, sample_rate):
    """
    Simulates wind by filtering Pink Noise with a slowly modulating Low-Pass Filter.
    """
    samples = shape[0]

    # 1. Base: Pink Noise
    white = np.random.normal(0, 1, samples).astype(np.float32)
    b, a = scipy.signal.butter(1, 0.05) # Static pink-ish filter
    pink = scipy.signal.lfilter(b, a, white)

    # 2. Modulation: Create an LFO (Low Frequency Oscillator) for wind gusts
    # Very slow: 0.2Hz to 0.5Hz
    t = np.linspace(0, samples/sample_rate, samples)

    # Sum of two sines for irregularity
    lfo = np.sin(2 * np.pi * 0.1 * t) + 0.5 * np.sin(2 * np.pi * 0.3 * t + 1.0)
    # Map LFO (-1.5 to 1.5) to Cutoff Frequencies (100Hz to 800Hz)
    # Wind "whoosh" is high frequency content passing through

    # Since time-varying filters are hard with lfilter, we'll approximate by 
    # amplitude modulation of different filtered bands or just amplitude modulation of a fixed lowpass.
    # A simple but effective trick for wind: 
    # Pink noise * (Base Volume + Gust Volume * LFO)
    # And maybe separate High/Low bands.

    # Let's try simple Amplitude Modulation on a Low-Passed Pink Noise first.
    # Filter it quite low (400Hz)
    b_wind, a_wind = scipy.signal.butter(2, 400/(sample_rate/2), btype='low')
    wind_tone = scipy.signal.lfilter(b_wind, a_wind, pink)

    # Apply LFO dynamics (Gusts)
    # Normalize LFO to 0.5 - 1.5 multiplier
    lfo_norm = (lfo + 2.0) / 2.5 # 0.2 to 1.4 approx

    wind = wind_tone * lfo_norm * WIND_LEVEL

    return wind.astype(np.float32)

def generate_drifting_hum(shape, sample_rate):
    """
    Hum with slight frequency and amplitude drift.
    """
    samples = shape[0]
    t = np.linspace(0, samples/sample_rate, samples, False)

    # Amplitude drift (beating) - 0.5Hz
    amp_mod = 0.8 + 0.2 * np.sin(2 * np.pi * 0.5 * t)

    # Harmonics
    hum = np.sin(2 * np.pi * HUM_FREQ * t) * HUM_LEVEL * amp_mod
    hum += np.sin(2 * np.pi * (HUM_FREQ * 3) * t) * (HUM_LEVEL * 0.3) * amp_mod # 3rd harmonic (180Hz)

    return hum.astype(np.float32)

def add_smart_clicks(audio, timestamps, sample_rate):
    audio_copy = audio.copy()
    samples = audio.shape[0]

    # Add clicks at SRT start points
    for ts in timestamps:
        idx = int(ts * sample_rate)
        # Offset slightly backwards (-0.1s to be distinct from transient)
        idx = max(0, idx - int(0.1 * sample_rate))

        if idx < samples - 100:
            audio_copy[idx] += CLICK_INTENSITY
            audio_copy[idx+1] -= CLICK_INTENSITY * 0.8

    # Randoms
    for _ in range(3):
        idx = random.randint(1000, samples - 1000)
        audio_copy[idx] += CLICK_INTENSITY * 0.6
        audio_copy[idx+1] -= CLICK_INTENSITY * 0.3

    return audio_copy

def main():
    print("Generating Enhanced Noise Assets (Wind & Drift)...")

    rate, audio, is_int16 = load_audio(SOURCE_FILE)
    if audio is None:
        return

    timestamps = parse_srt(SRT_FILE)

    # 1. Wind (Dynamic Atmosphere)
    print("Generating Wind Atmosphere...")
    wind = generate_dynamic_wind(audio.shape, rate)
    save_audio(os.path.join(OUTPUT_DIR, "noisy_voice.wav"), rate, audio + wind, is_int16)

    # 2. Drifting Hum
    print("Generating Drifting Hum...")
    hum = generate_drifting_hum(audio.shape, rate)
    save_audio(os.path.join(OUTPUT_DIR, "hum_demo.wav"), rate, audio + hum, is_int16)

    # 3. Smart Clicks
    print("Generating Smart Clicks...")
    audio_click = add_smart_clicks(audio, timestamps, rate)
    save_audio(os.path.join(OUTPUT_DIR, "click_demo.wav"), rate, audio_click, is_int16)

    # 4. Bad Case Demo (All Combined)
    print("Generating Bad Case Demo (All)...")
    audio_all = audio + wind + hum
    audio_all = add_smart_clicks(audio_all, timestamps, rate)
    save_audio(os.path.join(OUTPUT_DIR, "bad_case_demo.wav"), rate, audio_all, is_int16)

    print("All assets generated with dynamic atmosphere.")

if __name__ == "__main__":
    main()
