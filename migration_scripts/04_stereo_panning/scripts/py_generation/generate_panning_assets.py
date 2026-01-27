import os
import wave
import math

# CONFIGURATION
LESSON_ID = "04_stereo_panning"
ASSET_DIR = "../../assets"

def generate_stereo_noise(filename, duration):
    """Generate stereo white noise."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    path = os.path.join(ASSET_DIR, filename)
    print(f"Generating {path}...")
    
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Simple noise generation
        import random
        for _ in range(n_samples):
            # Left channel
            val_l = int(random.uniform(-0.5, 0.5) * 32767)
            # Right channel
            val_r = int(random.uniform(-0.5, 0.5) * 32767)
            wav_file.writeframes(val_l.to_bytes(2, 'little', signed=True))
            wav_file.writeframes(val_r.to_bytes(2, 'little', signed=True))

def main():
    print(f"--- Lesson {LESSON_ID} Asset Generator ---")
    if not os.path.exists(ASSET_DIR):
        os.makedirs(ASSET_DIR)

    # Assets for Panning Lab
    generate_stereo_noise("internal_heartbeat_visceral.wav", 3.0)
    generate_stereo_noise("external_threat_low_L.wav", 4.0)
    generate_stereo_noise("external_threat_high_R.wav", 4.0)
    
    print("Asset generation complete.")

if __name__ == "__main__":
    main()
