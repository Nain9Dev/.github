#!/usr/bin/env python3
"""Deterministic Technical Blueprint SVG Banner and Social Card Generator for NainDev Projects.

Renders crisp, vector-scaled SVGs adhering strictly to the NainDev Brandbook v1.5:
- Blueprint grid coordinate lines
- Mathematical logo geometry (52.0° traversal, 14% stroke, corner fillets)
- Brand palette: Deep Blue #002B66, Signature Blue #0047AB, Accent Green #80FF00, Paper #EDF1F6
- Zero-blur 4px and 12px solid shadows (#1D1D1B)
- Dark and Light mode variants for GitHub README <picture> integration
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, List, NamedTuple


class ProjectMeta(NamedTuple):
    id: str
    name: str
    tagline: str
    stack: str
    metrics: List[str]
    domain: str
    target_dir: Path


PROJECTS: List[ProjectMeta] = [
    ProjectMeta(
        id="nainorder",
        name="NainOrder",
        tagline="Tactical DDD E-Commerce Order API with CQRS & Concurrency Tokens",
        stack=".NET 10 · Clean Architecture · EF Core + Dapper · PostgreSQL · 0.00 €",
        metrics=["p95 Latency < 42ms", "100% Stock Concurrency Safe", "Zero Client Dependencies"],
        domain="order.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/NainOrder/docs/assets"),
    ),
    ProjectMeta(
        id="nain3d",
        name="Nain3D",
        tagline="Deterministic 3D Geometric Validation Engine & Conformance Gateway",
        stack="Python 3.12 · FastAPI · OpenCASCADE · Trimesh · WebGL · 0.00 €",
        metrics=["Quantum Limit 1e-12 m²", "Checks C1-C10 Fail-Closed", "Dual-Contract Output"],
        domain="3d.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/3d-ai-conformance-demo/docs/assets"),
    ),
    ProjectMeta(
        id="nainpolicy",
        name="NainPolicy",
        tagline="High-Assurance Insurance Lifecycle & Financial Accounting Engine",
        stack=".NET 10 · Clean Architecture · SQL Server · Dapper · Vue 3 · 0.00 €",
        metrics=["Tenant Data Isolation", "Auditable Event History", "Deterministic Balance"],
        domain="policy.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/API-Gestion-Financiera/docs/assets"),
    ),
    ProjectMeta(
        id="nainprospect",
        name="NainProspect",
        tagline="Automated B2B Lead Generation Pipeline & Compliance Outreach Workbench",
        stack="Python 3.12 · FastAPI · Local LLM · Vue 3 · TypeScript · 0.00 €",
        metrics=["Sub-100ms Ingestion", "Strict RGPD Compliance", "Zero Facturable APIs"],
        domain="prospect.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/ProspectAI/docs/assets"),
    ),
    ProjectMeta(
        id="nainwrite",
        name="NainWrite ES",
        tagline="Fail-Closed Spanish Rewriting Workbench & Invariant Preservation Engine",
        stack="Python 3.12 · Local Ollama · LanguageTool · Diff Engine · 0.00 €",
        metrics=["Fail-Closed Invariants", "Meaning Preservation Gate", "Zero API Cost"],
        domain="write.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/NainWrite/docs/assets"),
    ),
    ProjectMeta(
        id="havetickets",
        name="HaveTickets",
        tagline="Deterministic High-Concurrency Cinema Ticketing & Seat Reservation Platform",
        stack=".NET 10 · Blazor WASM · Clean Architecture · EF Core · SQLite · 0.00 €",
        metrics=["Zero Overbooking Races", "Minor-Unit Exact Money", "Turnstile Admission"],
        domain="tickets.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/HaveTickets/docs/assets"),
    ),
    ProjectMeta(
        id="naindrive",
        name="NainDrive",
        tagline="Deterministic Driving School Billing, VAT Reconciliation & Document Verification",
        stack="Python 3.12 · FastAPI · Vue 3 + TS · ReportLab In-Memory · 0.00 €",
        metrics=["Exact Half-Up Rounding", "Mod-23 Identity Verification", "100% Traceability"],
        domain="drive.naindev.com",
        target_dir=Path("d:/Development/Personal-Projects/Gestion-Autoescuela-Python/docs/assets"),
    ),
]


def render_logo_svg(x: int, y: int, size: int, color_bars: str, color_diag: str) -> str:
    """Renders the mathematical NainDev isotype at specified coordinates."""
    scale = size / 440.0
    return f"""
    <g transform="translate({x}, {y}) scale({scale})">
      <defs>
        <mask id="cut_{x}_{y}">
          <rect x="0" y="0" width="440" height="440" fill="white" />
          <polygon points="60,60 160,60 340,340 240,340" fill="none" stroke="black" stroke-width="24" stroke-linejoin="miter" />
        </mask>
      </defs>
      <g mask="url(#cut_{x}_{y})">
        <rect x="60" y="60" width="100" height="280" fill="{color_bars}" rx="8" />
        <rect x="240" y="60" width="100" height="280" fill="{color_bars}" rx="8" />
      </g>
      <polygon points="60,60 160,60 340,340 240,340" fill="{color_diag}" stroke-linejoin="miter" />
    </g>
    """


def render_banner_svg(meta: ProjectMeta, mode: str) -> str:
    """Renders a 1280x360 adaptive header banner."""
    is_dark = mode == "dark"
    bg_color = "#060D1A" if is_dark else "#EDF1F6"
    grid_color = "#0F2243" if is_dark else "#C6D2E3"
    grid_major = "#1B3B6F" if is_dark else "#A8BCDA"
    border_color = "#1E3A8A" if is_dark else "#002B66"
    title_color = "#FFFFFF" if is_dark else "#002B66"
    text_muted = "#94A3B8" if is_dark else "#4E6B92"
    badge_bg = "#002B66" if is_dark else "#0047AB"
    badge_text = "#80FF00" if is_dark else "#FFFFFF"
    accent_green = "#80FF00"
    card_bg = "#0A1629" if is_dark else "#FFFFFF"
    shadow_color = "#000000" if is_dark else "#1D1D1B"

    # Logo color scheme
    logo_bars = "#38BDF8" if is_dark else "#0047AB"
    logo_diag = "#80FF00" if is_dark else "#002B66"

    # Metrics markup
    metric_elements = []
    x_offset = 64
    for i, m in enumerate(meta.metrics):
        metric_elements.append(f"""
        <g transform="translate({x_offset}, 285)">
          <rect x="0" y="0" width="220" height="42" fill="{card_bg}" stroke="{border_color}" stroke-width="1.5" rx="4" />
          <rect x="4" y="4" width="220" height="42" fill="none" stroke="{shadow_color}" stroke-width="1.5" rx="4" />
          <circle cx="16" cy="21" r="4" fill="{accent_green}" />
          <text x="28" y="25" font-family="'IBM Plex Mono', monospace" font-size="11" font-weight="600" fill="{title_color}">{m}</text>
        </g>
        """)
        x_offset += 240

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 360" width="1280" height="360">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&amp;family=Urbanist:wght@600;800;900&amp;display=swap');
      .txt-brand {{ font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.32em; text-transform: uppercase; }}
      .txt-title {{ font-family: 'Urbanist', system-ui, sans-serif; font-weight: 900; }}
      .txt-mono {{ font-family: 'IBM Plex Mono', monospace; }}
    </style>
    <pattern id="grid_{mode}" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{grid_color}" stroke-width="1" />
    </pattern>
    <pattern id="grid_major_{mode}" width="200" height="200" patternUnits="userSpaceOnUse">
      <path d="M 200 0 L 0 0 0 200" fill="none" stroke="{grid_major}" stroke-width="1.5" />
    </pattern>
  </defs>

  <!-- Background Canvas -->
  <rect width="1280" height="360" fill="{bg_color}" />
  <rect width="1280" height="360" fill="url(#grid_{mode})" opacity="0.6" />
  <rect width="1280" height="360" fill="url(#grid_major_{mode})" opacity="0.8" />
  <rect x="16" y="16" width="1248" height="328" fill="none" stroke="{border_color}" stroke-width="2" rx="4" />

  <!-- Technical Cotas & Dimensions -->
  <line x1="16" y1="36" x2="1264" y2="36" stroke="{grid_color}" stroke-width="1" stroke-dasharray="4 4" />
  <text x="32" y="29" class="txt-brand" font-size="10" font-weight="700" fill="{accent_green}">NAINDEV ARCHITECTURAL BLUEPRINT // SPEC-1.5 // 52.0°</text>
  <text x="1100" y="29" class="txt-mono" font-size="10" fill="{text_muted}">SEC: {meta.domain}</text>

  <!-- Left Content: Logo & Title -->
  {render_logo_svg(64, 60, 160, logo_bars, logo_diag)}

  <g transform="translate(250, 75)">
    <!-- Category Pill -->
    <rect x="0" y="0" width="140" height="24" fill="{badge_bg}" rx="4" />
    <text x="10" y="16" class="txt-brand" font-size="9" font-weight="700" fill="{badge_text}">ENTERPRISE SUITE</text>

    <!-- Main Project Name -->
    <text x="0" y="70" class="txt-title" font-size="52" fill="{title_color}">{meta.name}</text>

    <!-- Value Proposition -->
    <text x="0" y="105" class="txt-mono" font-size="16" font-weight="400" fill="{text_muted}">{meta.tagline}</text>

    <!-- Stack Footprint -->
    <text x="0" y="132" class="txt-mono" font-size="13" font-weight="600" fill="{accent_green}">STACK: {meta.stack}</text>
  </g>

  <!-- Technical Angle Callout & Grid Reticle -->
  <g transform="translate(1080, 80)">
    <circle cx="90" cy="90" r="70" fill="none" stroke="{grid_major}" stroke-width="1.5" stroke-dasharray="3 3" />
    <line x1="90" y1="20" x2="90" y2="160" stroke="{grid_major}" stroke-width="1" />
    <line x1="20" y1="90" x2="160" y2="90" stroke="{grid_major}" stroke-width="1" />
    <line x1="90" y1="90" x2="145" y2="35" stroke="{accent_green}" stroke-width="2" />
    <text x="105" y="60" class="txt-mono" font-size="11" font-weight="700" fill="{accent_green}">52.0°</text>
    <text x="55" y="175" class="txt-mono" font-size="9" fill="{text_muted}">COTAS: 14% ATOM</text>
  </g>

  <!-- Metrics Bar -->
  {''.join(metric_elements)}

  <!-- Live Link Callout -->
  <g transform="translate(860, 285)">
    <rect x="0" y="0" width="356" height="42" fill="{badge_bg}" stroke="{accent_green}" stroke-width="1.5" rx="4" />
    <rect x="4" y="4" width="356" height="42" fill="none" stroke="{shadow_color}" stroke-width="1.5" rx="4" />
    <text x="24" y="26" class="txt-mono" font-size="12" font-weight="700" fill="#FFFFFF">LIVE DEMO 24/7 // {meta.domain} ↗</text>
  </g>
</svg>
"""


