import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import sounddevice as sd  <-- Removed global import
import scipy.io.wavfile as wav
import sys
import os

def visualize_audio(filename, render_mode=False):
    # Load audio
    try:
        fs, data = wav.read(filename)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return

    # Normalize to float -1..1
    if data.dtype == np.int16:
        data = data / 32768.0
    elif data.dtype == np.int32:
        data = data / 2147483648.0
    elif data.dtype == np.float32:
        pass

    # If stereo, take one channel
    if len(data.shape) > 1:
        data = data[:, 0]

    # Import Style Config
    try:
        sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib"))
        import style_config
        style_config.apply_style()
        print("✅ Applied Visual System Style")
    except ImportError:
        print("⚠️ Style Config not found, using default matplotlib style")

    print(f"Loaded {filename}, Sample Rate: {fs}, Duration: {len(data)/fs:.2f}s")

    # Setup visualization parameters
    window_size = 2048
    hop_size = 512

    # Setup Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Waveform Plot (Using Cycle Colors automatically from rcParams)
    x_wave = np.arange(0, window_size)
    line, = ax1.plot(x_wave, np.zeros(window_size), '-', lw=1.5) 
    ax1.set_title('Real-time Waveform')
    ax1.set_ylim(-1, 1)
    ax1.set_xlim(0, window_size)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # Spectrogram Plot (Rolling)
    spec_width = 100 
    freq_bins = window_size // 2 + 1
    spec_data = np.zeros((freq_bins, spec_width))

    # Create distinct image for spectrogram
    im = ax2.imshow(
        spec_data,
        aspect='auto',
        origin='lower',
        cmap='magma', 
        vmin=-60, vmax=0, 
        extent=[0, spec_width, 0, fs/2]
    )
    ax2.set_title('Real-time Spectrogram (Linear Freq - Mist View)')
    ax2.set_xlabel('Time Frame')
    ax2.set_ylabel('Frequency (Hz)')
    ax2.set_ylim(0, 16000)

    # Audio Callback State
    global current_idx
    current_idx = 0
    block_size = hop_size # Update every hop

    # Stream for playback
    def callback(outdata, frames, time_info, status):
        global current_idx
        if status:
            print(status)

        chunk = data[current_idx : current_idx + frames]
        if len(chunk) < frames:
            # End of file, fill with zeros or stop
            outdata[:len(chunk)] = chunk.reshape(-1, 1)
            outdata[len(chunk):] = 0
            raise sd.CallbackStop # Stop playback
        else:
            outdata[:] = chunk.reshape(-1, 1)
            current_idx += frames

    # Animation Update
    # For rendering, we don't need to skip frames to keep up, we render every frame needed for 30fps
    fps = 30

    def update_plot(frame):
        global current_idx

        # Determine position
        if render_mode:
            # frame is 0, 1, 2...
            # time = frame / fps
            # sample_pos = time * fs
            pos = int((frame / fps) * fs)
        else:
            # Real-time: usage global current_idx updated by callback
            pos = current_idx

        if pos >= len(data):
             return line, im

        # Get a chunk for waveform (recent samples)
        start_pos = max(0, pos - window_size)
        wave_chunk = data[start_pos : pos]
        # Pad if needed
        if len(wave_chunk) < window_size:
            wave_chunk = np.pad(wave_chunk, (window_size - len(wave_chunk), 0))

        line.set_ydata(wave_chunk)

        # Get a chunk for spectrum (latest window)
        start_spec = max(0, pos - window_size)
        spec_chunk = data[start_spec : pos]
        if len(spec_chunk) < window_size:
            spec_chunk = np.pad(spec_chunk, (window_size - len(spec_chunk), 0))

        # Windowing
        windowed = spec_chunk * np.hanning(window_size)
        # FFT
        spectrum = np.abs(np.fft.rfft(windowed))
        # Power -> dB
        with np.errstate(divide='ignore'):
            spec_db = 20 * np.log10(spectrum + 1e-9)

        # Roll spectrogram data
        # To make it scroll smoothly in render, we just push new column
        current_img = im.get_array()
        current_img = np.roll(current_img, -1, axis=1)
        current_img[:, -1] = spec_db

        im.set_array(current_img)

        return line, im

    if render_mode:
        print("Rendering video... This may take a while.")

        # Explicitly set ffmpeg path
        plt.rcParams['animation.ffmpeg_path'] = '/opt/homebrew/bin/ffmpeg'

        # Total frames
        total_frames = int((len(data) / fs) * fps)

        ani = animation.FuncAnimation(
            fig,
            update_plot,
            frames=total_frames,
            interval=1000/fps,
            blit=True
        )

        # Save output
        temp_video = "temp_vis.mp4"
        output_video = filename.replace(".wav", ".mp4")

        # 1. Save video (no audio)
        # extra_args=['-vcodec', 'libx264'] ensures mp4 format
        ani.save(temp_video, writer='ffmpeg', fps=fps, dpi=100, extra_args=['-vcodec', 'libx264'])

        # 2. Merge audio using ffmpeg CLI
        import subprocess
        print("Merging audio...")
        cmd = [
            "/opt/homebrew/bin/ffmpeg", "-y",
            "-i", temp_video,
            "-i", filename,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_video
        ]
        subprocess.run(cmd, check=True)

        # Cleanup
        if os.path.exists(temp_video):
            os.remove(temp_video)
        print(f"Render complete: {output_video}")

    else:
        # Start audio stream for Real-time
        try:
            import sounddevice as sd
        except ImportError:
            print("Error: 'sounddevice' module not found. Real-time playback unavailable.")
            print("Try running with --render to generate a video file instead.")
            return

        stream = sd.OutputStream(
            samplerate=fs,
            channels=1,
            callback=callback,
            blocksize=block_size
        )

        ani = animation.FuncAnimation(
            fig,
            update_plot,
            interval=25,
            blit=True,
            cache_frame_data=False
        )

        print("Starting playback...")
        with stream:
            plt.tight_layout()
            plt.show()
        print("Playback finished.")

if __name__ == "__main__":
    import os

    # Path Strategy
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(base_dir))

    default_target = os.path.join(project_root, "_Library", "S02_Purify", "asset_S02_dirty_heartbeat.wav")
    target = default_target
    render = False

    if len(sys.argv) >= 2:
        if sys.argv[1] == "--render":
            render = True
            if len(sys.argv) >= 3:
                target = sys.argv[2]
        else:
            target = sys.argv[1]
            if len(sys.argv) >= 3 and sys.argv[2] == "--render":
                render = True

    if not os.path.exists(target):
         print(f"File not found: {target}")
         # Try looking in old or other places? No, just fail.
         sys.exit(1)

    visualize_audio(target, render_mode=render)
