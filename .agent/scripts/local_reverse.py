#!/usr/bin/env python3
import numpy as np
import scipy.io.wavfile as wav
import sys
import os

def local_reverse(input_path, output_path, silence_thresh_db=-40, min_silence_len_ms=200):
    """
    Splits audio by silence and reverses each active segment in place.
    """
    print(f"Loading {input_path}...")
    sample_rate, data = wav.read(input_path)
    
    # Handle stereo/mono
    if len(data.shape) > 1:
        data = data.mean(axis=1) # Convert to mono for simple processing
    
    # Normalize to float -1..1
    if data.dtype == np.int16:
        audio = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        audio = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.float32:
        audio = data
    else:
        raise ValueError(f"Unsupported bit depth: {data.dtype}")

    # Calculate amplitude envelope
    # Window size for RMS
    window_size = int(sample_rate * 0.01) # 10ms window
    # Simple Rectification + Smoothing could be faster but let's do simple running RMS or Abs
    # Optimization: Chunk processing to avoid OOM on huge files, but these are small assets.
    
    abs_audio = np.abs(audio)
    
    # Thresholding
    # db = 20 * log10(amp)
    # amp = 10 ** (db / 20)
    thresh_amp = 10 ** (silence_thresh_db / 20)
    
    is_active = abs_audio > thresh_amp
    
    # Dilate active regions to bridge short gaps (hysteresis) and include breaths
    # min_silence_len samples
    min_silence_samples = int(sample_rate * (min_silence_len_ms / 1000.0))
    
    # Identify segments
    # This is a simple state machine
    segments = []
    start = -1
    
    # Fast iteration or boolean masked conversion
    # Let's use scipy.ndimage if available for speed, or just simple loop optimization
    # Since files are short (<2 mins), simple loop is fine.
    
    # Better: find indices where True
    # nonzero returns indices
    # We want to group consecutive indices
    
    print("Detecting phrases...")
    
    # Smoothing is_active to bridge gaps
    # Convolve with a kernel of ones = min_silence_samples
    # If the convolution is > 0, then we are near activity.
    # Actually, simpler:
    # 1. Find all active samples.
    # 2. If gap between active samples < min_silence, merge them.
    
    active_indices = np.where(is_active)[0]
    
    if len(active_indices) == 0:
        print("Warning: Silence only.")
        wav.write(output_path, sample_rate, data.astype(np.int16)) # Write original or silence
        return

    # Differences between indices
    diffs = np.diff(active_indices)
    # Gaps are where diff > 1
    # Large gaps are where diff > min_silence_samples
    
    split_points = np.where(diffs > min_silence_samples)[0]
    
    # Construct segments
    # segment = (start_idx, end_idx)
    current_start_idx_pointer = 0
    final_segments = []
    
    for split_ptr in split_points:
        # split_ptr is the index in active_indices array
        # active_indices[split_ptr] is the end of the current segment
        # active_indices[split_ptr+1] is the start of the next
        
        start_samp = active_indices[current_start_idx_pointer]
        end_samp = active_indices[split_ptr]
        
        # Add some padding/tails to segments so we don't clip words
        start_samp = max(0, start_samp - 1000)
        end_samp = min(len(audio), end_samp + 1000)
        
        final_segments.append((start_samp, end_samp))
        current_start_idx_pointer = split_ptr + 1
        
    # Last segment
    start_samp = active_indices[current_start_idx_pointer]
    end_samp = active_indices[-1]
    start_samp = max(0, start_samp - 1000)
    end_samp = min(len(audio), end_samp + 1000)
    final_segments.append((start_samp, end_samp))
    
    print(f"Found {len(final_segments)} phrases. Reversing...")
    
    output_audio = audio.copy()
    
    for start, end in final_segments:
        # Check specific length
        chunk = output_audio[start:end]
        reversed_chunk = chunk[::-1]
        output_audio[start:end] = reversed_chunk
        
    # Fade in/out cuts to avoid clicks? 
    # For "Shadow" glitch aesthetic, clicks might be okay, but let's be safe.
    # Skipping crossfades for MVP, the "Dry" nature usually means silence is 0.
    
    # Convert back to int16
    output_data = (output_audio * 32768.0).astype(np.int16)
    
    wav.write(output_path, sample_rate, output_data)
    print(f"Saved local reverse to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python local_reverse.py input.wav output.wav")
        sys.exit(1)
        
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    
    local_reverse(in_file, out_file)
