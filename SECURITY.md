# Security Policy

## Supported Versions

Only the current active release of each repository is supported with security updates.

| Project / Ecosystem | Supported Version | Notes |
| :--- | :--- | :--- |
| .NET 10 Microservices & APIs | `10.0.x` | Microsoft LTS baseline |
| Python / FastAPI Services | `3.12.x` / `3.13.x` | Active Python releases |
| Vue 3 / React 19 Frontend Clients | Latest `main` | Continuous deployment on GitHub Pages / Vercel |

## Reporting a Vulnerability

Security and data integrity are top priorities across all NainDev projects.

If you identify a potential security vulnerability, privilege escalation, or sensitive information exposure:

1. **Do not disclose the issue publicly** in an open GitHub Issue, Discussion, or pull request.
2. Submit a report through **GitHub Private Vulnerability Reporting** via the Security tab of the affected repository.
3. If Private Vulnerability Reporting is unavailable for the target repository, contact the maintainer directly:
   - **Contact**: `security@naindev.com` / `aitor.nain.mendoza@gmail.com`
   - **Subject**: `[SECURITY VULNERABILITY] <Repository Name> - <Brief Description>`

### Please Include

- A detailed description of the vulnerability and potential impact.
- Step-by-step reproduction instructions or a minimal proof-of-concept (PoC).
- Affected components, files, versions, and configurations.

## Response Commitment

- **Initial Acknowledgment**: Within 48 hours of receipt.
- **Triage & Assessment**: Within 5 business days.
- **Remediation & Patch**: Delivered via an atomic security patch commit following responsible disclosure principles.

## Security Standards & Architecture

- **Zero Hardcoded Secrets**: Production credentials, API tokens, and connection strings are injected exclusively at runtime via encrypted environment secrets (Render, Vercel, GitHub Actions Secrets).
- **Network Boundary & CSP**: Web clients enforce strict Content Security Policy (CSP) headers limiting script execution and API connection targets to explicitly declared origins.
- **Deterministic Validation**: Geometry and file processing pipelines reject untrusted inputs before passing payloads to downstream kernels.
- **Automated Dependency Scans**: Weekly grouped Dependabot checks monitor CVE advisories across NuGet, npm, pip, and GitHub Actions ecosystems.
