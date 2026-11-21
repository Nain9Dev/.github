# SPEC-001 — Project page indexing

Status: Proposed
Owner: naindev
Scope: `site/`, `scripts/`, CI workflow

## Problem

`https://standards.naindev.com/` is a public page, but it declares no canonical URL and publishes no
sitemap. Google Search Console cannot be given a sitemap for it, and the page
lacks the Open Graph and structured data that the other NainDev project pages
carry.

## Requirements

Notation: EARS.

- **REQ-IDX-001** — The page shall declare `https://standards.naindev.com/` as its canonical URL.
- **REQ-IDX-002** — The page shall declare Open Graph and Twitter card metadata
  (`og:type`, `og:title`, `og:description`, `og:url`, `og:image`, `twitter:card`).
- **REQ-IDX-003** — The page shall embed JSON-LD of type `SoftwareSourceCode`
  that points to the page URL and to the GitHub repository.
- **REQ-IDX-004** — The page shall not carry a `noindex` directive.
- **REQ-IDX-005** — The site shall publish `/sitemap.xml` listing only the page URL.
- **REQ-IDX-006** — The site shall publish `/robots.txt` that allows crawling and
  names the sitemap.
- **REQ-IDX-007** — The site shall publish `/llms.txt`, a short plain-text summary
  of the project for AI answer engines, derived from the page description.

## Out of scope

- Content, layout and copy of the page.
- Submitting the sitemap to Search Console and Bing Webmaster (owner step, after the deploy).
