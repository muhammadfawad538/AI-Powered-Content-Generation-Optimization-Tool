---
id: 1
title: "Phase 2 Planning"
stage: plan
date_iso: "2026-01-13"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "1-ai-content-tool"
branch: "1-ai-content-tool"
user: "user"
command: "/sp.plan plan for phase 2"
labels: ["planning", "phase-2", "seo", "quality", "ethics", "optimization"]
links:
  spec: "../../specs/1-ai-content-tool/spec.md"
  plan: "../../specs/1-ai-content-tool/plan_phase2.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/1-ai-content-tool/plan_phase2.md"
  - "specs/1-ai-content-tool/research_phase2.md"
  - "specs/1-ai-content-tool/data-model_phase2.md"
  - "specs/1-ai-content-tool/quickstart_phase2.md"
  - "specs/1-ai-content-tool/contracts_phase2/seo-optimization-api.yaml"
  - "specs/1-ai-content-tool/contracts_phase2/quality-review-api.yaml"
  - "specs/1-ai-content-tool/contracts_phase2/ethics-check-api.yaml"
tests_yaml:
  - "API contract validation"
  - "data model validation"
prompt_text: |
   plan for phase 2

   ## User Input

   ```text
    plan for phase 2
   ```

   You **MUST** consider the user input before proceeding (if not empty).

   ## Outline

   1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g. 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

   2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

   3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
      - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
      - Fill Constitution Check section from constitution
      - Evaluate gates (ERROR if violations unjustified)
      - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
      - Phase 1: Generate data-model.md, contracts/, quickstart.md
      - Phase 1: Update agent context by running the agent script
      - Re-evaluate Constitution Check post-design

   4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

   ## Phases

   ### Phase 0: Outline & Research

   1. **Extract unknowns from Technical Context** above:
      - For each NEEDS CLARIFICATION → research task
      - For each dependency → best practices task
      - For each integration → patterns task

   2. **Generate and dispatch research agents**:

      ```text
      For each unknown in Technical Context:
        Task: "Research {unknown} for {feature context}"
      For each technology choice:
        Task: "Find best practices for {tech} in {domain}"
      ```

   3. **Consolidate findings** in `research.md` using format:
      - Decision: [what was chosen]
      - Rationale: [why chosen]
      - Alternatives considered: [what else evaluated]

   **Output**: research.md with all NEEDS CLARIFICATION resolved

   ### Phase 1: Design & Contracts

   **Prerequisites:** `research.md` complete

   1. **Extract entities from feature spec** → `data-model.md`:
      - Entity name, fields, relationships
      - Validation rules from requirements
      - State transitions if applicable

   2. **Generate API contracts** from functional requirements:
      - For each user action → endpoint
      - Use standard REST/GraphQL patterns
      - Output OpenAPI/GraphQL schema to `/contracts/`

   3. **Agent context update**:
      - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`
      - These scripts detect which AI agent is in use
      - Update the appropriate agent-specific context file
      - Add only new technology from current plan
      - Preserve manual additions between markers

   **Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

   ## Key rules

   - Use absolute paths
   - ERROR on gate failures or unresolved clarifications

   ---

   As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

   1) Determine Stage
      - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

   2) Generate Title and Determine Routing:
      - Generate Title: 3–7 words (slug for filename)
      - Route is automatically determined by stage:
        - `constitution` → `history/prompts/constitution/`
        - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
        - `general` → `history/prompts/general/`

   3) Create and Fill PHR (Shell first; fallback agent‑native)
      - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
      - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
      - If the script fails:
        - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
        - Allocate an ID; compute the output path based on stage from step 2; write the file
        - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

   4) Validate + report
      - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
      - On failure: warn, don't block. Skip only for `/sp.phr`.
response_text: |
  Successfully created the implementation plan for Phase 2 of the AI-Powered Content Generation & Optimization Tool. The plan includes:

  1. Technical context with language (Python 3.11), dependencies for SEO and quality analysis, and performance goals
  2. Constitution check ensuring alignment with project principles
  3. Project structure extending Phase 1 with new modules for SEO, quality, and ethics features
  4. Research document with decisions on SEO analysis tools, quality review approach, plagiarism detection method, integration pattern, and performance optimization
  5. Data models for SEOAnalysis, QualityReview, and EthicsCheck requests/responses
  6. Quickstart guide with configuration and usage instructions for Phase 2 features
  7. API contracts for SEO optimization, quality review, and ethics check endpoints
  8. Updated agent context for Claude

  The plan focuses on User Stories 2 (SEO Optimization), 3 (Quality Review), and 4 (Plagiarism & Ethical Safeguard) as specified in the user requirements, building upon the foundation established in Phase 1.
outcome: |
  The Phase 2 implementation plan is complete with all required artifacts created. The plan provides a solid foundation for implementing SEO optimization, quality review, and ethical safeguard features while adhering to the project's constitution and technical requirements. Ready for the next phase of task creation and implementation.
evaluation: |
  The generated plan successfully addresses all requirements from the specification template, including technical context, constitution check, research, data models, and API contracts. The plan is comprehensive, well-structured, and aligned with the project's goals. The agent context has been updated to reflect the new technology stack.
---