import numpy as np
from scipy.io import wavfile
import scipy.signal as signal
import os

def check_dirs():
    """Ensure output directory exists."""
    output_dir = "03_MVP_Demo/assets"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

def generate_organic_heartbeat(duration_sec, sample_rate=44100, bpm=60):
    """
    Generates an organic heartbeat using:
    1. Pitch-dropping sine wave (Simulates muscle contraction/kick drum).
    2. Low-pass filtered noise burst (Simulates blood flow turbulence).
    """
    t_full = np.linspace(0, duration_sec, int(sample_rate * duration_sec), endpoint=False)
    audio = np.zeros_like(t_full)
    
    beat_interval = 60.0 / bpm
    num_beats = int(duration_sec / beat_interval)
    
    # Heartbeat parameters
    # Lub (Systole): Lower, longer, stronger.
    # Dub (Diastole): Higher, shorter, sharper.
    
    for i in range(num_beats):
        start_time = i * beat_interval
        
        # --- Lub Component ---
        # 1. Pitch Drop Sine
        dur_lub = 0.12
        t_lub = np.linspace(0, dur_lub, int(sample_rate * dur_lub))
        # Pitch drop from 60Hz to 40Hz
        freq_sweep_lub = np.linspace(60, 40, len(t_lub))
        phase_lub = 2 * np.pi * np.cumsum(freq_sweep_lub) / sample_rate
        # Envelope: Fast attack, exponential decay
        env_lub = np.exp(-15 * t_lub)
        wave_lub = np.sin(phase_lub) * env_lub
        
        # 2. Blood Flow Noise (Low-passed noise)
        noise_lub = np.random.normal(0, 1, len(t_lub))
        # Low pass filter at 200Hz
        b, a = signal.butter(4, 200 / (sample_rate / 2), 'low')
        noise_lub_lp = signal.lfilter(b, a, noise_lub)
        wave_lub += noise_lub_lp * 0.4 # Mix level
        
        # Add to main track
        start_idx = int(start_time * sample_rate)
        end_idx = start_idx + len(wave_lub)
        if end_idx < len(audio):
            audio[start_idx:end_idx] += wave_lub

        # --- Dub Component (occurs ~0.25s later) ---
        # 1. Pitch Drop Sine
        dur_dub = 0.1
        t_dub = np.linspace(0, dur_dub, int(sample_rate * dur_dub))
        # Pitch drop from 80Hz to 60Hz
        freq_sweep_dub = np.linspace(80, 60, len(t_dub))
        phase_dub = 2 * np.pi * np.cumsum(freq_sweep_dub) / sample_rate
        env_dub = np.exp(-20 * t_dub)
        wave_dub = np.sin(phase_dub) * env_dub * 0.7 # Slightly quieter
        
        # 2. Blood Flow Noise
        noise_dub = np.random.normal(0, 1, len(t_dub))
        noise_dub_lp = signal.lfilter(b, a, noise_dub)
        wave_dub += noise_dub_lp * 0.3
        
        # Add to main track
        start_idx_dub = int((start_time + 0.28) * sample_rate)
        end_idx_dub = start_idx_dub + len(wave_dub)
        if end_idx_dub < len(audio):
            audio[start_idx_dub:end_idx_dub] += wave_dub

    # Normalize
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))
        
    return audio

def generate_colored_noise(length, color='pink'):
    """Generates colored noise."""
    samples = np.random.randn(length)
    if color == 'brown':
        # Brown noise is 1/f^2, -6dB/octave. Integrate white noise.
        samples = np.cumsum(samples)
    elif color == 'pink':
        # Simple 1/f approximation
        # Using the same method as before essentially (FFT scaling)
        uneven = length % 2
        X = np.fft.rfft(samples)
        S = np.sqrt(np.arange(len(X)) + 1.)
        X = X / S
        samples = np.fft.irfft(X)
        if uneven: samples = samples[:-1]
        
    # Normalize
    if np.max(np.abs(samples)) > 0:
        samples = samples / np.max(np.abs(samples))
    return samples

