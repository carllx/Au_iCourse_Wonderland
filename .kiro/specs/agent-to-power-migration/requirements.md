# Requirements Document: Agent to Power Migration

## Introduction

This specification defines the migration of an existing `.agent` directory architecture to Kiro Power format. The `.agent` system contains three skills (lab-factory, validation-suite, transcript-compiler), a rules system, knowledge base, styles, workflows, and Python executors. The migration will transform each skill into a standalone Kiro Power while preserving all functionality and addressing the limitation that Kiro Powers cannot directly execute Python/JSX scripts within the power folder.

## Glossary

- **Power**: A Kiro IDE package containing documentation, workflow guides (steering files), and optionally MCP servers
- **Skill**: An existing capability in the `.agent` architecture (lab-factory, validation-suite, transcript-compiler)
- **External Mounting**: A strategy where executable scripts remain in their original locations and are referenced via paths in power.md
- **YAML Frontmatter**: Metadata section at the top of power.md containing name, description, and keywords
- **Steering File**: Markdown workflow guide within a Power that provides step-by-step instructions
- **MCP Server**: Model Context Protocol server that provides tools to the IDE (not used in this migration)

## Requirements

### Requirement 1: Power Structure Creation

**User Story:** As a developer, I want each skill converted to a Kiro Power, so that I can use them within Kiro IDE.

#### Acceptance Criteria

1. THE Migration_System SHALL create three separate Power directories under `.kiro/powers/`
2. WHEN creating Power directories, THE Migration_System SHALL use kebab-case naming (lab-factory-power, validation-suite-power, transcript-compiler-power)
3. THE Migration_System SHALL create a power.md file in each Power directory as the primary documentation
4. THE Migration_System SHALL include YAML frontmatter in each power.md with name, description, and keywords fields
5. WHERE a skill has multiple capabilities, THE Migration_System SHALL document all capabilities in a single power.md

### Requirement 2: Content Migration and Flattening

**User Story:** As a developer, I want all skill documentation consolidated into power.md, so that I have a single source of truth for each Power.

#### Acceptance Criteria

1. WHEN migrating a skill, THE Migration_System SHALL merge SKILL.md content into power.md
2. WHEN migrating a skill, THE Migration_System SHALL integrate relevant rules from `.agent/rules/` into power.md instructions
3. WHEN migrating a skill, THE Migration_System SHALL integrate relevant knowledge from `.agent/knowledge/` into power.md
4. WHEN migrating a skill, THE Migration_System SHALL integrate relevant styles from `.agent/styles/` into power.md
5. THE Migration_System SHALL preserve all technical details, constraints, and protocols from the original documentation
6. THE Migration_System SHALL maintain all code examples and usage patterns in power.md

### Requirement 3: External Script Mounting

**User Story:** As a developer, I want executable scripts to remain in their original locations, so that they continue to work without modification.

#### Acceptance Criteria

1. THE Migration_System SHALL NOT copy Python scripts into Power directories
2. THE Migration_System SHALL NOT copy JSX scripts into Power directories
3. WHEN documenting scripts, THE Migration_System SHALL include absolute or relative paths to script locations
4. WHEN documenting scripts, THE Migration_System SHALL include usage instructions with full command-line examples
5. THE Migration_System SHALL document script dependencies and prerequisites in power.md
6. WHERE scripts require specific working directories, THE Migration_System SHALL document the required execution context

### Requirement 4: Lab Factory Power Migration

**User Story:** As a developer, I want the Audition automation capabilities available as a Power, so that I can automate Adobe Audition workflows from Kiro IDE.

#### Acceptance Criteria

1. THE Migration_System SHALL create `.kiro/powers/lab-factory-power/power.md`
2. WHEN creating lab-factory-power, THE Migration_System SHALL include keywords: audition, automation, audio, jsx, extendscript
3. THE Migration_System SHALL document the Audition.jsx library API in power.md
4. THE Migration_System SHALL document the Universal_Lab_Builder.jsx in power.md
5. THE Migration_System SHALL reference script locations at `.agent/skills/lab-factory/lib/`
6. THE Migration_System SHALL document the "external mounting" pattern for including JSX libraries
7. THE Migration_System SHALL integrate robustness protocols (Traffic Light strategy) into power.md
8. THE Migration_System SHALL document known API limitations in power.md
9. THE Migration_System SHALL include fast debug protocol instructions in power.md

### Requirement 5: Validation Suite Power Migration

**User Story:** As a developer, I want validation tools available as a Power, so that I can check project health from Kiro IDE.

#### Acceptance Criteria

