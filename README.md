# NainDev Engineering Standards & Reusable Workflows

Central engineering standards, organization-level default templates, and reusable GitHub Actions workflows for the NainDev ecosystem.

## Available Reusable Workflows

All workflows execute on GitHub-managed `ubuntu-latest` runners with zero operational overhead (0.00 € cost).

### 1. .NET 10 Verification (`reusable-dotnet.yml`)

Restores, checks formatting, builds in Release configuration, and executes test suites with code coverage collection.

```yaml
name: CI

on:
  push:
    branches: ["main"]
  pull_request:

jobs:
  test:
    uses: Nain9Dev/.github/.github/workflows/reusable-dotnet.yml@main
    with:
      dotnet-version: "10.0.x"
      run-format-check: false
```

### 2. Python Verification (`reusable-python.yml`)

Sets up Python with pip caching, lints with Ruff, and runs test suites via pytest or unittest.

```yaml
name: CI

on:
  push:
    branches: ["main"]
  pull_request:

jobs:
  test:
    uses: Nain9Dev/.github/.github/workflows/reusable-python.yml@main
    with:
      python-version: "3.12"
      requirements-file: "requirements.txt"
      test-command: "pytest -v"
```

### 3. Web & Node Verification (`reusable-web.yml`)

Sets up Node.js LTS, caches dependencies, executes tests, and builds production bundles.

```yaml
name: CI

on:
  push:
    branches: ["main"]
  pull_request:

jobs:
  test:
    uses: Nain9Dev/.github/.github/workflows/reusable-web.yml@main
    with:
      node-version: "22.x"
      test-command: "npm test"
      build-command: "npm run build"
```

### 4. GitHub Pages Deployment (`reusable-pages-deploy.yml`)

Builds client applications under Node.js 24 LTS, optionally runs pre-flight test suites, configures GitHub Pages, and executes atomic artifact deployment with zero duplication across portfolio demos.

```yaml
name: Deploy Live Demo

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    uses: Nain9Dev/.github/.github/workflows/reusable-pages-deploy.yml@main
    with:
      working-directory: "ProspectAI.Client"
      dist-path: "dist"
      build-command: "npm run build"
      run-tests: false
```

## Governance & Maintenance

- **[Default Pull Request Template](.github/pull_request_template.md)**: Enforces evidence-based delivery criteria (What changed, How verified, Unverified areas, Risk analysis) across all ecosystem repositories.
- **[Grouped Dependabot Standard](.github/dependabot.yml)**: Weekly automated dependency updates grouped into single PRs per ecosystem (Actions, npm, pip, nuget), eliminating notification spam and PR fatigue.
