#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script: Make It Hiss (White Noise Injector)
Description: Adds white noise to a clean audio file to create a 'bad' asset for repair practice.
Usage: python3 make_it_hiss.py --input <path> --output <path> --level <dB_reduction>
"""

import argparse
import numpy as np
from scipy.io import wavfile
import os
import sys

def add_white_noise(input_path, output_path, noise_level_db):
    """
    Adds white noise to an audio file.
    
    Args:
        input_path (str): Path to input WAV file.
        output_path (str): Path to output WAV file.
        noise_level_db (float): Noise level in dB relative to full scale (approximate) or mixing ratio.
                                Here we interpret it as the noise amplitude scaling factor in dB 
                                relative to the signal's max amplitude.
                                e.g. -20 means noise peak is 20dB lower than signal peak.
    """
    print(f"Loading: {input_path}")
    
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    try:
        sample_rate, data = wavfile.read(input_path)
    except Exception as e:
        print(f"Error reading WAV file: {e}")
        sys.exit(1)

    # Normalize data for processing if it's integer type
    original_dtype = data.dtype
    if np.issubdtype(original_dtype, np.integer):
        # Determine max value for normalization
        max_val = np.iinfo(original_dtype).max
        signal = data.astype(np.float32) / max_val
    else:
        signal = data
        max_val = 1.0

    # Generate white noise matching signal shape
    rng = np.random.default_rng()
    noise = rng.standard_normal(signal.shape)

    # Calculate scaling factor
    # noise_level_db = 20 * log10(scale)
    # scale = 10 ^ (noise_level_db / 20)
    scale = 10 ** (noise_level_db / 20.0)
    
    # Adjust noise amplitude relative to signal's peak amplitude
    signal_peak = np.max(np.abs(signal))
    if signal_peak == 0:
        signal_peak = 1.0 # Avoid division by zero for silent files
        
    scaled_noise = noise * scale * signal_peak

    # Mix
    mixed_signal = signal + scaled_noise

    # Clip to prevent clipping distortion (hard limit at -1.0 to 1.0)
    mixed_signal = np.clip(mixed_signal, -1.0, 1.0)

    # Convert back to original data type
    if np.issubdtype(original_dtype, np.integer):
        output_data = (mixed_signal * max_val).astype(original_dtype)
    else:
        output_data = mixed_signal.astype(original_dtype)

    print(f"Injecting White Noise at {noise_level_db}dB relative to signal peak...")
    wavfile.write(output_path, sample_rate, output_data)
    print(f"Saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Inject white noise into an audio file.")
    parser.add_argument("--input", "-i", required=True, help="Input WAV file path")
    parser.add_argument("--output", "-o", required=True, help="Output WAV file path")
    parser.add_argument("--level", "-l", type=float, default=-20.0, help="Noise level in dB (relative to signal peak). Default: -20")

    args = parser.parse_args()

    add_white_noise(args.input, args.output, args.level)

if __name__ == "__main__":
    main()
