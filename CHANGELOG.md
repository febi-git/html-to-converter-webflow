# Changelog

All notable changes to the `html-to-webflow` plugin are documented here.

## 0.2.0 — 2026-05-18

Naming release. No skill, build-script, or converter behavior changed — only
the plugin and skill identifiers, to fix the duplicated slash command.

### Changed

- **Plugin renamed `html-to-converter-webflow` → `html-to-webflow`** and the
  **skill renamed → `convert`** (directory `skills/html-to-converter-webflow/`
  → `skills/convert/`). The slash command is now `/html-to-webflow:convert`
  instead of the repeated `/html-to-converter-webflow:html-to-converter-webflow`.
  Reinstall with `/plugin install html-to-webflow@febinsha-webflow`. The
  GitHub repo slug (`febi-git/html-to-converter-webflow`) is unchanged, so
  `/plugin marketplace add` and clone URLs stay the same.

## 0.1.2 — 2026-05-18

Packaging release. No skill, build-script, or converter behavior changed —
the workflow content is identical to 0.1.1.

### Added

- **Installable Claude Code plugin.** Repo restructured into an all-in-one
  plugin + marketplace: `.claude-plugin/plugin.json` manifest and
  `.claude-plugin/marketplace.json` (marketplace `febinsha-webflow`). Skill
  files moved under `skills/html-to-converter-webflow/`. Install with
  `/plugin marketplace add febi-git/html-to-converter-webflow` then
  `/plugin install html-to-webflow@febinsha-webflow` (renamed in 0.2.0).

### Changed

- **README install/update flow** rewritten for the plugin marketplace, with
  clone-based instructions for Cursor, Codex, and Antigravity (replacing the
  prior Cline/Roo guidance).

## 0.1.1 — 2026-05-16

Documentation/UX corrections from real-project usage. No build-script or
converter behavior changed — the docs now match what the moden.club converter
actually does and prompt for context that was previously left implicit.

### Fixed

- **[#1] Converter output shape documented.** `webflow-designer-checklist.md`
  now has a *"What the converter actually outputs"* subsection explaining that
  CSS/JS land as inline `<style>`/`<script>` Webflow Embed nodes inside the
  component (not site-wide Custom Code), with relocation steps and the
  consequences of skipping them. `webflow-runtime.md` §2 gains a caveat noting
  `Webflow.push()` has reduced effect from an inline Embed. The Step 6
  smoke-test now states the canvas-visibility precondition.
- **[#1] Removed the non-existent "Direct import via Webflow API" flow.**
  Step 4 of the checklist and Step 6 of Mode A
  (`component-or-section.md`) now describe the only real flow: the
  `→ Convert to Webflow` button copies a Webflow-pasteable snippet to the
  clipboard; paste into the Designer canvas. No sign-in / project picker /
  API push.

### Added

- **[#2] Re-import class cleanup reminder.** Mode A Step 7 and the checklist's
  *Class manager check* now spell out that re-importing a single
  element/component (no page deletion) orphans old classes, and walk through
  deleting the old instance and its unused classes from the Class Manager
  before pasting the rebuilt version.
- **[#3] "Gather the design intent" step.** `SKILL.md` adds a global step,
  after mode selection, inviting the user to explain their idea and share
  references (screenshots, Figma, a live URL, existing code). Each mode file
  (`component-or-section.md`, `existing-site.md`, `multi-page-project.md`)
  reinforces this in its first authoring step.

## 0.1.0

- Initial release: HTML → Webflow converter workflow skill with three modes
  (single component, existing site, multi-page project), reference docs, and
  the parameterized `_build.py` template.
