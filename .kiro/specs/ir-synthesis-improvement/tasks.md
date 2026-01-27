# Implementation Tasks

## Task 1: Core Utility Functions

### Task 1.1: Implement Voss-McCartney Pink Noise Generator
**Description:** Replace naive FFT-based pink noise with acoustically accurate Voss-McCartney algorithm

**Details:**
- Create `generate_pink_noise_voss(n_samples, num_sources=16)` function
- Implement multiple white noise sources updated at different rates
- Validate output has -3dB/octave spectral slope (±1dB tolerance)
- Add to all three generator scripts

**Acceptance Criteria:**
- Function generates pink noise with -3dB/octave slope
- Spectral analysis confirms ±1dB accuracy across octave bands
- Performance is comparable to existing FFT method

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 1.2: Implement Frequency-Dependent Decay System
**Description:** Add multi-band filtering to simulate air absorption and material damping

**Details:**
- Create `apply_frequency_dependent_decay(signal, sample_rate, t60_low, t60_high)` function
- Split signal into 3 bands: Low (<500Hz), Mid (500Hz-4kHz), High (>4kHz)
- Apply different exponential decay envelopes to each band
- Recombine with proper phase alignment using scipy.signal filters

**Acceptance Criteria:**
- High frequencies decay faster than low frequencies
- T60(8kHz) ≈ 0.5-0.7 × T60(125Hz)
- No audible artifacts at band boundaries
- Function works with any input signal length

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 1.3: Implement Acoustic Validation Metrics
**Description:** Add functions to measure and validate IR acoustic properties

**Details:**
- Create `measure_t60(ir, sample_rate)` using Schroeder backward integration
- Create `measure_edt(ir, sample_rate)` for early decay time
- Create `measure_c80(ir, sample_rate)` for clarity index
- Create `analyze_spectrum(signal, sample_rate)` for spectral slope verification
- Add validation report output to console

**Acceptance Criteria:**
- T60 measurement accurate within ±5% of known test IRs
- EDT and C80 calculations follow ISO 3382 standard
- Spectral analysis correctly identifies pink noise slope
- Validation reports are human-readable and informative

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

## Task 2: Update Void IR Generator

### Task 2.1: Enhance Void IR Parameters
**Description:** Update void IR generation with improved parameters for infinite space feeling

**Details:**
- Change T60 from 2.5s to 6.0s
- Change duration from 4.0s to 8.0s
- Add pre_delay_ms parameter (default 100ms)
- Add high_freq_damping parameter (default 0.5)
- Update VOID_CONFIG dictionary with new parameters

**Acceptance Criteria:**
- Generated void IR has T60 ≥ 5.5s (measured)
- Pre-delay is audible and creates distance perception
- Duration is sufficient to capture full decay

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`

---

### Task 2.2: Add Frequency Shaping to Void IR
**Description:** Apply low-pass filtering and frequency-dependent decay to create "dark, deep" void character

**Details:**
- Apply gentle low-pass filter to pink noise (cutoff ~4kHz, 12dB/octave)
- Use frequency-dependent decay with high_freq_damping = 0.5
- Reduce tail gain from 0.4 to 0.3 for more ethereal quality
- Ensure direct sound impulse remains at full amplitude

**Acceptance Criteria:**
- Void IR sounds noticeably darker than before
- High-frequency content decays faster than low frequencies
- Spectral analysis shows reduced energy above 4kHz
- Direct sound impulse is not affected by filtering

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`

---

### Task 2.3: Add Validation Output to Void Generator
**Description:** Add acoustic metric validation and reporting to void IR generation

**Details:**
- Measure and report T60 after generation
- Measure and report EDT
- Analyze and report spectral characteristics
- Print validation report to console
- Warn if metrics are outside expected ranges

