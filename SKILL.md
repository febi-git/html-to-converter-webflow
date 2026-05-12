---
name: html-to-converter-webflow
version: 0.1.0
description: Ship hand-coded HTML/CSS/JS into Webflow via the moden.club converter. Encodes 48+ tested fixes for class collisions, Designer canvas glitches, GSAP/ScrollTrigger integration, asset re-linking, and re-import cleanup. Use when the user mentions "html to webflow", "moden.club", "webflow converter", "import to Webflow", "Webflow paste tool", or invokes `/html-to-converter-webflow` directly. Supports three modes: single component/section, edit existing Webflow site, or new multi-page project.
---

# HTML → Webflow Converter Workflow

You are helping the user ship hand-coded HTML/CSS/JS into Webflow via the **Modern HTML to Webflow Converter** at https://moden.club/tools/html-to-webflow. This skill encodes every fix and convention that this workflow needs to be smooth — class collision handling, Designer canvas workarounds, GSAP/Webflow runtime integration, asset re-linking, and re-import cleanup.

## Before you do anything else: pick a mode

Ask the user this question, exactly once, at the start of the session:

> What are you doing today?
> **a)** Building a single component or section (smallest surface — quick wins, no full-page scaffold)
> **b)** Editing an existing Webflow site (working from a `.zip` export, adding a new page, or modifying an existing page)
> **c)** Starting a new multi-page project from scratch

Use AskUserQuestion to ask. Then load the matching mode file and follow it:

| Answer | Load this file                                                              |
| ------ | --------------------------------------------------------------------------- |
| a)     | [modes/component-or-section.md](modes/component-or-section.md)              |
| b)     | [modes/existing-site.md](modes/existing-site.md)                            |
| c)     | [modes/multi-page-project.md](modes/multi-page-project.md)                  |

If the user is ambiguous ("I want to add something to my site" — does that mean a new page or modifying an existing one?), ask follow-up questions. Don't assume.

## Reference docs (load on demand)

The mode files reference these. Don't read them up front — only load when the mode flow asks you to:

- [reference/css-rules.md](reference/css-rules.md) — the 7 BEM authoring rules (REM, single-underscore BEM, class-only, no descendants, simple selectors, named blocks, basic pseudos only)
- [reference/designer-canvas-fixes.md](reference/designer-canvas-fixes.md) — `inDesigner` guard, fit-content for flex children, custom scroll listener vs ScrollTrigger.scrub
- [reference/webflow-runtime.md](reference/webflow-runtime.md) — `Webflow.push()`, GSAP CDN footer setup, `body { overflow-x: hidden }` mobile safety
- [reference/class-collisions.md](reference/class-collisions.md) — detection, `COLLIDE_RENAMES` protocol, `acme-` (or your own) prefix
- [reference/variable-mapping.md](reference/variable-mapping.md) — `VAR_TO_LITERAL` inlining strategy + sanity check
- [reference/asset-handling.md](reference/asset-handling.md) — `placehold.co` placeholders → re-link in Webflow Asset Manager
- [reference/frameworks-comparison.md](reference/frameworks-comparison.md) — BEM (default) vs Lumos vs Finsweet Client First (only relevant for mode c)
- [reference/webflow-designer-checklist.md](reference/webflow-designer-checklist.md) — the Webflow-side steps (delete page → import → re-link assets → publish), including MCP tool integration where available

## Templates (copy and parameterize)

When a mode flow says "scaffold the project / page / component", copy from:

- [templates/_build.py](templates/_build.py) — the parameterized build script (config block at top)
- [templates/page-template.html](templates/page-template.html) — page scaffold
- [templates/tokens.css](templates/tokens.css) — empty design tokens template
- [templates/base.css](templates/base.css) — reset + typography + layout primitives
- [templates/components.css](templates/components.css) — button placeholder
- [templates/page.css](templates/page.css) — empty page CSS
- [templates/page.js](templates/page.js) — IIFE + `inDesigner` guard skeleton
- [templates/inDesigner-canvas-snippet.js](templates/inDesigner-canvas-snippet.js) — canonical canvas guard pattern, ready to paste

## Hard rules across every mode

These apply no matter which mode the user picked. Don't violate them.

1. **Build section by section.** Never write a full page in one go. Finish a section, show the user, get approval, then move on. A polished hero is more valuable than a draft of the whole page.
2. **CSS authoring follows the 7 rules** in [reference/css-rules.md](reference/css-rules.md). The converter parses CSS into Webflow classes; anything that doesn't map to a single class on a single element gets dropped or mangled.
3. **Source code stays unprefixed; the build script adds prefixes.** Authors write `class="hero"` locally; the build emits `class="acme-hero"` (or whatever prefix you configure). This keeps source readable and lets local browser preview match what Webflow renders.
4. **Never hand-edit the generated `.webflow.{html,css,js}` files.** They're overwritten on every build. Edit source only.
5. **All design values go through tokens.** `var(--color-orange)` in source, inlined to `#ff4f41` at build time. If a value isn't in `tokens.css`, propose adding it before using a literal.
6. **Test locally by opening the HTML in a browser.** No dev server. No build tooling beyond `_build.py`.
7. **Vanilla only.** No React/Vue/Tailwind/Bootstrap. If animation is needed, prefer GSAP (Webflow's official integration choice).
8. **Page JS must run via `Webflow.push()`** in the export so it executes after Webflow's runtime initialises. Source stays as a plain IIFE — the build script wraps it.

## How to use this skill across a project

This skill is workflow-aware. After a mode picks up, follow its flow strictly. If you hit a question the mode file doesn't answer, load the relevant `reference/*.md` file. If a reference file doesn't answer it, ask the user — don't improvise around the conventions.
