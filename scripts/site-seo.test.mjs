import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { test } from "node:test";

const ORIGIN = "https://standards.naindev.com/";
const html = readFileSync(new URL("../site/index.html", import.meta.url), "utf8");
const sitemap = readFileSync(new URL("../site/sitemap.xml", import.meta.url), "utf8");
const robots = readFileSync(new URL("../site/robots.txt", import.meta.url), "utf8");

// SPEC-1: the project page declares one canonical URL and is discoverable
// by search engines through a sitemap.

test("declares the canonical URL of the page (REQ-IDX-001)", () => {
  assert.ok(html.includes(`<link rel="canonical" href="${ORIGIN}">`));
});

test("declares Open Graph and Twitter card metadata (REQ-IDX-002)", () => {
  for (const property of ["og:type", "og:title", "og:description", "og:url", "og:image"]) {
    assert.match(html, new RegExp(`<meta property="${property}" content="[^"]+">`), property);
  }
  assert.ok(html.includes(`<meta property="og:url" content="${ORIGIN}">`));
  assert.match(html, /<meta name="twitter:card" content="summary_large_image">/);
});

test("embeds valid JSON-LD that describes the project (REQ-IDX-003)", () => {
  const match = html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  assert.ok(match, "JSON-LD block missing");
  const data = JSON.parse(match[1]);
  assert.equal(data["@type"], "SoftwareSourceCode");
  assert.equal(data.url, ORIGIN);
  assert.equal(data.codeRepository, "https://github.com/Nain9Dev/.github");
});

test("does not block indexing (REQ-IDX-004)", () => {
  assert.doesNotMatch(html, /<meta name="robots" content="[^"]*noindex/i);
});

test("sitemap lists the page URL and nothing else (REQ-IDX-005)", () => {
  const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
  assert.deepEqual(locs, [ORIGIN]);
});

test("robots.txt allows crawling and points to the sitemap (REQ-IDX-006)", () => {
  assert.match(robots, /^Allow: \/$/m);
  assert.ok(robots.includes(`Sitemap: ${ORIGIN}sitemap.xml`));
});
