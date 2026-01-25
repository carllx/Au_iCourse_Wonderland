# Architecture Decision Records (ADR)

This document records the "Why" behind critical technical decisions. Future Agents **MUST NOT** revert these changes without user approval.

---

## ADR-001: Modular Architecture for MVP Demo
*   **Status**: Accepted (2026-01-25)
*   **Context**: The project previously had flat `tools` and `assets` folders, leading to confusion between "script A" and "asset B".
*   **Decision**: 
    1. Split into `_Pipeline` (Code) and `_Library` (Data).
    2. Enforce strict `[Type]_[Module]_[Name]` naming (e.g. `gen_S02_heartbeat.py` -> `asset_S02_heartbeat.wav`).
*   **Consequences**: 
    *   (+) Clear ownership. 
    *   (-) Requires Agents to follow regex rules.

---

## ADR-002: Exponential Audio Fade
*   **Status**: Accepted (2026-01-25)
*   **Context**: Linear volume fade-outs sounded abrupt because human hearing is logarithmic (`dB`).
*   **Decision**: All audio generator scripts MUST use **Exponential Fade** (Linear in dB) logic for transitions.
*   **Code Pattern**: `np.logspace(0, -3, length)` (Fade from 1.0 to 0.001)

---

## ADR-003: Linear Frequency Visualization
*   **Status**: Accepted (2026-01-25)
*   **Context**: For the "Mist/Fog" metaphor in S02, Log scale compressed high-frequency noise into a thin line.
*   **Decision**: For `render_S02_spectrum.py` specifically, we MUST use **Linear Frequency Scale** (0-16kHz) to make the noise visually fill the screen.
*   **Constraint**: Regular audio analysis usually needs Log scale. This is an artistic exception for the "Fog" metaphor.
