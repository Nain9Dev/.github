#!/usr/bin/env python3
"""Deterministic architectural conformance and ecosystem scorecard for NainDev repositories.

Scans repositories across 5 architectural pillars:
1. Documentation Governance (docs/ numbered phases or specs/ with ADRs)
2. Centralized CI/CD (adoption of Nain9Dev/.github reusable workflows)
3. Platform Status (registration in status.naindev.com synthetic probes)
4. Ecosystem Suite Coherence (inclusion of <nain-ecosystem-bar>)
5. Confidentiality & Sanitization (zero confidential client tokens or private paths)
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

# Directories strictly pruned from recursive file traversals
IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".astro",
    ".venv",
    "venv",
    "bin",
    "obj",
    "dist",
    ".pytest_cache",
    ".vscode",
    "__pycache__",
    "packages",
}

# Banned tokens that must never appear in public codebases
CONFIDENTIAL_PATTERNS = [
    re.compile(r"\bContrast\b"),
    re.compile(r"\bDavid\b"),
    re.compile(r"01-brandbook"),
]

# Registered domains monitored by status.naindev.com
KNOWN_STATUS_DOMAINS = [
    "www.naindev.com",
    "policy.naindev.com",
    "order.naindev.com",
    "drive.naindev.com",
    "notify.naindev.com",
    "tai.naindev.com",
    "3d.naindev.com",
    "parametricad.naindev.com",
    "configurator.naindev.com",
    "prospect.naindev.com",
    "write.naindev.com",
    "tickets.naindev.com",
    "gamehaven.naindev.com",
    "orbe.naindev.com",
    "pong.naindev.com",
    "brand.naindev.com",
    "status.naindev.com",
]


def audit_repository(repo_path: Path) -> Dict[str, Any]:
    """Audits a single repository directory against the 5 architectural pillars."""
    repo_name = repo_path.name
    results: Dict[str, Any] = {
        "repo": repo_name,
        "path": str(repo_path),
        "docs_score": 0,
        "ci_score": 0,
        "status_score": 0,
        "bar_score": 0,
        "security_score": 100,
        "details": [],
        "passed": True,
    }

    # 1. Documentation Governance
    has_docs = (repo_path / "docs").is_dir()
    has_specs = (repo_path / "specs").is_dir()
    has_readme = (repo_path / "README.md").is_file()

    if has_docs or has_specs:
        results["docs_score"] = 100
        results["details"].append("Formal docs/ or specs/ lifecycle present")
    elif has_readme:
        readme_text = (repo_path / "README.md").read_text(encoding="utf-8", errors="ignore")
        if "Architecture" in readme_text or "Clean Architecture" in readme_text:
            results["docs_score"] = 80
            results["details"].append("README includes architecture section")
        else:
            results["docs_score"] = 50
            results["details"].append("Basic README present without dedicated architecture section")
    else:
        results["docs_score"] = 0
        results["details"].append("Missing documentation structure")

    # 2. Centralized CI/CD Workflows
    workflows_dir = repo_path / ".github" / "workflows"
    if workflows_dir.is_dir():
        workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
        uses_reusable = False
        for wf in workflow_files:
            text = wf.read_text(encoding="utf-8", errors="ignore")
            if "Nain9Dev/.github/.github/workflows/reusable-" in text:
                uses_reusable = True
                break

        if uses_reusable or repo_name == ".github":
            results["ci_score"] = 100
            results["details"].append("Adopts centralized reusable workflows")
        elif workflow_files:
            results["ci_score"] = 70
            results["details"].append("Standalone workflows present, migration to reusable recommended")
        else:
            results["ci_score"] = 0
            results["details"].append("No GitHub Actions workflows configured")
    else:
        results["ci_score"] = 0
        results["details"].append("No .github/workflows directory found")

    # 3. Platform Status Probe Registration
    is_registered_status = False
    for domain in KNOWN_STATUS_DOMAINS:
        cname_file = repo_path / "CNAME"
        cname_public = repo_path / "public" / "CNAME"
        if cname_file.is_file() and domain in cname_file.read_text(encoding="utf-8", errors="ignore"):
            is_registered_status = True
            break
        if cname_public.is_file() and domain in cname_public.read_text(encoding="utf-8", errors="ignore"):
            is_registered_status = True
            break
        clean_name = repo_name.lower().replace("-", "").replace(".", "")
        clean_domain = domain.split(".")[0].replace("-", "")
        if clean_name in clean_domain or clean_domain in clean_name:
            is_registered_status = True
            break

    infra_repos = [".github", "engineering-handbook", "template-fastapi-vue-clean-arch", "template-dotnet-clean-arch"]
    if repo_name in infra_repos or is_registered_status:
        results["status_score"] = 100
        results["details"].append("Status monitoring verified or infrastructure-tier")
    else:
        results["status_score"] = 50
        results["details"].append("Endpoint not explicitly registered in status probes")

    # 4. Ecosystem Suite Coherence (<nain-ecosystem-bar>)
    has_bar = False
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            if f.endswith((".html", ".vue", ".astro", ".js")):
                try:
                    content = Path(root, f).read_text(encoding="utf-8", errors="ignore")
                    if "<nain-ecosystem-bar" in content or "ecosystem-bar.js" in content:
                        has_bar = True
                        break
                except Exception:
                    pass
        if has_bar:
            break

    if has_bar or repo_name in infra_repos:
        results["bar_score"] = 100
        results["details"].append("Ecosystem navigation bar integrated or infrastructure repo")
    else:
        results["bar_score"] = 40
        results["details"].append("No <nain-ecosystem-bar> detected in client markup")

    # 5. Confidentiality & Sanitization
    violations = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for f in files:
            if f.endswith((".md", ".txt", ".json", ".py", ".cs", ".ts", ".js", ".yml", ".yaml")):
                # Do not scan scanner tools or workflows that define the patterns
                if f in ("audit_ecosystem.py", "validate.yml", "sanitize_brandbook.py"):
                    continue
                p = Path(root, f)
                try:
                    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                    for line_idx, line in enumerate(lines, 1):
                        if "CONFIDENTIAL_PATTERNS" in line or "forbidden =" in line:
                            continue
                        for pattern in CONFIDENTIAL_PATTERNS:
                            if pattern.search(line):
                                violations.append(f"{p.relative_to(repo_path)}:L{line_idx} matches {pattern.pattern}")
                except Exception:
                    pass

    if violations:
        results["security_score"] = 0
        results["passed"] = False
        results["details"].append(f"Security violations found: {', '.join(violations[:3])}")
    else:
        results["security_score"] = 100
        results["details"].append("100% sanitized with zero confidential token leaks")

    # Compute total composite score
    weights = {
        "docs_score": 0.20,
        "ci_score": 0.25,
        "status_score": 0.15,
        "bar_score": 0.15,
        "security_score": 0.25,
    }
    total = sum(results[k] * w for k, w in weights.items())
    results["total_score"] = round(total, 1)

    return results


def run_ecosystem_audit(base_dir: Path) -> int:
    """Scans all sibling project directories and produces a formatted markdown report."""
    repos: List[Path] = []
    if base_dir.is_dir():
        for item in base_dir.iterdir():
            if item.is_dir() and (item / ".git").is_dir():
                repos.append(item)

    repos.sort(key=lambda p: p.name.lower())
    if not repos:
        print(f"No git repositories found in {base_dir}")
        return 1

    audits = [audit_repository(r) for r in repos]
    avg_score = round(sum(a["total_score"] for a in audits) / len(audits), 1)

    lines = [
        "# NainDev Ecosystem Architectural Scorecard",
        "",
        f"**Audited Repositories**: {len(audits)} | **Ecosystem Health Index**: {avg_score}%",
        "",
        "| Repository | Docs | Reusable CI | Status Probe | Ecosystem Bar | Security | Total Score |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]

    for a in audits:
        badge = "PASS" if a["total_score"] >= 70 and a["passed"] else "REVIEW"
        lines.append(
            f"| `{a['repo']}` | {a['docs_score']}% | {a['ci_score']}% | {a['status_score']}% | "
            f"{a['bar_score']}% | {a['security_score']}% | **{a['total_score']}%** ({badge}) |"
        )

    lines.extend([
        "",
        "### Audit Criteria Weights",
        "- **Documentation Governance (20%)**: Formal `docs/` lifecycle, numbered phases, or architecture specifications.",
        "- **Centralized CI/CD (25%)**: Delegation to `Nain9Dev/.github` reusable workflows.",
        "- **Status Observability (15%)**: Registered synthetic probes under `status.naindev.com`.",
        "- **Ecosystem Bar Coherence (15%)**: Presence of `<nain-ecosystem-bar>` web component.",
        "- **Confidentiality Gate (25%)**: Zero occurrence of sensitive client identifiers or internal paths.",
    ])

    report_md = "\n".join(lines)
    print(report_md)

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report_md + "\n")

    return 0 if avg_score >= 70 else 1


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd().parent
    sys.exit(run_ecosystem_audit(target))
