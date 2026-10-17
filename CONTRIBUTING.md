# Contributing Guidelines

Thank you for your interest in contributing to the NainDev engineering ecosystem.

We maintain high technical standards centered around deterministic validation, Clean Architecture, zero-cost operational models, and automated quality gates.

---

## Code of Conduct

All contributors and participants are expected to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). Please treat everyone with professional respect and constructive critique.

---

## Architectural Principles

1. **Deterministic Contracts**: Business rules, monetary arithmetic, and geometry validation must be deterministic. Floating-point numbers are forbidden for financial amounts (use `Decimal`).
2. **Layer Isolation**: Keep Domain free of external framework dependencies (FastAPI, EF Core, ASP.NET Core, etc.). Invariants belong in the domain; presentation only renders and captures input.
3. **Spec-Driven**: Significant changes or additions must be backed by a design document or Architectural Decision Record (ADR) under `docs/` or `specs/`.
4. **Zero-Cost Principle**: All portfolio demonstrations and public showcase repositories must run entirely within free tiers or local resources with 0.00 € recurring infrastructure cost.

---

## Development Workflow

1. **Fork and Branch**:
   - Create a feature or bugfix branch from `main`:
     ```bash
     git checkout -b feat/your-feature-name
     # or
     git checkout -b fix/your-bugfix-name
     ```
2. **Local Verification**:
   - Every repository provides automated test commands or a `Taskfile.yml`:
     ```bash
     task test   # or dotnet test / pytest / npm test
     task lint   # or dotnet format / ruff / eslint
     ```
   - All tests must pass locally before submitting changes.
3. **Commit Messages**:
   - We enforce [Conventional Commits](https://www.conventionalcommits.org/) in concise, professional English:
     - `feat(scope): add new feature description`
     - `fix(scope): resolve bug description`
     - `docs(scope): update documentation`
     - `test(scope): add regression test`
     - `refactor(scope): restructure code without changing behavior`
     - `chore(scope): update build configurations or tooling`
   - Do not include emojis, dates, or non-technical jargon in commit messages.

---

## Pull Request Process

1. Ensure the test suite passes with zero errors or regressions.
2. Complete all checklist items in the [Pull Request Template](.github/pull_request_template.md).
3. Ensure CI passes completely on your pull request.
4. Keep pull requests focused on a single atomic concern.
