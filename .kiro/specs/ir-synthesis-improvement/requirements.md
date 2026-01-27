# Requirements Document

## Introduction

This specification addresses the improvement of impulse response (IR) synthesis algorithms in `gen_S04_contrast_IRs.py`. The current implementation generates pedagogical demonstration IRs for contrasting spatial characteristics, but suffers from acoustic inaccuracies that diminish its educational value. The large hall IR, intended to demonstrate "overly civilized, wall-heavy" reverberation unsuitable for abyss scenes, must authentically simulate concert hall acoustics with proper frequency response, early reflection patterns, and reverb tail characteristics.

## Glossary

- **IR (Impulse Response)**: A recording or simulation of how a space responds to a brief sound impulse, capturing all reflections and reverberation
- **T60**: Reverberation time - the time it takes for sound to decay by 60 dB
- **ER (Early Reflections)**: The first discrete reflections arriving within ~80-100ms after the direct sound, carrying spatial information about room geometry
- **Reverb_Tail**: The diffuse late reverberation following early reflections, characterized by exponential decay
- **Pink_Noise**: Noise with equal energy per octave, exhibiting -3dB/octave spectral slope
- **Generator**: The Python script that synthesizes IR audio files
- **Concert_Hall_IR**: The large hall impulse response demonstrating "civilized" reverberation with clear wall reflections

## Requirements

### Requirement 1: Accurate Pink Noise Generation

**User Story:** As an audio educator, I want the reverb tail to use properly generated pink noise, so that the frequency response matches real-world concert hall characteristics.

#### Acceptance Criteria

1. WHEN generating pink noise, THE Generator SHALL produce a spectrum with -3dB/octave slope across the audible frequency range (20Hz-20kHz)
2. WHEN analyzing the generated pink noise spectrum, THE Generator SHALL verify that energy is approximately equal per octave band
3. THE Generator SHALL use a validated pink noise algorithm (Voss-McCartney or proper IIR filtering) rather than naive FFT manipulation
4. WHEN comparing generated pink noise to reference pink noise, THE spectral difference SHALL be less than ±1dB per octave band

### Requirement 2: Realistic Early Reflection Modeling

**User Story:** As an audio educator, I want early reflections to simulate actual concert hall geometry, so that students can hear authentic wall, ceiling, and floor reflections.

#### Acceptance Criteria

1. WHEN generating early reflections for a concert hall, THE Generator SHALL model discrete reflections from walls, ceiling, and floor based on geometric ray tracing principles
2. WHEN calculating reflection timing, THE Generator SHALL use physically plausible delays based on room dimensions (15m width, 20m length, 10m height for typical concert hall)
3. WHEN setting reflection amplitudes, THE Generator SHALL apply distance-based attenuation (inverse square law) and surface absorption coefficients
4. THE Generator SHALL include first-order reflections (direct wall/ceiling/floor bounces) and second-order reflections (corner reflections)
5. WHEN generating the early reflection pattern, THE Generator SHALL produce 8-15 discrete reflections within the first 80ms

### Requirement 3: Proper ER-to-Tail Transition

**User Story:** As an audio educator, I want a smooth transition from early reflections to diffuse reverb tail, so that the IR sounds natural and matches real concert hall behavior.

#### Acceptance Criteria

1. WHEN combining early reflections and reverb tail, THE Generator SHALL use a crossfade window rather than simple addition
2. THE Generator SHALL position the reverb tail onset at approximately 80ms after the initial impulse
3. WHEN transitioning from ER to tail, THE Generator SHALL apply a 20-40ms crossfade window to avoid discontinuities
4. THE Generator SHALL ensure early reflections decay into the tail naturally, with the tail starting at an amplitude level consistent with the last early reflections

### Requirement 4: Frequency-Dependent Decay

**User Story:** As an audio educator, I want high frequencies to decay faster than low frequencies, so that the IR exhibits realistic air absorption and material damping characteristics.

#### Acceptance Criteria

1. WHEN generating the reverb tail, THE Generator SHALL apply frequency-dependent decay rates
2. THE Generator SHALL implement faster decay for frequencies above 4kHz (air absorption)
3. WHEN calculating T60 values per frequency band, THE Generator SHALL ensure T60(8kHz) ≈ 0.6 × T60(125Hz) for concert hall characteristics
4. THE Generator SHALL use multi-band filtering or time-varying filters to achieve frequency-dependent decay

### Requirement 5: Configurable Room Parameters

**User Story:** As a developer, I want to configure room acoustic parameters, so that I can generate different hall types without modifying core algorithms.

#### Acceptance Criteria

1. THE Generator SHALL accept room dimension parameters (width, length, height)
2. THE Generator SHALL accept surface absorption coefficients per frequency band
3. THE Generator SHALL accept T60 target values per octave band
4. WHEN parameters are modified, THE Generator SHALL regenerate the IR with updated characteristics without code changes

### Requirement 6: IR Validation and Quality Metrics

**User Story:** As an audio educator, I want automated validation of generated IRs, so that I can verify they meet acoustic quality standards.

#### Acceptance Criteria

1. WHEN an IR is generated, THE Generator SHALL compute and report actual T60 values using Schroeder integration method
2. THE Generator SHALL verify that measured T60 is within ±10% of target T60
3. THE Generator SHALL compute and report the early decay time (EDT) and verify EDT ≈ T60 for diffuse fields
4. THE Generator SHALL analyze and report the clarity index (C80) to verify appropriate early-to-late energy ratio
5. WHEN validation fails, THE Generator SHALL log warnings with specific metric violations

### Requirement 7: Output File Specifications

**User Story:** As a course developer, I want generated IR files to meet technical specifications, so that they integrate properly with Adobe Audition workflows.

#### Acceptance Criteria

1. THE Generator SHALL output IR files at 48kHz sample rate in 16-bit PCM WAV format
2. THE Generator SHALL normalize IR amplitude to -1dBFS peak to prevent clipping
3. THE Generator SHALL generate mono (single-channel) IR files
4. WHEN writing output files, THE Generator SHALL preserve the existing file naming convention (contrast_IR_large_hall.wav)
5. THE Generator SHALL create output directories if they do not exist

### Requirement 8: Round-Trip Validation

**User Story:** As a developer, I want to validate that IR generation is deterministic and reproducible, so that course materials remain consistent across builds.

#### Acceptance Criteria

1. WHEN generating an IR with fixed random seed, THE Generator SHALL produce bit-identical output on repeated runs
2. THE Generator SHALL accept an optional random seed parameter for reproducibility
3. WHEN no seed is provided, THE Generator SHALL use a default seed value for consistency
4. FOR ALL generated IRs, loading then analyzing then regenerating with same parameters SHALL produce equivalent acoustic metrics (±1% tolerance)
