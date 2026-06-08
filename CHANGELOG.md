# Changelog

All notable changes to the `html-to-webflow` plugin are documented here.

## 0.3.0 — 2026-06-08

First-class multi-framework support. For a **new project** (a new multi-page
site in Mode C, or a new-project component in Mode A) the skill now asks which
CSS framework to use — **Lumos v2** and **Finsweet Client-First v2.1** as the
headline options, with **BEM** as the self-contained default and a free-text
escape hatch for any other framework. Lumos and Client-First were studied
against their official specs and incorporated so the generated output imports
cleanly into Webflow Designer.

### Added

- **Framework authoring references.** `reference/frameworks/lumos.md` (Lumos
  **v2** — `_wrap`/`_contain`/`_layout` triad, `component_type_element` naming,
  `u-*` utilities, the variable system, Designer-import requirements, mirroring
  Timothy Ricks' official generation spec) and
  `reference/frameworks/client-first.md` (Client-First **v2.1** — class types,
  `page-wrapper`/`main-wrapper`/`section_*`/`padding-global`/`container-*`
  structure, the full utility vocabulary, spacing/typography scales).
- **Framework templates.** `templates/lumos/` and `templates/client-first/`,
  each with a `page-template.html` (correct framework structure), `page.js`, and
  a `SETUP.md` covering the clone-the-cloneable step and local-preview caveat.

### Changed

- **`templates/_build.py` is framework-aware** via a new `FRAMEWORK` flag
  (`"bem"` | `"lumos"` | `"client-first"`). BEM is unchanged (self-contained:
  drop `:root`, inline every `var()` to a literal). Lumos/Client-First are
  **cloneable-referencing**: component/custom-class CSS only, `var()` refs kept
  intact (no token bundling, no inlining), and the "zero `var()` may remain"
  sanity check is relaxed to a report.
- **Mode C** (`multi-page-project.md`) and **Mode A** (`component-or-section.md`)
  now ask the framework question for new projects, branch the scaffold to the
  right templates/build flag, and record the choice in the project `CLAUDE.md`.
- **`frameworks-comparison.md`** rewritten: all three frameworks are first-class
  (was "BEM only — fork the templates yourself"), with a self-contained vs
  cloneable-referencing explanation and a Lumos v2-vs-v1 note.
- **`SKILL.md`** and **`css-rules.md`** marked framework-aware: the BEM 7 rules
  are the default; Lumos/Client-First follow their own reference, and the
  inline-tokens hard rule is scoped to BEM.

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
