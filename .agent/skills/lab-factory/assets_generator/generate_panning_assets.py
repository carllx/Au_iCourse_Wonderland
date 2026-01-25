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
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/course_materials/04_stereo_panning")
BPM = 100
SAMPLE_RATE = 44100

def generate_sine(freq, duration, rate):
    t = np.linspace(0, duration, int(duration * rate), False)
    return np.sin(2 * np.pi * freq * t)

def generate_square(freq, duration, rate):
    t = np.linspace(0, duration, int(duration * rate), False)
    return scipy.signal.square(2 * np.pi * freq * t)

def generate_kick(duration, rate):
    # Sine sweep 150Hz -> 50Hz
    t = np.linspace(0, duration, int(duration * rate), False)
    # Log frequency sweep
    freq = np.logspace(np.log10(150), np.log10(50), len(t))
    # Phase integral
    phase = 2 * np.pi * np.cumsum(freq) / rate
    
    # Amplitude envelope (Impact)
    env = np.exp(-t * 15) # Fast decay
    return np.sin(phase) * env

def generate_snare(duration, rate):
    # White noise burst
    noise = np.random.normal(0, 1, int(duration * rate))
    env = np.exp(-np.linspace(0, duration, len(noise)) * 20)
    return noise * env * 0.8

def generate_hat(duration, rate):
    # High pass noise
    noise = np.random.normal(0, 1, int(duration * rate))
    # High pass filter
    sos = scipy.signal.butter(10, 8000, 'hp', fs=rate, output='sos')
    filtered = scipy.signal.sosfilt(sos, noise)
    env = np.exp(-np.linspace(0, duration, len(noise)) * 50) # Very short
    return filtered * env * 0.5 

def make_loop(beat_pattern, loops):
    return np.tile(beat_pattern, loops)

def load_vocal(path):
    if not os.path.exists(path): return None
    file_rate, data = wavfile.read(path)
    
    # Normalize to Float32 -1..1
    if data.dtype == np.int16: 
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.uint8:
        data = (data.astype(np.float32) - 128) / 128.0
        
    # Mix to Mono if stereo
    if len(data.shape) > 1: 
        data = np.mean(data, axis=1)
        
    # Resample if mismatch
    if file_rate != SAMPLE_RATE:
        print(f"Resampling Vocal: {file_rate}Hz -> {SAMPLE_RATE}Hz")
        samples_target = int(len(data) * SAMPLE_RATE / file_rate)
        data = scipy.signal.resample(data, samples_target)
        
    return data

def save_wav(path, data, rate):
    data = np.clip(data, -1.0, 1.0)
    output = (data * 32767).astype(np.int16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, rate, output)
    print(f"Saved: {path}")

def pan_signal(sig, pan):
    angle = (pan + 1) * (np.pi / 4)
    return sig * np.cos(angle), sig * np.sin(angle)