**Acceptance Criteria:**
- Validation report shows T60 ≥ 5.5s
- Report confirms frequency-dependent decay is working
- Console output is clear and informative
- Warnings appear if validation fails

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`

---

## Task 3: Update Contrast IR Generator

### Task 3.1: Enhance Closet IR Parameters
**Description:** Make closet IR more claustrophobic with tighter parameters

**Details:**
- Change T60 from 0.5s to 0.2s
- Change ER duration from 80ms to 50ms
- Increase ER density (reduce probability of silence in random impulses)
- Reduce tail gain from 0.3 to 0.25
- Add frequency-dependent decay (high_freq_t60_ratio = 0.5)

**Acceptance Criteria:**
- Closet IR sounds suffocating and coffin-like
- Measured T60 is 0.18-0.22s
- Early reflections are extremely dense
- Perceptual test confirms claustrophobic character

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 3.2: Improve Hall Early Reflection Model
**Description:** Replace random burst ER with geometrically accurate discrete reflections

**Details:**
- Implement `generate_early_reflections_hall_geometric(sample_rate, room_dims)` function
- Use room dimensions: 15m width × 20m length × 10m height
- Calculate reflection delays based on geometric ray tracing
- Apply inverse square law for distance attenuation
- Include 8-12 discrete reflections within first 80ms
- Increase ER gain from 1.0 to 1.2 to emphasize "wall-heavy" character

**Acceptance Criteria:**
- Early reflections show clear discrete peaks (not random noise)
- Reflection timing is physically plausible for concert hall
- Perceptual test confirms "civilized, wall-heavy" character
- C80 metric indicates appropriate early-to-late energy ratio

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 3.3: Add Frequency-Dependent Decay to Contrast IRs
**Description:** Apply realistic air absorption to both closet and hall IRs

**Details:**
- Add frequency-dependent decay to closet IR (high_freq_t60_ratio = 0.5)
- Add frequency-dependent decay to hall IR (high_freq_t60_ratio = 0.6)
- Use multi-band filtering approach from Task 1.2
- Ensure decay is applied to reverb tail, not early reflections

**Acceptance Criteria:**
- Both IRs exhibit frequency-dependent decay
- Hall has slightly less high-freq damping than closet (0.6 vs 0.5)
- Measured T60 varies appropriately across frequency bands
- No audible artifacts from filtering

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 3.4: Add Configuration Dictionary System
**Description:** Implement SPACE_CONFIGS dictionary for easy parameter tuning

**Details:**
- Create SPACE_CONFIGS dictionary with 'closet' and 'hall' keys
- Include all acoustic parameters (t60, duration, er_density, etc.)
- Refactor generation functions to accept config dictionaries
- Add comments explaining each parameter's acoustic purpose

**Acceptance Criteria:**
- All parameters are centralized in SPACE_CONFIGS
- Changing parameters doesn't require modifying function code
- Configuration is self-documenting with clear parameter names
- Easy to add new space types in the future

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 3.5: Add Validation Output to Contrast Generator
**Description:** Add acoustic metric validation and reporting to contrast IR generation

**Details:**
- Measure and report T60 for both closet and hall
- Measure and report EDT for both spaces
- Measure and report C80 for hall (should indicate clarity)
- Print validation reports to console
- Warn if metrics are outside expected ranges

**Acceptance Criteria:**
- Closet validation shows T60 ≈ 0.2s
- Hall validation shows T60 ≈ 2.0s
- Hall C80 indicates appropriate early energy
- Console output clearly distinguishes closet vs hall metrics

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

## Task 4: Fix Wet/Dry Mixing Logic

### Task 4.1: Remove Double Dry Signal
**Description:** Fix convolution mixing to eliminate duplicated direct sound

**Details:**
- Remove dry signal addition: delete `(dry_padded * 0.7)` term
- Output pure convolution result: `final_mix = wet_sig * 1.0`
- Add detailed comments explaining convolution physics
- Explain why IR impulse already contains direct sound
- Document alternative mixing approach for future reference

**Acceptance Criteria:**
- Output contains single direct sound peak (not double)
- Void demo sounds distant and spatial (not close)
- Code comments clearly explain the physics
- No regression in file format or output path

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_wet_demo.py`

---

### Task 4.2: Add Mixing Logic Documentation
**Description:** Add comprehensive comments explaining wet/dry mixing principles

**Details:**
- Document what convolution does (includes direct sound + reflections)
- Explain why adding dry signal creates double direct sound
- Document alternative approach (reduce IR impulse, then add dry)
- Add references to acoustic principles
- Include example calculations

**Acceptance Criteria:**
- Comments explain convolution physics clearly
- Future developers understand why current approach is correct
- Alternative approaches are documented for flexibility
- Code is self-documenting

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_wet_demo.py`

---

## Task 5: Testing and Validation

### Task 5.1: Generate and Validate All IRs
**Description:** Run all generators and verify acoustic metrics meet specifications

**Details:**
- Run `gen_S04_void_ir.py` and check validation output
- Run `gen_S04_contrast_IRs.py` and check validation output
- Verify all T60 measurements are within ±10% of targets
- Verify frequency-dependent decay is working correctly
- Check spectral analysis confirms pink noise quality

**Acceptance Criteria:**
- Void IR: T60 ≥ 5.5s, pre-delay ≥ 80ms, dark spectrum
- Closet IR: T60 ≈ 0.2s, very dense ER, claustrophobic
- Hall IR: T60 ≈ 2.0s, clear geometric ER, grand character
- All validation reports show metrics within spec

**Files to test:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 5.2: Test Wet Demo with Fixed Mixing
**Description:** Generate wet demo and verify spatial characteristics

**Details:**
- Ensure dry voice file exists: `asset_S0X_dry_voice_clean.wav`
- Run `gen_S04_wet_demo.py` with void IR
- Listen to output and verify void character is present
- Check waveform for single direct sound peak
- Verify output file format (48kHz, 16-bit, mono)

**Acceptance Criteria:**
- Wet demo sounds distant and spatial (not close)
- Waveform shows single direct sound peak
- Void character (dark, infinite, ethereal) is audible
- File format matches specification

**Files to test:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_wet_demo.py`

