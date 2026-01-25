---
trigger: glob
description: Enforces pedagogical scaffolding to prevent "God-View Bias" and "Naked Metaphors" in educational scripts.
globs: 01_Scripts/*.md
---

# Rule: Pedagogy Scaffolding (反上帝视角协议)

**Context**: Prevents the Agent from using future knowledge (concepts not yet introduced) in current scripts, ensuring a linear learning path for students.

## 1. The "No Naked Metaphor" Principle
**Definition**: A "Naked Metaphor" is a metaphor or role (e.g., "Director", "Magician") introduced without establishing the *need* for it first.

**Enforcement**:
**Enforcement**:
*   ❌ **Don't**: "Today we are going to be Realm Creators." (Imposed Role)
*   ✅ **Do**: "The sound is clear but feels empty (Pain). We need to give it a place to live (Need). That's why we need to build a Realm (Solution)."

## 2. SCQA Introduction Loop
All new major concepts must follow the SCQA flow:
1.  **S (Situation)**: What is the current state? (e.g., "The audio is clean.")
2.  **C (Complication)**: What is wrong with it? (e.g., "It lacks emotion and space.")
3.  **Q (Question)**: How do we fix this? (e.g., "How do we add character?")
4.  **A (Answer)**: The new Concept/Metaphor. (e.g., "We invoke a Rain Forest Realm.")
    *   **Anderson Exception**: In "Appreciation Mode", the Answer can be **Poetic/Philosophical** (e.g., "We use Reverb to build the Relic of Time"). The solution doesn't always have to be purely functional; it can be emotional.

## 3. Anti-Time Travel (No Future Leaks)
*   **Prohibited**: Referencing specific future modules/assets (e.g., "As we will see in the Alice Project") *unless* explicitly positioned as a "Mystery Box" or "Teaser".
*   **Allowed**: Referencing *generic* goals (e.g., "We will learn to shape sound").

## 4. Persona Consistency (The "Why" Rule)
*   Never upgrade the user's role (e.g., Student -> Engineer -> Director) without a **Functional Reason**.
*   Transition logic: `Current Skill Limit` -> `New Problem` -> `New Role Required`.