def render_social_card_svg(meta: ProjectMeta) -> str:
    """Renders a 1280x640 OpenGraph Social Preview image."""
    bg_color = "#060D1A"
    grid_color = "#0F2243"
    grid_major = "#1B3B6F"
    border_color = "#1E3A8A"
    title_color = "#FFFFFF"
    text_muted = "#94A3B8"
    accent_green = "#80FF00"
    badge_bg = "#002B66"

    metric_cards = []
    y_pos = 460
    for i, m in enumerate(meta.metrics):
        metric_cards.append(f"""
        <g transform="translate({100 + i * 360}, {y_pos})">
          <rect x="0" y="0" width="330" height="70" fill="#0A1629" stroke="{border_color}" stroke-width="1.5" rx="6" />
          <rect x="6" y="6" width="330" height="70" fill="none" stroke="#000000" stroke-width="1.5" rx="6" />
          <circle cx="24" cy="35" r="5" fill="{accent_green}" />
          <text x="40" y="40" font-family="'IBM Plex Mono', monospace" font-size="14" font-weight="600" fill="#FFFFFF">{m}</text>
        </g>
        """)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 640" width="1280" height="640">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&amp;family=Urbanist:wght@600;800;900&amp;display=swap');
      .txt-brand {{ font-family: 'IBM Plex Mono', monospace; letter-spacing: 0.32em; text-transform: uppercase; }}
      .txt-title {{ font-family: 'Urbanist', system-ui, sans-serif; font-weight: 900; }}
      .txt-mono {{ font-family: 'IBM Plex Mono', monospace; }}
    </style>
    <pattern id="og_grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{grid_color}" stroke-width="1" />
    </pattern>
    <pattern id="og_grid_major" width="200" height="200" patternUnits="userSpaceOnUse">
      <path d="M 200 0 L 0 0 0 200" fill="none" stroke="{grid_major}" stroke-width="1.5" />
    </pattern>
  </defs>

  <rect width="1280" height="640" fill="{bg_color}" />
  <rect width="1280" height="640" fill="url(#og_grid)" opacity="0.6" />
  <rect width="1280" height="640" fill="url(#og_grid_major)" opacity="0.8" />
  <rect x="24" y="24" width="1232" height="592" fill="none" stroke="{border_color}" stroke-width="2" rx="8" />

  <!-- Top Metadata Bar -->
  <line x1="24" y1="70" x2="1256" y2="70" stroke="{grid_color}" stroke-width="1" stroke-dasharray="4 4" />
  <text x="48" y="52" class="txt-brand" font-size="12" font-weight="700" fill="{accent_green}">NAINDEV ARCHITECTURAL SHOWCASE // PRODUCTION SPEC</text>
  <text x="960" y="52" class="txt-mono" font-size="12" fill="{text_muted}">ENDPOINT: https://{meta.domain}</text>

  <!-- Central Logo & Hierarchy -->
  {render_logo_svg(100, 130, 220, "#38BDF8", "#80FF00")}

  <g transform="translate(360, 150)">
    <rect x="0" y="0" width="180" height="28" fill="{badge_bg}" stroke="{accent_green}" stroke-width="1" rx="4" />
    <text x="14" y="19" class="txt-brand" font-size="10" font-weight="700" fill="{accent_green}">ENTERPRISE SYSTEM</text>

    <text x="0" y="90" class="txt-title" font-size="64" fill="{title_color}">{meta.name}</text>
    <text x="0" y="140" class="txt-mono" font-size="19" fill="{text_muted}">{meta.tagline}</text>
    <text x="0" y="180" class="txt-mono" font-size="15" font-weight="600" fill="{accent_green}">STACK: {meta.stack}</text>
  </g>

  <!-- Technical Reticle Callout -->
  <g transform="translate(1040, 170)">
    <circle cx="80" cy="80" r="70" fill="none" stroke="{grid_major}" stroke-width="1.5" stroke-dasharray="4 4" />
    <line x1="80" y1="10" x2="80" y2="150" stroke="{grid_major}" stroke-width="1" />
    <line x1="10" y1="80" x2="150" y2="80" stroke="{grid_major}" stroke-width="1" />
    <line x1="80" y1="80" x2="135" y2="25" stroke="{accent_green}" stroke-width="2.5" />
    <text x="95" y="50" class="txt-mono" font-size="13" font-weight="700" fill="{accent_green}">52.0°</text>
  </g>

  <!-- Lower Metric Cards -->
  {''.join(metric_cards)}

  <!-- Footer Brand Baseline -->
  <line x1="24" y1="560" x2="1256" y2="560" stroke="{grid_color}" stroke-width="1" stroke-dasharray="4 4" />
  <text x="48" y="590" class="txt-mono" font-size="12" fill="{text_muted}">NainDev Full Stack Architecture // 0.00 EUR Operating Footprint // Tested &amp; Audited</text>
  <text x="1020" y="590" class="txt-mono" font-size="12" font-weight="700" fill="{accent_green}">status.naindev.com 100% OK</text>
</svg>
"""


def generate_all_banners() -> None:
    """Generates dark, light, and social preview SVGs for each flagship project."""
    for p in PROJECTS:
        p.target_dir.mkdir(parents=True, exist_ok=True)

        dark_svg = render_banner_svg(p, "dark")
        light_svg = render_banner_svg(p, "light")
        social_svg = render_social_card_svg(p)

        (p.target_dir / "banner-dark.svg").write_text(dark_svg, encoding="utf-8")
        (p.target_dir / "banner-light.svg").write_text(light_svg, encoding="utf-8")
        (p.target_dir / "social-preview.svg").write_text(social_svg, encoding="utf-8")

        print(f"Generated assets for {p.name} in {p.target_dir}")


if __name__ == "__main__":
    generate_all_banners()