---

### Task 5.3: Perceptual Validation Tests
**Description:** Conduct listening tests to verify pedagogical effectiveness

**Details:**
- Listen to closet IR convolved with voice: should sound suffocating, boxy
- Listen to hall IR convolved with voice: should sound grand, with clear reflections
- Listen to void IR convolved with voice: should sound infinite, dark, distant
- Compare contrast between all three spaces
- Verify pedagogical message is clear

**Acceptance Criteria:**
- Closet sounds like "coffin" or "small box"
- Hall sounds like "concert hall" or "church"
- Void sounds like "infinite abyss" or "deep space"
- Contrast between spaces is dramatic and pedagogically effective
- Students can easily distinguish spatial characteristics

**Files to test:**
- All generated IR files in `01_MVP_Demo/_Library/S04_Space/`

---

## Task 6: Documentation and Cleanup

### Task 6.1: Update Script Headers and Docstrings
**Description:** Update version numbers and documentation in all modified scripts

**Details:**
- Update version numbers to 3.0 in all three scripts
- Add detailed docstrings to all new functions
- Document acoustic principles in function comments
- Add parameter descriptions with units and ranges
- Include references to acoustic standards where applicable

**Acceptance Criteria:**
- All functions have clear docstrings
- Version numbers reflect major changes
- Acoustic principles are explained in comments
- Code is maintainable and self-documenting

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_wet_demo.py`

---

### Task 6.2: Create Validation Report Template
**Description:** Standardize validation output format across all generators

**Details:**
- Create consistent format for validation reports
- Include all relevant metrics (T60, EDT, C80, spectral analysis)
- Use clear visual formatting (boxes, separators)
- Add pass/fail indicators (✓/✗)
- Include warnings for out-of-spec metrics

**Acceptance Criteria:**
- All generators use same validation report format
- Reports are easy to read and understand
- Pass/fail status is immediately clear
- Warnings are prominent and actionable

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

## Task 7: Optional Enhancements

### Task 7.1*: Add Visualization Output
**Description:** Generate spectrograms and decay curves for visual validation

**Details:**
- Add optional matplotlib visualization
- Generate spectrogram showing frequency content over time
- Generate decay curve showing T60 measurement
- Save visualizations to output directory
- Make visualization optional (--visualize flag)

**Acceptance Criteria:**
- Spectrograms clearly show frequency-dependent decay
- Decay curves show T60 measurement process
- Visualizations are saved as PNG files
- Feature is optional and doesn't break existing workflow

**Files to modify:**
- `01_MVP_Demo/_Pipeline/generators/gen_S04_void_ir.py`
- `01_MVP_Demo/_Pipeline/generators/gen_S04_contrast_IRs.py`

---

### Task 7.2*: Add Unit Tests
**Description:** Create pytest unit tests for core utility functions

**Details:**
- Test pink noise spectral slope accuracy
- Test frequency-dependent decay correctness
- Test T60 measurement accuracy with known IRs
- Test convolution mixing logic
- Achieve >80% code coverage

**Acceptance Criteria:**
- All core functions have unit tests
- Tests pass consistently
- Code coverage >80%
- Tests run in <10 seconds

**Files to create:**
- `01_MVP_Demo/_Pipeline/generators/test_ir_synthesis.py`

---

## Execution Order

**Phase 1 - Foundation (Tasks 1.1, 1.2, 1.3):**
Build core utility functions that all generators will use

**Phase 2 - Void IR (Tasks 2.1, 2.2, 2.3):**
Update void IR generator with new parameters and validation

**Phase 3 - Contrast IRs (Tasks 3.1, 3.2, 3.3, 3.4, 3.5):**
Update contrast IR generator with improved models and validation

**Phase 4 - Mixing Fix (Tasks 4.1, 4.2):**
Fix wet/dry mixing logic and add documentation

**Phase 5 - Validation (Tasks 5.1, 5.2, 5.3):**
Test all changes and verify acoustic quality

**Phase 6 - Documentation (Tasks 6.1, 6.2):**
Update documentation and standardize output

**Phase 7 - Optional (Tasks 7.1, 7.2):**
Add enhancements if time permits

---

## Notes

- Tasks marked with `*` are optional enhancements
- Each task should be completed and tested before moving to the next
- Validation tasks (5.x) are critical - do not skip
- Perceptual testing (5.3) requires human listening - cannot be automated
- All file modifications preserve backward compatibility (file names, formats)
