# Task: Architecture & Agent Governance Upgrade

## Status Board
*   **Total Consumed Scripts**: 0
*   **Target Duration**: 60 Minutes

## Todo List

### 1. 🛡️ Foundation: Validation & Assets
- [x] **Enhance Validator**: Upgrade `.agent/skills/validate_links.py` to enforce physical file existence check. <!-- id: 1 -->
- [x] **Asset Setup**: Create placeholder audio files in `03_MVP_Demo/assets/` to pass the new validation. (`bad_case_demo.wav` etc.) <!-- id: 2 -->

### 2. 🤖 Agent Governance (The "Cage")
- [x] **Writer (Execution)**: Update `.agent/skills/compile_transcript.md` to enforce `READ_CONTEXT` (Style + Knowledge) and `Alignment` with Course Material. <!-- id: 3 -->
- [x] **Auditor (Review)**: Create `.agent/skills/pedagogy_auditor.md` to define "Educational Audit" criteria (Director Questions + Listening Gaps). <!-- id: 4 -->
- [x] **Muse (Inspiration)**: Create `.agent/rules/creative_muse.md` to define constraints for artistic metaphors (Theme only, no technical interference). <!-- id: 5 -->

### 3. 🎧 Content Strategy: Deep Listening
- [x] **Update Action Map**: Add `ACT_Listen_xx` entries to `03_MVP_Demo/Action_Map.md`. <!-- id: 6 -->
- [x] **Update Structure**: Inject "Guided Listening" sessions (3-5 mins) into `00_Structure_Map.md` to physically fill the time gap. <!-- id: 7 -->

### 4. 🚀 Active Agent Implementation (The Executor)
- [x] **Create Executor**: Build `.agent/executors/build_factory.py` to assemble prompts from MD files. <!-- id: 8 -->
- [x] **Verify Writer**: Test `build_factory.py --task writer` and verify output contains 'Voice' and 'Knowledge'. <!-- id: 9 -->
- [x] **Verify Auditor**: Test `build_factory.py --task auditor` and verify output contains audit checklist. <!-- id: 10 -->

### 5. 📜 Governance (The Law)
- [x] **Create Protocol**: Define `.agent/rules/workflow_protocol.md` to trigger factory usage. <!-- id: 11 -->

### 6. 🔒 Security & Protocol Audit
- [x] **Vulnerability Scan**: Identify risks in agent activation (Language Protocol, Silent Failures). <!-- id: 12 -->
- [x] **Hardening**: Patch `build_factory.py` to strict Chinese Output and Fatal Error handling. <!-- id: 13 -->
