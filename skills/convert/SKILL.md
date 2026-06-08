---
name: convert
version: 0.3.0
description: Ship hand-coded or vibe-coded HTML/CSS/JS into Webflow via the moden.club converter. Encodes 48+ tested fixes for class collisions, Designer canvas glitches, GSAP/ScrollTrigger integration, asset re-linking, and re-import cleanup. For new projects, asks which CSS framework to use — Lumos v2, Finsweet Client-First v2.1, or self-contained BEM. Use when the user mentions "html to webflow", "moden.club", "webflow converter", "import to Webflow", "Webflow paste tool", or invokes `/html-to-webflow:convert` directly. Supports three modes: single component/section, edit existing Webflow site, or new multi-page project.
---

# HTML → Webflow Converter Workflow

Help the user ship hand-coded or vibe-coded HTML/CSS/JS into Webflow via the **Modern HTML to Webflow Converter** at https://moden.club/tools/html-to-webflow. This skill encodes every fix and convention that this workflow needs to be smooth — class collision handling, Designer canvas workarounds, GSAP/Webflow runtime integration, asset re-linking, and re-import cleanup.

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

## Gather the design intent

Once the mode is picked, **before scaffolding or authoring anything**, give the user room to tell you what they actually want. Don't jump straight to writing code from a one-line request — the output is only as good as the brief.

Ask the user (open-ended; use AskUserQuestion or a plain prompt):

> Tell me about what you're building. A couple of things help a lot:
> - **The idea, in your words** — what this is, who it's for, the feel you want, anything you specifically like or want to avoid.
> - **References** — paste or link any of: a screenshot/mockup, a Figma file, a live URL to emulate, or existing code/components whose style you want matched.

This is optional but strongly encouraged. If the user shares reference code or a URL, read/inspect it before authoring. If they have nothing to share, say so explicitly and proceed with sensible, on-brief defaults — don't silently assume a direction. The mode files reinforce this in their first step; this is the single place it's asked up front for every mode.

## Reference docs (load on demand)

The mode files reference these. Don't read them up front — only load when the mode flow asks you to:

- [reference/css-rules.md](reference/css-rules.md) — BEM authoring rules (the default; REM, single-underscore BEM, class-only, no descendants, simple selectors, named blocks, basic pseudos only). Lumos/Client-First follow their own framework reference instead.
- [reference/frameworks-comparison.md](reference/frameworks-comparison.md) — the framework chooser (Lumos vs Client-First vs BEM); relevant whenever starting a new project (mode c, or a new-project component in mode a)
- [reference/frameworks/lumos.md](reference/frameworks/lumos.md) — Lumos **v2** authoring rules (naming, `_wrap`/`_contain`/`_layout` triad, `u-*` utilities, variables, Designer-import requirements, clone-first setup)
- [reference/frameworks/client-first.md](reference/frameworks/client-first.md) — Finsweet Client-First **v2.1** authoring rules (class types, page structure, utility vocabulary, clone-first setup)
- [reference/designer-canvas-fixes.md](reference/designer-canvas-fixes.md) — `inDesigner` guard, fit-content for flex children, custom scroll listener vs ScrollTrigger.scrub
- [reference/webflow-runtime.md](reference/webflow-runtime.md) — `Webflow.push()`, GSAP CDN footer setup, `body { overflow-x: hidden }` mobile safety
- [reference/class-collisions.md](reference/class-collisions.md) — detection, `COLLIDE_RENAMES` protocol, `acme-` (or your own) prefix
- [reference/variable-mapping.md](reference/variable-mapping.md) — `VAR_TO_LITERAL` inlining strategy + sanity check (BEM only — Lumos/Client-First keep `var()` refs)
- [reference/asset-handling.md](reference/asset-handling.md) — `placehold.co` placeholders → re-link in Webflow Asset Manager
- [reference/webflow-designer-checklist.md](reference/webflow-designer-checklist.md) — the Webflow-side steps (delete page → import → re-link assets → publish), including MCP tool integration where available

## Templates (copy and parameterize)

When a mode flow says "scaffold the project / page / component", copy from:

- [templates/_build.py](templates/_build.py) — the parameterized build script (config block at top). One script, all frameworks: set `FRAMEWORK = "bem" | "lumos" | "client-first"`.
- [templates/page-template.html](templates/page-template.html) — **BEM** page scaffold
- [templates/tokens.css](templates/tokens.css) — empty design tokens template (BEM)
- [templates/base.css](templates/base.css) — reset + typography + layout primitives (BEM)
- [templates/components.css](templates/components.css) — button placeholder (BEM)
- [templates/page.css](templates/page.css) — empty page CSS
- [templates/page.js](templates/page.js) — IIFE + `inDesigner` guard skeleton
- [templates/inDesigner-canvas-snippet.js](templates/inDesigner-canvas-snippet.js) — canonical canvas guard pattern, ready to paste
- **Framework variants** (Lumos / Client-First — cloneable-referencing, no tokens/base/components):
  - `templates/lumos/` — `page-template.html`, `page.js`, `SETUP.md`
  - `templates/client-first/` — `page-template.html`, `page.js`, `SETUP.md`

## Hard rules across every mode

These apply no matter which mode the user picked. Don't violate them.

1. **Build section by section.** Never write a full page in one go. Finish a section, show the user, get approval, then move on. A polished hero is more valuable than a draft of the whole page.
2. **CSS authoring follows the project's framework rules.** **BEM** (default) → the 7 rules in [reference/css-rules.md](reference/css-rules.md). **Lumos** → [reference/frameworks/lumos.md](reference/frameworks/lumos.md). **Client-First** → [reference/frameworks/client-first.md](reference/frameworks/client-first.md). The converter parses CSS into Webflow classes; anything that doesn't map to a single class on a single element gets dropped or mangled — that constraint holds for every framework.
3. **Source code stays unprefixed; the build script adds prefixes.** Authors write `class="hero"` locally; the build emits `class="acme-hero"` (or whatever prefix you configure). This keeps source readable and lets local browser preview match what Webflow renders. (Framework utilities like `u-section` / `padding-global` are never prefixed.)
4. **Never hand-edit the generated `.webflow.{html,css,js}` files.** They're overwritten on every build. Edit source only.
5. **Design values: BEM inlines tokens; Lumos/Client-First keep `var()` refs.** For **BEM**, `var(--color-orange)` in source is inlined to `#ff4f41` at build time — if a value isn't in `tokens.css`, propose adding it before using a literal. For **Lumos/Client-First**, the framework's variables/utilities are the design system; the build keeps `var()` refs intact (they resolve against the cloned project) and ships no tokens of its own.
6. **Test locally by opening the HTML in a browser.** No dev server. No build tooling beyond `_build.py`.
7. **Vanilla only.** No React/Vue/Tailwind/Bootstrap. If animation is needed, prefer GSAP (Webflow's official integration choice).
8. **Page JS must run via `Webflow.push()`** in the export so it executes after Webflow's runtime initialises. Source stays as a plain IIFE — the build script wraps it.

## How to use this skill across a project

This skill is workflow-aware. After a mode picks up, follow its flow strictly. If you hit a question the mode file doesn't answer, load the relevant `reference/*.md` file. If a reference file doesn't answer it, ask the user — don't improvise around the conventions.