def generate_dynamic_atmosphere(duration_sec, sample_rate=44100):
    """
    Generates a dynamic room tone using mixed noise colors and LFO modulation.
    """
    length = int(duration_sec * sample_rate)
    
    # 1. Base Layers
    # Brown Noise: Low rumble, room presence
    brown = generate_colored_noise(length, 'brown')
    # Pink Noise: Hiss, air texture
    pink = generate_colored_noise(length, 'pink')
    
    # 2. LFO (Low Frequency Oscillation) for "Breathing"
    # Slow drift between 0.2Hz and 0.5Hz
    t = np.linspace(0, duration_sec, length)
    lfo1 = np.sin(2 * np.pi * 0.2 * t) * 0.5 + 0.5 # 0 to 1
    lfo2 = np.sin(2 * np.pi * 0.13 * t + 2) * 0.5 + 0.5
    
    # Brown noise is often steady, pink noise fluctuates
    modulated_pink = pink * (0.7 + 0.3 * lfo1) # Fluctuate by 30%
    
    # Mix
    # More Brown (60%), Less Pink (40%) for a "darker" room tone, less digital hiss
    atmosphere = (brown * 0.6) + (modulated_pink * 0.4)
    
    # Add occasional random "crackles" or variation (optional, but requested "not static")
    # Let's add very slow amplitude modulation to the whole thing
    global_drift = np.sin(2 * np.pi * 0.05 * t) * 0.2 + 0.8
    atmosphere = atmosphere * global_drift
    
    # Normalize
    if np.max(np.abs(atmosphere)) > 0:
        atmosphere = atmosphere / np.max(np.abs(atmosphere))
    
    return atmosphere

def main():
    # Output Path Strategy (Relative to script)
    # Script: _Pipeline/generators/gen_S02_heartbeat.py
    # Target: _Library/S02_Purify/asset_S02_heartbeat_subtle.wav
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up two levels: generators -> _Pipeline -> 03_MVP_Demo
    project_root = os.path.dirname(os.path.dirname(base_dir))
    output_dir = os.path.join(project_root, "_Library", "S02_Purify")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    SAMPLE_RATE = 44100
    DURATION_PER_PHASE = 8 # seconds
    TOTAL_DURATION = DURATION_PER_PHASE * 2
    
    print(f"Generating organic heartbeat... ({TOTAL_DURATION}s)")
    heartbeat = generate_organic_heartbeat(TOTAL_DURATION, SAMPLE_RATE, bpm=60)
    
    print("Generating dynamic atmosphere...")
    noise = generate_dynamic_atmosphere(TOTAL_DURATION, SAMPLE_RATE)
    
    # Envelope for Noise: Cut at 8s with 1.5s Fade Out (Dissolve)
    noise_envelope = np.zeros_like(noise)
    split_index = int(DURATION_PER_PHASE * SAMPLE_RATE)
    
    # Fade parameters
    fade_duration = 1.5 # seconds
    fade_len = int(fade_duration * SAMPLE_RATE)
    
    # Full volume until split point
    noise_envelope[:split_index] = 1.0
    
    # Exponential fade out (Linear in dB)
    # Start: 1.0 (0dB), End: 0.001 (-60dB)
    # Ensure we don't go out of bounds
    end_fade = min(split_index + fade_len, len(noise_envelope))
    actual_fade_len = end_fade - split_index
    
    if actual_fade_len > 0:
        # np.logspace start/stop are powers of 10. 
        # 1.0 = 10^0, 0.001 = 10^-3
        # We want to fade from 1.0 down to almost zero, then cut.
        noise_envelope[split_index:end_fade] = np.logspace(0, -3, actual_fade_len)
    
    # Silence after fade
    noise_envelope[end_fade:] = 0
    
    noise_shaped = noise * noise_envelope * 0.15 # 15% volume for background
    
    # Mix
    # Heartbeat needs to be prominent but Deep
    mix = (heartbeat * 0.7) + noise_shaped
    
    # Final normalization
    max_val = np.max(np.abs(mix))
    if max_val > 0:
        mix = mix / max_val * 0.9
    
    # Convert to 16-bit PCM
    mix_pcm = (mix * 32767).astype(np.int16)
    
    output_path = os.path.join(output_dir, "asset_S02_heartbeat_subtle.wav")
    
    wavfile.write(output_path, SAMPLE_RATE, mix_pcm)
    print(f"Generated Asset: {output_path}")
    print("  - Heartbeat: Pitch sweep + Blood flow noise")
    print("  - Atmosphere: Brown/Pink noise mix + LFO breathing")
    print("  - Transition: 8.0s (1.5s Dissolve)")

if __name__ == "__main__":
    main()
