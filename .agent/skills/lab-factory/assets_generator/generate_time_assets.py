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
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/course_materials/05_time_pitch")
SAMPLE_RATE = 44100

def generate_sine(freq, duration, rate):
    t = np.linspace(0, duration, int(duration * rate), False)
    return np.sin(2 * np.pi * freq * t)

def load_vocal(path):
    # Reuse load logic
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

def main():
    print("Generating Lesson 05 Assets: The Temporal Detective...")

    # 1. Load the Source
    vocal = load_vocal(SOURCE_VOCAL)
    if vocal is None:
        print("Error: Source vocal not found!")
        return

    # 2. Extract the "Clue"
    # Take a 4-second distinct phrase (e.g., from 2s to 6s)
    # The source is usually longer.
    start_sec = 2.0
    dur_sec = 4.0
    start_idx = int(start_sec * SAMPLE_RATE)
    end_idx = start_idx + int(dur_sec * SAMPLE_RATE)

    if len(vocal) > end_idx:
        clue = vocal[start_idx:end_idx]
    else:
        # If too short, just use what we have or loop
        clue = np.tile(vocal, 2)[:int(dur_sec*SAMPLE_RATE)]

    print(f"Extracted Clue: {len(clue)/SAMPLE_RATE:.2f}s")

    # ==========================================
    # ENCRYPTION STAGE 1: REVERSE
    # ==========================================
    # Simple array inversion.
    # To Fix: Student must use "Reverse" effect.
    reversed_clue = clue[::-1]

    # ==========================================
    # ENCRYPTION STAGE 2: CHIPMUNK SPEED (VARISPEED)
    # ==========================================
    # We resample to 1/3 of the length (3x Speed).
    # Ideally: This raises pitch by ~19 semitones.
    # To Fix: 
    #   Method A (Tape): Stretch 300% (Varispeed). Fixes both. TOO EASY.
    #   Method B (Elastic): Stretch 300% (Time Only). Pitch remains High. 
    #                       Then Pitch Shift -19st.
    # We will encourage Method B in the lab guide.

    speed_factor = 3.0 # 3x faster
    target_len = int(len(reversed_clue) / speed_factor)
    scrambled = scipy.signal.resample(reversed_clue, target_len)

    # ==========================================
    # ENCRYPTION STAGE 3: MASKING
    # ==========================================
    # Add a low rumble to make it sound like a "damaged tape".
    # This ensures they can't just engage "Auto-Detect".
    noise = np.random.normal(0, 0.05, len(scrambled))
    sos_lp = scipy.signal.butter(2, 200, 'lp', fs=SAMPLE_RATE, output='sos')
    rumble = scipy.signal.sosfilt(sos_lp, noise)

    # Mix: Evidence needs to be reasonably loud to be recoverable
    evidence = scrambled * 0.8 + rumble * 0.4

    # Pad with silence to allow manipulation room
    # Add 0.5s silence at both ends
    silence = np.zeros(int(0.5 * SAMPLE_RATE))
    final_output = np.concatenate((silence, evidence, silence))

    save_wav(os.path.join(OUTPUT_DIR, "evidence_tape_05.wav"), final_output, SAMPLE_RATE)
    print("Encryption Complete. The detective is ready.")

    # ==========================================
    # PRACTICAL CHALLENGE: PODCAST JINGLE (FIT TO VOICE)
    # ==========================================
    # Scenario: Voice is ~16s. Music is 12s.
    # Task: Stretch Music to 16s.
    # CRITICAL: Needs distinct Start/End to make alignment meaningful.
    print("Generating Practical Asset: Podcast Jingle (12s)...")
    bpm = 110
    total_dur = 12.0 

    t = np.linspace(0, total_dur, int(total_dur*SAMPLE_RATE), False)

    # 1. Structure: Intro (0-1s) -> Groove (1s-10s) -> Outro (10s-12s)

    # ==========================================
    # PRACTICAL CHALLENGE: PODCAST JINGLE (MUSICAL ALIGNMENT)
    # ==========================================
    # Analysis: 80 BPM. Beat=0.75s. Bar=3.0s.
    # Transition MUST happen at 9.0s (Start of Bar 4) to be musical.
    # Current Issue: 10.0s is mid-beat, causing a "Sudden Cut".
    print("Generating Practical Asset: Podcast Jingle (Aligned 9.0s)...")
    bpm = 80
    beat_dur = 60.0 / bpm 
    bar_dur = beat_dur * 4 # 3.0s
    total_dur = 12.0 

    t = np.linspace(0, total_dur, int(total_dur*SAMPLE_RATE), False)

    # 1. Rhythmic Arpeggio (Bars 1-3: 0s - 9s)
    melody_dur = 9.0 # Stop exactly at Bar 4
    notes = [440, 554, 659, 880] 
    melody = np.zeros_like(t)

    step = beat_dur / 2.0 # 8th notes
    num_steps = int(melody_dur / step)

    for i in range(num_steps):
        note_freq = notes[i % 4]
        if i % 4 == 0: note_freq *= 0.5

        start = int(i * step * SAMPLE_RATE)
        local_t = np.linspace(0, 0.5, int(0.5*SAMPLE_RATE), False)

        tone = np.sin(2*np.pi*note_freq*local_t) + 0.5*np.sin(2*np.pi*note_freq*2*local_t)
        pluck = tone * np.exp(-local_t * 5)

        end = min(start + len(pluck), len(melody))
        melody[start:end] += pluck[:end-start] * 0.25

    # 2. Bass Pad (Fades out for Transition)
    bass_freq = 110 
    pad = np.sin(2*np.pi*bass_freq*t) * 0.15
    # Fade out at 8.5s to 9.0s (Clear space for Downbeat)
    pad_vol = np.ones_like(t)
    fade_start = 8.5
    fade_end = 9.0

    fade_zone = (t >= fade_start) & (t < fade_end)
    pad_vol[fade_zone] = np.linspace(1, 0, np.sum(fade_zone))
    pad_vol[t >= fade_end] = 0
    pad *= pad_vol

    # 3. Distinct Outro: Final Chord (Bar 4: 9s - 12s)
    outro_start = 9.0
    outro_idx = int(outro_start * SAMPLE_RATE)
    outro_len = total_dur - outro_start
    out_t = np.linspace(0, outro_len, int(outro_len*SAMPLE_RATE), False)

    chord_freqs = [220, 440, 554, 659]
    final_chord = np.zeros(len(out_t))
    for f in chord_freqs:
        # Slower attack (0.05s) to avoid click, but fast enough to be a beat
        env = np.ones_like(out_t)
        att_len = int(0.05 * SAMPLE_RATE)
        if att_len < len(env):
            env[:att_len] = np.linspace(0, 1, att_len)
        env *= np.exp(-out_t*1.5)

        final_chord += np.sin(2*np.pi*f*out_t) * env * 0.2

    outro_layer = np.zeros_like(t)
    l_chord = min(len(final_chord), len(outro_layer)-outro_idx)
    outro_layer[outro_idx:outro_idx+l_chord] = final_chord[:l_chord]

    # Mix
    bgm = melody + pad + outro_layer
    save_wav(os.path.join(OUTPUT_DIR, "podcast_jingle.wav"), bgm, SAMPLE_RATE)
    print("Podcast Jingle Saved (Aligned).")

if __name__ == "__main__":
    main()