def main():
    print("Generating Visceral Panning Assets (Self vs Opponent vs Threat)...")
    
    # Global Timing (Heartrate)
    # 60 BPM = 1 beat/sec.
    beat_dur = 60.0 / BPM
    bar_dur = beat_dur * 4
    
    # ==========================================
    # 1. THE OPPONENT (Track 2: Center)
    # ==========================================
    # Concept: The "Control" Group.
    # We need a clear, dry vocal to represent the external reality.
    # It occupies the CENTER (0) position, competing with the internal self.
    # The student's goal is to keep this audible despite the chaos.
    # 1. The Opponent (Vocal) - Standing opposite you.
    # Just the clean vocal.
    vocal = load_vocal(SOURCE_VOCAL)
    
    if vocal is None:
        print("Vocal not found, using dummy")
        total_duration = bar_dur * 4
        vocal_processed = np.zeros(int(total_duration*SAMPLE_RATE), dtype=np.float32)
        num_bars = 4
        total_samples = int(total_duration * SAMPLE_RATE)
    else:
        total_duration = len(vocal) / SAMPLE_RATE
        num_bars = int(np.ceil(total_duration / bar_dur)) + 1
        target_len = int(num_bars * bar_dur * SAMPLE_RATE)
        vocal_processed = np.zeros(target_len, dtype=np.float32)
        vocal_processed[:len(vocal)] = vocal
        total_samples = target_len

    save_wav(os.path.join(OUTPUT_DIR, "opponent_voice.wav"), vocal_processed, SAMPLE_RATE)

    # ==========================================
    # 2. THE SELF (Track 3: Internal/Down)
    # ==========================================
    # Concept: Biomimetic Heartbeat (Medical Realism).
    # To sound "Internal" (Bone Conduction), we cannot use a Drum Kit.
    # We simulate the physical mechanics of the heart:
    #   - S1 (Lub): Mitral Valve closure (Low Thud + Long Decay).
    #   - S2 (Dub): Aortic Valve closure (Higher Thud + Short Decay).
    #   - Blood Flow: Bandpass filtered noise (100-400Hz) gated by the pulse.
    # 2. The Self (Biomimetic Heartbeat)
    # The previous "Kick Drum" approach was too fake.
    # We will simulate the S1 (Lub) and S2 (Dub) physics.
    print("Synthesizing Biomimetic Heartbeat (Medical Realism)...")
    
    def generate_heart_transient(duration, freq_start, freq_end, noise_mix=0.0):
        t_h = np.linspace(0, duration, int(duration*SAMPLE_RATE), False)
        # 1. Tonal Component (Muscle) - Sine Sweep
        # Use a logarithmic chirp for natural decay
        phase = 2 * np.pi * (freq_start * t_h - 0.5 * (freq_start - freq_end) * t_h**2 / duration) 
        # Actually simple exp decay freq is better for percussion
        freqs = np.logspace(np.log10(freq_start), np.log10(freq_end), len(t_h))
        phases = np.cumsum(freqs) * 2 * np.pi / SAMPLE_RATE
        tone = np.sin(phases)
        
        # Envelope: Fast attack, exponential decay
        env = np.exp(-t_h * 15)
        tone *= env
        
        # 2. Texture Component (Fluid/Valve) - Filtered Noise
        noise = np.random.normal(0, 1, len(t_h))
        # Bandpass 100-300Hz for "Squish"
        sos_bp = scipy.signal.butter(2, [100, 400], 'bp', fs=SAMPLE_RATE, output='sos')
        texture = scipy.signal.sosfilt(sos_bp, noise) * env
        
        return (tone * (1-noise_mix) + texture * noise_mix)

    # Paramters for realistic heart
    # S1 (Lub): Deeper, closure of AV valves. ~60Hz
    lub = generate_heart_transient(0.15, 70, 40, noise_mix=0.4)
    # S2 (Dub): Sharper, closure of Semilunar valves. ~80Hz
    dub = generate_heart_transient(0.12, 90, 50, noise_mix=0.3)
    
    # Sequence Construction
    bar_pulse = np.zeros(int(bar_dur * SAMPLE_RATE), dtype=np.float32)
    
    # Timing: Lub at 0, Dub at 0.3s
    # Add slight random micro-timing for realism? No, keep sync for loop.
    
    def add_sound(canvas, sound, pos_sec, gain=1.0):
        idx = int(pos_sec * SAMPLE_RATE)
        l = min(len(sound), len(canvas) - idx)
        if l > 0:
            canvas[idx:idx+l] += sound[:l] * gain

    # Beat 1
    add_sound(bar_pulse, lub, 0.0, 1.0)
    add_sound(bar_pulse, dub, 0.28, 0.9) # Physiological gap ~280ms
    
    # Add a subtle "diastolic rumble" (blood filling)
    # Very low filtered noise between beats
    # rumble = np.random.normal(0, 0.05, int(0.4 * SAMPLE_RATE))
    # sos_r = scipy.signal.butter(1, 50, 'lp', fs=SAMPLE_RATE, output='sos')
    # rumble = scipy.signal.sosfilt(sos_r, rumble)
    # add_sound(bar_pulse, rumble, 0.45, 0.5)

    # Low Pass the master to put it "inside the body" (muffled high end, but keep mid for audibility)
    # Previous 60Hz was too low. 250Hz is better for "chest piece" of stethoscope.
    sos_master = scipy.signal.butter(2, 250, 'lp', fs=SAMPLE_RATE, output='sos')
    bar_pulse = scipy.signal.sosfilt(sos_master, bar_pulse)
    
    # Normalize bar
    bar_pulse = bar_pulse / np.max(np.abs(bar_pulse)) * 0.9
    
    track_heartbeat = np.tile(bar_pulse, num_bars)
    save_wav(os.path.join(OUTPUT_DIR, "internal_heartbeat_visceral.wav"), track_heartbeat, SAMPLE_RATE)
    
    track_heartbeat = np.tile(bar_pulse, num_bars)
    save_wav(os.path.join(OUTPUT_DIR, "internal_heartbeat_visceral.wav"), track_heartbeat, SAMPLE_RATE)

    # ==========================================
    # 3. THE ENVIRONMENT (Track 4 & 5: Sides)
    # ==========================================
    # Concept: Asymmetric Threat.
    # If the threat is Mono (Center), it masks the Self and Opponent.
    # We split the threat into two distinct frequency bands and pan them HARD L/R.
    # This creates a "Surround" effect that envelopes the listener.
    
    # 3. The Threat (External Environment)
    # Combined Pressure and Anxiety into distinct layers of "The Threat"
    print("Synthesizing External Threat Layers...")
    
    t = np.linspace(0, num_bars * bar_dur, total_samples, False)
    
    # Layer A: Pressure (Left) - The Wall
    # [Psychoacoustics]: Low frequencies (<100Hz) create a sense of weight/pressure.
    # By panning this HARD LEFT, we "remove" the mud from the center.
    # Layer A: Pressure (Left) - The Wall
    # Heavy, constant, suffocating.
    drone_wave = generate_square(55.0, num_bars * bar_dur, SAMPLE_RATE)
    sos_d = scipy.signal.butter(2, 100, 'lp', fs=SAMPLE_RATE, output='sos')
    pressure = scipy.signal.sosfilt(sos_d, drone_wave) * 0.3
    # Gentle breathing modulation (no hard cuts)
    pressure *= (np.sin(2*np.pi*0.1*t) * 0.3 + 0.7) 
    
    # Fade edges
    pressure[:1000] *= np.linspace(0, 1, 1000)
    pressure[-44100:] *= np.linspace(1, 0, 44100) # 1s fade out
    
    save_wav(os.path.join(OUTPUT_DIR, "external_threat_low_L.wav"), pressure, SAMPLE_RATE)
    
    # Layer B: Anxiety (Right) - The Needle
    # [Psychoacoustics]: High frequencies (>3kHz) trigger "alert/pain" responses.
    # [Math]: We use a Power Curve (surge ** 8) to create smooth, non-linear spikes.
    # This prevents the "Clicking" artifact of hard gating.
    # Layer B: Anxiety (Right) - The Nerve
    # Metallic scrape, intermittent but SMOOTH.
    s1 = np.sin(2 * np.pi * 3000 * t)
    s2 = np.sin(2 * np.pi * 3150 * t)
    metallic = (s1 + s2) * 0.05
    
    # Surge Envelope (Replacing hard clip with smooth exp)
    # Base LFO: 0..1
    base_lfo = (np.sin(2 * np.pi * 0.15 * t) + 1) * 0.5
    # Power curve to make it "spiky" but smooth (no instant drops)
    surge = base_lfo ** 8 
    
    anxiety = metallic * surge
    
    # Fade edges
    anxiety[:1000] *= np.linspace(0, 1, 1000)
    anxiety[-44100:] *= np.linspace(1, 0, 44100) # 1s fade out

    save_wav(os.path.join(OUTPUT_DIR, "external_threat_high_R.wav"), anxiety, SAMPLE_RATE)

    # 5. Reference Mix
    print("Generating Reference Mix...")
    mix_L = np.zeros(total_samples)
    mix_R = np.zeros(total_samples)
    
    # Center: Opponent + Heartbeat (Both occupy the middle, student needs to separate or clarify)
    # Actually, Heartbeat is internal (Center), Opponent is Center. They WILL clash.
    # The lab exercise is to Pan the Threat to Sides to make room for these two.
    c = vocal_processed + track_heartbeat
    l, r = pan_signal(c, 0.0)
    mix_L += l; mix_R += r
    
    # Threats -> Hard Panned
    l, r = pan_signal(pressure, -0.9)
    mix_L += l; mix_R += r
    
    l, r = pan_signal(anxiety, 0.9)
    mix_L += l; mix_R += r
    
    stereo = np.vstack((mix_L, mix_R)).T
    save_wav(os.path.join(OUTPUT_DIR, "visceral_mix_reference.wav"), stereo, SAMPLE_RATE)
    
    print("Done.")

if __name__ == "__main__":
    main()
