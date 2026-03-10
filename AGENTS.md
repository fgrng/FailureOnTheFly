# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FailureOnTheFly is a Specify-Driven Development (SDD) template repository. It provides a methodology framework for AI-assisted software development — not application code. It is language/framework agnostic and ready to bootstrap any project.

## Repository Structure

- `.claude/commands/` — 9 custom Claude commands implementing the SDD workflow
- `.specify/templates/` — Document templates (spec, plan, tasks, checklist, constitution, agent-file)
- `.specify/scripts/bash/` — Automation scripts (common.sh, setup-plan.sh, check-prerequisites.sh, create-new-feature.sh, update-agent-context.sh)
- `specs/[NNN-feature-name]/` — Feature specifications created during development (spec.md, plan.md, tasks.md, research.md, data-model.md, contracts/, checklists/)
- `.specify/memory/constitution.md` — Project governance principles (created once)

## SDD Workflow

The core workflow follows this sequence:

```
constitution → specify → clarify → plan → tasks → analyze → implement
```

Each phase has a corresponding `/speckit.*` command. Checklist generation is available at any phase.

## Key Conventions

- **Feature branches**: `[NNN]-[short-name]` (e.g., `001-user-auth`)
- **Spec directories**: `specs/[NNN-feature-name]/`
- **Task IDs**: `T001`, `T002`, etc. with `[P]` marker for parallelizable tasks and `[US1]` for user story association
- **Requirements IDs**: `FR-001`, `FR-002` (functional), `SC-001`, `SC-002` (success criteria)
- **User stories**: Prioritized as P1, P2, P3; each independently implementable and testable
- **Acceptance scenarios**: Given/When/Then format

## Scripts

All scripts in `.specify/scripts/bash/` support `--json` for machine-readable output. Key environment variables:
- `SPECIFY_FEATURE` — Override current feature detection (useful in non-git repos)

## No Build System

This is intentionally a pure template. There is no package.json, build tooling, testing framework, or CI/CD configuration. These are added per-feature during implementation.

## Active Technologies
- Python 3.11+ + FastAPI, instructor, openai, pydantic, uvicorn, python-multipart (001-diagnostic-training-sim)
- In-memory (Python dict) — prototype scope, no database (001-diagnostic-training-sim)
- Python 3.11+ + streamlit, instructor, openai, pydantic (001-diagnostic-training-sim)
- In-memory (Streamlit session state) — prototype scope, no database (001-diagnostic-training-sim)

## Recent Changes
- 001-diagnostic-training-sim: Added Python 3.11+ + FastAPI, instructor, openai, pydantic, uvicorn, python-multipart
