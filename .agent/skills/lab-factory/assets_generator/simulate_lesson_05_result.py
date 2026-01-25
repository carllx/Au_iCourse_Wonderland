import numpy as np
from scipy.io import wavfile
import scipy.signal
import os

# Configuration
SOURCE_VOCAL = "docs/course_materials/_shared_assets/dry_voice_clean.wav"
OUTPUT_DIR = "docs/course_materials/05_time_pitch"
OUTPUT_FILE = "podcast_mix_preview.wav"
SAMPLE_RATE = 44100

def load_vocal(path):
    if not os.path.exists(path): return None
    file_rate, data = wavfile.read(path)
    if data.dtype == np.int16: 
        data = data.astype(np.float32) / 32768.0
    if len(data.shape) > 1: 
        data = np.mean(data, axis=1)
    if file_rate != SAMPLE_RATE:
        data = scipy.signal.resample(data, int(len(data) * SAMPLE_RATE / file_rate))
    return data

def save_wav(path, data, rate):
    data = np.clip(data, -1.0, 1.0)
    output = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output)
    print(f"Saved: {path}")

def generate_stretched_jingle(target_dur):
    # Simulate Elastic Audio (Time Stretch, Pitch Preserved)
    # Source: 12.0s. Target: ~16s.
    # Logic: Rhythmic Arpeggio (No Drums), stretched.
    
    ratio = target_dur / 12.0
    print(f"Generating Stretched Jingle (Ratio {ratio:.2f})...")
    
    t = np.linspace(0, target_dur, int(target_dur*SAMPLE_RATE), False)
    
    # 1. Melody Arpeggio
    # Original: 80BPM 8th notes (Chill).
    # Stretched: Slower BPM.
    base_step = 60.0 / 80 / 2.0
    step = base_step * ratio # Slower steps
    
    # Melody Duration: Original 0-9s (3 Bars) -> New 0-(9*ratio)
    melody_dur = 9.0 * ratio
    notes = [440, 554, 659, 880] 
    melody = np.zeros_like(t)
    
    num_steps = int(melody_dur / step)
    for i in range(num_steps):
        note_freq = notes[i % 4]
        if i % 4 == 0: note_freq *= 0.5
        
        start = int(i * step * SAMPLE_RATE)
        local_len = 0.5 * ratio
        local_t = np.linspace(0, local_len, int(local_len*SAMPLE_RATE), False)
        
        tone = np.sin(2*np.pi*note_freq*local_t) + 0.5*np.sin(2*np.pi*note_freq*2*local_t)
        pluck = tone * np.exp(-local_t * 5/ratio)
        
        end = min(start + len(pluck), len(melody))
        melody[start:end] += pluck[:end-start] * 0.25

    # 2. Bass Pad
    bass_freq = 110 
    pad = np.sin(2*np.pi*bass_freq*t) * 0.15
    # Fade out 8.5*ratio to 9.0*ratio
    pad_vol = np.ones_like(t)
    fade_start = 8.5 * ratio
    fade_end = 9.0 * ratio
    
    fade_zone = (t >= fade_start) & (t < fade_end)
    pad_vol[fade_zone] = np.linspace(1, 0, np.sum(fade_zone))
    pad_vol[t >= fade_end] = 0
    pad *= pad_vol
    
    # 3. Outro (Starts at 9.0 * ratio)
    outro_start = 9.0 * ratio
    outro_idx = int(outro_start * SAMPLE_RATE)
    outro_len = target_dur - outro_start
    if outro_len > 0:
        out_t = np.linspace(0, outro_len, int(outro_len*SAMPLE_RATE), False)
        chord_freqs = [220, 440, 554, 659]
        final_chord = np.zeros(len(out_t))
        for f in chord_freqs:
            env = np.ones_like(out_t)
            att_len = int(0.05 * ratio * SAMPLE_RATE)
            if att_len < len(env): env[:att_len] = np.linspace(0, 1, att_len)
            env *= np.exp(-out_t*1.5/ratio)
            final_chord += np.sin(2*np.pi*f*out_t) * env * 0.2
            
        outro_layer = np.zeros_like(t)
        l_chord = min(len(final_chord), len(outro_layer)-outro_idx)
        outro_layer[outro_idx:outro_idx+l_chord] = final_chord[:l_chord]
        return melody + pad + outro_layer
    else:
        return melody + pad

def main():
    print("Simulating Elastic Audio Result...")
    
    vocal = load_vocal(SOURCE_VOCAL)
    if vocal is None:
        print("Vocal not found.")
        return
        
    vocal_dur = len(vocal) / SAMPLE_RATE
    print(f"Vocal Duration: {vocal_dur:.2f}s")
    
    # Generate Stretched Jingle
    # This simulates what happens when you drag the Stretch Tool in Audition
    bgm = generate_stretched_jingle(vocal_dur)
    
    # Safety Check lengths
    min_len = min(len(vocal), len(bgm))
    vocal = vocal[:min_len]
    bgm = bgm[:min_len]
    
    # Mix
    # Vocal Center, BGM Stereo (Simulated Width?) No, keep Mono for simplicity script
    mix = vocal * 0.6 + bgm * 0.3
    
    save_wav(os.path.join(OUTPUT_DIR, OUTPUT_FILE), mix, SAMPLE_RATE)
    print("Preview Generated.")

if __name__ == "__main__":
    main()