1. THE Migration_System SHALL create `.kiro/powers/validation-suite-power/power.md`
2. WHEN creating validation-suite-power, THE Migration_System SHALL include keywords: validation, testing, quality, links, consistency
3. THE Migration_System SHALL document all validation scripts with their purposes
4. THE Migration_System SHALL reference script locations at `.agent/skills/validation-suite/scripts/`
5. THE Migration_System SHALL include command-line usage examples for each validation script
6. THE Migration_System SHALL document script parameters and options in power.md

### Requirement 6: Transcript Compiler Power Migration

**User Story:** As a developer, I want the transcript compilation capability available as a Power, so that I can generate course transcripts from Kiro IDE.

#### Acceptance Criteria

1. THE Migration_System SHALL create `.kiro/powers/transcript-compiler-power/power.md`
2. WHEN creating transcript-compiler-power, THE Migration_System SHALL include keywords: transcript, compiler, course, content, pedagogy
3. THE Migration_System SHALL integrate LinXin_Voice.md style guide into power.md
4. THE Migration_System SHALL integrate relevant pedagogy rules into power.md
5. THE Migration_System SHALL document the compilation workflow in power.md
6. THE Migration_System SHALL reference the build_factory.py executor location
7. THE Migration_System SHALL document input requirements (Structure_Map, Performance_Map, Textbook_Index)
8. THE Migration_System SHALL include quality check criteria in power.md

### Requirement 7: Workflow Integration

**User Story:** As a developer, I want workflows converted to steering files, so that I can follow guided processes within Powers.

#### Acceptance Criteria

1. WHEN a workflow is relevant to a single Power, THE Migration_System SHALL convert it to a steering file in that Power's directory
2. WHEN a workflow is cross-cutting, THE Migration_System SHALL document it in the most relevant Power's power.md
3. THE Migration_System SHALL preserve all workflow steps and instructions
4. THE Migration_System SHALL maintain workflow trigger conditions and prerequisites
5. THE Migration_System SHALL convert `.agent/workflows/new_asset.md` to a steering file in lab-factory-power

### Requirement 8: Rules and Protocols Integration

**User Story:** As a developer, I want rules and protocols embedded in Powers, so that I follow correct procedures when using each Power.

#### Acceptance Criteria

1. WHEN a rule applies to a specific skill, THE Migration_System SHALL integrate it into the corresponding Power's power.md
2. WHEN a rule is global, THE Migration_System SHALL document it in all relevant Powers
3. THE Migration_System SHALL integrate rule_workflow_protocol.md into transcript-compiler-power
4. THE Migration_System SHALL integrate rule_mvp_conventions.md into lab-factory-power
5. THE Migration_System SHALL preserve all rule constraints and protocols

### Requirement 9: Knowledge Base Integration

**User Story:** As a developer, I want knowledge base content accessible through Powers, so that I have context when using each capability.

#### Acceptance Criteria

1. WHEN knowledge is specific to a skill, THE Migration_System SHALL integrate it into the corresponding Power's power.md
2. THE Migration_System SHALL integrate Audition_Skills_Map.md into lab-factory-power
3. THE Migration_System SHALL reference Textbook_Index.md location in transcript-compiler-power
4. THE Migration_System SHALL reference Chapter_Mapping.md location in transcript-compiler-power
5. WHERE knowledge files are large, THE Migration_System SHALL reference their locations rather than embedding full content

### Requirement 10: Executor Integration

**User Story:** As a developer, I want executors documented in Powers, so that I can run build automation from Kiro IDE.

#### Acceptance Criteria

1. THE Migration_System SHALL document build_factory.py in transcript-compiler-power
2. WHEN documenting executors, THE Migration_System SHALL include full command-line usage examples
3. THE Migration_System SHALL document executor parameters and options
4. THE Migration_System SHALL reference executor location at `.agent/executors/`
5. THE Migration_System SHALL document executor dependencies and prerequisites

### Requirement 11: Migration Validation

**User Story:** As a developer, I want to verify the migration is complete, so that I can trust the new Power structure.

#### Acceptance Criteria

1. WHEN migration is complete, THE Migration_System SHALL verify all three Powers have power.md files
2. WHEN migration is complete, THE Migration_System SHALL verify all YAML frontmatter is valid
3. WHEN migration is complete, THE Migration_System SHALL verify all script references are correct
4. WHEN migration is complete, THE Migration_System SHALL verify no executable files were copied into Power directories
5. THE Migration_System SHALL generate a migration report documenting what was migrated and where

### Requirement 12: Backward Compatibility

**User Story:** As a developer, I want the original `.agent` structure preserved, so that existing workflows continue to work during transition.

#### Acceptance Criteria

1. THE Migration_System SHALL NOT delete or modify files in `.agent/` directory
2. THE Migration_System SHALL NOT move scripts from their original locations
3. THE Migration_System SHALL create new Power files without affecting existing structure
4. WHEN migration is complete, THE Migration_System SHALL document the relationship between old and new structures
