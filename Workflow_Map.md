# Unified Workflow Map

> **Architecture Note**: All workflows now integrate the **INI Framework** (Integrated Narrative Integrity).

## Core Commands (The "Big 4")

| Slash Command | Role | Description | INI Check? |
| :--- | :--- | :--- | :--- |
| **`/write`** | **Writer** | **Create Scripts**. Auto-injects "Radio Play Protocol" prompts. | ✅ (Injection) |
| **`/audit`** | **Auditor** | **Verify Scripts**. Runs Linter + Pedagogy Rubric + Cognitive Tests. | ✅ (Linter) |
| **`/update_module`** | **Publisher** | **Release Updates**. Runs Pre-Flight Checks before SRT gen. | ✅ (Linter) |
| **`/new_visual`** | **Artist** | **Create Assets**. "Spec-First" workflow for visuals. | N/A |

### Deprecated / Legacy
*   `run_auto_review.command` -> Kept as CI/CD entry point (Runs `/audit` logic systematically).
