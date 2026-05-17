# Changelog

All notable changes to the `html-to-converter-webflow` skill are documented here.

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
