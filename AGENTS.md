# FailureOnTheFly: AI Agents & Roles

This document defines the roles and responsibilities of the AI agents (Gemini CLI, Claude Code, etc.) within the FailureOnTheFly project. This project follows **Specify-Driven Development (SDD)**, where AI agents act as specialized partners throughout the development lifecycle.

## 🤖 Principal Agent: Gemini CLI

The Gemini CLI acts as the **Lead Engineer** and **Architect**. It is responsible for:
- **Research**: Investigating the existing codebase and specs.
- **Strategy**: Proposing architectural changes based on specifications.
- **Execution**: Implementing features and fixing bugs while adhering to SDD principles.
- **Validation**: Ensuring that all changes are verified through tests and align with the `Success Criteria` (SC) in the specs.

### Command Capabilities (`/speckit.*`)
Gemini CLI utilizes specialized commands defined in `.gemini/commands/` to maintain the SDD workflow:
- `/speckit.specify`: Drafts new feature specifications (`spec.md`).
- `/speckit.plan`: Formulates architectural strategies (`plan.md`).
- `/speckit.tasks`: Generates atomic, testable task lists (`tasks.md`).
- `/speckit.implement`: Executes specific tasks and updates the task list.
- `/speckit.analyze`: Performs deep-dive root cause analysis.
- `/speckit.checklist`: Generates quality assurance checklists.

## 🧑‍💻 SDD Roles

Regardless of which AI tool is used, the workflow assumes the following specialized roles:

| Role | Responsibility | Key Output |
| :--- | :--- | :--- |
| **Specifier** | Defines *what* to build based on user requirements. | `spec.md` |
| **Planner** | Defines *how* to build it (architecture, tech stack). | `plan.md` |
| **Task Master** | Breaks down the plan into small, executable units. | `tasks.md` |
| **Implementer** | Writes the code, following the plan and tasks. | Code + Tests |
| **Validator** | Verifies that the implementation meets all requirements. | Passing Tests |

## 📐 Interaction Standards

1. **Context First**: Always read the relevant `specs/` directory before starting any implementation.
2. **Persistence**: Never assume a state from a previous session; always verify the current state of `tasks.md`.
3. **Traceability**: Link implementation changes to specific Requirement IDs (e.g., `FR-001`) or User Stories (e.g., `US1`).
4. **Validation Rigor**: No task is considered "Done" without empirical verification (automated test or manual verification script).

## 🛠 Active Tools & Scripts

Agents should leverage the following internal scripts for automation:
- `.specify/scripts/bash/create-new-feature.sh`: Scaffolds a new feature spec directory.
- `.specify/scripts/bash/setup-plan.sh`: Initializes a development plan.
- `.specify/scripts/bash/check-prerequisites.sh`: Verifies the environment for a feature.

---
*For Claude-specific instructions, see `CLAUDE.md`. For project-wide mandates, see `GEMINI.md`.*
