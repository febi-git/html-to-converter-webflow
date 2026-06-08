# Mode C: Build a complete multi-page project from scratch

The user wants a full multi-page Webflow site, authored locally and pushed via the converter. This is the largest scope and benefits most from project structure decisions made up front.

## First decision: which CSS naming framework?

Ask this **before scaffolding anything**, using AskUserQuestion. For a new project the headline options are **Lumos** and **Finsweet Client-First** (the real Webflow frameworks designers/clients edit in the Designer), with **BEM** as the lightweight self-contained option, plus a free-text escape hatch:

> Which CSS framework should this project use?
> **1) Lumos (v2)** — variable + container-query driven, breakpointless. Best designer-developer ergonomics. *Requires cloning the Lumos v2 Webflow project first.*
> **2) Finsweet Client-First (v2.1)** — descriptive utilities, cleanest handoff to non-technical clients, most consistent across projects. *Requires cloning the Client-First cloneable first.*
> **3) BEM (single-underscore)** — fully self-contained, zero setup, imports into any Webflow site. Best for small sites or when there's no framework.
> **Other** — name any framework; the skill follows its docs using the same cloneable-referencing pattern.

Skim [reference/frameworks-comparison.md](../reference/frameworks-comparison.md) to walk the user through the trade-offs if they're unsure. Rule of thumb: designer/client-edited real site → **Lumos** or **Client-First**; one-off or framework-less import → **BEM**.

**Capture the decision before continuing**, then load the matching authoring reference and templates:

| Choice | Authoring rules | Templates | Build flag |
| ------ | --------------- | --------- | ---------- |
| Lumos | [reference/frameworks/lumos.md](../reference/frameworks/lumos.md) | `templates/lumos/` | `FRAMEWORK = "lumos"` |
| Client-First | [reference/frameworks/client-first.md](../reference/frameworks/client-first.md) | `templates/client-first/` | `FRAMEWORK = "client-first"` |
| BEM | [reference/css-rules.md](../reference/css-rules.md) (7 rules) | `templates/` (root) | `FRAMEWORK = "bem"` |
| Other | the framework's own docs | adapt `templates/lumos/` as a starting point | non-`bem` value |

> **Setup step for Lumos / Client-First (do this before any import):** both are *cloneable-referencing* — their utilities and variables live in a Global Styles embed shipped with the framework's official Webflow project. The user must **clone that project first** so the embed is present on every page; the generated output only references those globals. See the "Setup first" section of the framework reference and `templates/<framework>/SETUP.md`. BEM needs none of this (self-contained).

The rest of this mode is written for BEM. Where it bundles `tokens.css` / `base.css` / `components.css` and inlines tokens, **Lumos and Client-First skip that** — they emit component/custom-class CSS only and keep `var()` refs (the build's `FRAMEWORK` flag handles it). Use the framework reference for authoring; the scaffold structure below is otherwise the same.

## Project structure

Scaffold this layout:

```
project-root/
├── pages/
│   ├── _shared/
│   │   ├── tokens.css         # design tokens — single source of truth
│   │   ├── base.css           # reset + typography + .container + .section
│   │   ├── components.css     # buttons + cross-page reused components
│   │   └── CONVENTIONS.md     # the 7 rules, project-local copy
│   ├── _build/
│   │   └── _build.py          # shared build script (one per project)
│   ├── home/
│   │   ├── index.html
│   │   ├── home.css
│   │   ├── home.js
│   │   └── _converter/
│   │       └── _build.py      # symlink or copy of pages/_build/_build.py
│   ├── about/
│   │   ├── index.html
│   │   ├── about.css
│   │   └── _converter/
│   │       └── _build.py
│   └── ... (one folder per page)
├── Webflow code/                 # (optional) export of live site for reference
└── CLAUDE.md                     # project rules — copy CLAUDE.md template at the bottom
```

Each page folder has its own `_converter/_build.py` so pages build independently. The script knows which page it's for via `PAGE_SLUG`.

## Step-by-step scaffold

### 1. Bootstrap shared files

**BEM:** copy from templates:
- `pages/_shared/tokens.css` ← [templates/tokens.css](../templates/tokens.css)
- `pages/_shared/base.css` ← [templates/base.css](../templates/base.css)
- `pages/_shared/components.css` ← [templates/components.css](../templates/components.css)

Open `tokens.css` and fill in the project's actual brand colors, type scale, spacing, etc. Don't add tokens speculatively — start with what the design needs and grow it as new sections demand new values. Discuss any new token addition with the user before adding.

**Lumos / Client-First:** there is **no `_shared` design system to bootstrap** — tokens, base, and utilities come from the cloned framework project's Global Styles embed. Instead:
- Confirm the user has cloned the framework's official Webflow project (see `templates/<framework>/SETUP.md`). If not, do that first.
- Each page ships **component/custom-class CSS only**. The per-page `_build.py` uses `FRAMEWORK = "lumos"` or `"client-first"`, which keeps `var()` refs and skips token bundling.
- Use `templates/<framework>/page-template.html` and `templates/<framework>/page.js` as the page starting point.

### 2. Add a project CLAUDE.md

Capture project rules in a `CLAUDE.md` at the project root so this skill behaves consistently across sessions. Template:

```markdown
# <Project Name> — Webflow Workflow

This project authors pages locally in vanilla HTML/CSS/JS, then ships to Webflow via the Modern HTML to Webflow Converter (https://moden.club/tools/html-to-webflow). Workflow is managed by the `/html-to-webflow:convert` skill.

## Framework
- **CSS framework:** <BEM | Lumos v2 | Client-First v2.1 | other>
- **Authoring rules:** <reference/css-rules.md (BEM) | reference/frameworks/lumos.md | reference/frameworks/client-first.md>
- **Build flag:** FRAMEWORK = "<bem | lumos | client-first>" in every page's `_build.py`
- **Cloneable (Lumos / Client-First only):** the framework's official Webflow project is cloned and its Global Styles embed is on every page. <link / note>

## Hard rules
- Build pages section by section. Never write a full page in one go.
- CSS follows the framework's authoring rules (above).
- Source code uses unprefixed class names; build script adds prefixes. (Never prefix framework utilities.)
- Don't hand-edit `_converter/<slug>.webflow.{html,css,js}` files — they're generated.
- BEM: all design values go through `tokens.css` (inlined at build). Lumos / Client-First: use framework variables/utilities; keep `var()` refs (do NOT inline).

## Where things live
- `pages/_shared/` — BEM design system (tokens, base, components). Lumos / Client-First: not used — globals come from the cloned project.
- `pages/<slug>/` — per-page source
- `pages/<slug>/_converter/` — generated bundle + per-page build script

## Class collision baseline
- Live site export: `Webflow code/<site-name>.webflow/` (read-only reference)
- Add new colliding **custom** class names to `COLLIDE_RENAMES` in each page's `_build.py` (never framework utilities)
```

### 3. Set up the first page (home)

Use sub-flow B2 (`existing-site.md` → "Add a new page"), but starting from blank. The flow is:

1. Copy the framework's page template → `pages/home/index.html` — `templates/page-template.html` (BEM), `templates/lumos/page-template.html`, or `templates/client-first/page-template.html`.
2. Create `pages/home/home.css` (empty).
3. Create `pages/home/home.js` if needed (use the framework's `page.js`).
4. Copy [templates/_build.py](../templates/_build.py) → `pages/home/_converter/_build.py`. Set `PAGE_SLUG = "home"` and `FRAMEWORK` to match the project's choice (`"bem"` / `"lumos"` / `"client-first"`).
5. **Gather the design intent before authoring.** Per the global [SKILL.md](../SKILL.md) step, have the user explain the project — what it is, the audience, the feel — and share references: screenshots/mockups, a Figma file, a site to emulate, or an existing codebase whose style to match. For a multi-page project this is also where you establish the design language the *whole* site inherits, so it's worth doing thoroughly. Read any reference code/URLs before writing.
6. Author the home page section by section. Hero first, show the user, iterate.

### 4. Reusing components across pages

When you build a component on page A and page B needs it:

1. Tell the user "X is being reused — moving it from `pages/A/A.css` to `pages/_shared/components.css`."
2. Move the rules verbatim. Don't refactor.
3. Remove the original from page A's CSS.
4. Both pages now reference it via `components.css`.

This rule keeps `components.css` lean and avoids premature abstraction. A component lives in its page until a second page demands it.

### 5. Build & import each page

Same as B2. For each page:

```bash
python pages/<slug>/_converter/_build.py
```

Then paste the three `.webflow.*` files into https://moden.club/tools/html-to-webflow and import to the corresponding Webflow page.

For multi-page projects, walk through [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md) once for the first page, then reuse the muscle memory.

## Token / collision management at scale

For a 20-page project, `COLLIDE_RENAMES` and `VAR_TO_LITERAL` need to stay in sync across all the per-page `_build.py` files. Two approaches:

- **Centralised:** put `COLLIDE_RENAMES` and `VAR_TO_LITERAL` in `pages/_shared/_build_config.py` and `import` it from each page's `_build.py`.
- **Symlinked:** maintain one `_build.py` in `pages/_build/` and symlink it to each page's `_converter/`.

Either is fine. Centralised is cleaner for projects > 5 pages.

## Webflow project setup (one-time, before any page imports)

Before importing the first page:

1. **Project Settings → Custom Code → Footer Code** → add GSAP + ScrollTrigger CDN tags. See [reference/webflow-runtime.md](../reference/webflow-runtime.md). Publish.
2. **Set up Webflow Pages.** Create empty pages for every URL the project will have, with correct slugs and SEO metadata. Imports go into these.
3. **Set up CMS Collections** if the project uses them — this skill doesn't cover CMS-driven pages. Webflow's CMS UI is the right place to set those up; the converter is for static page templates.

## Lumos / Client-First — specifics when the user picks one

Both are first-class — use their reference + templates + build flag (table at the top of this file). Key differences from the BEM flow:

1. **Authoring rules come from the framework reference**, not the BEM 7 rules: [reference/frameworks/lumos.md](../reference/frameworks/lumos.md) or [reference/frameworks/client-first.md](../reference/frameworks/client-first.md). Read it end-to-end before authoring.
2. **Clone the framework's Webflow project first** (see `templates/<framework>/SETUP.md`). The Global Styles embed must be on every page that receives an import, or sections render unstyled.
3. **Output is cloneable-referencing.** Component/custom-class CSS only; utilities (`u-*`, `heading-style-*`, …) and variables come from the embed. `var()` refs are kept (the `FRAMEWORK` flag stops the build inlining them). Rule #6 (avoid utilities) does **not** apply — these frameworks are utility-driven.
4. **Never prefix utilities in `COLLIDE_RENAMES`.** Lumos's `u-section` and Client-First's `padding-global` are intentionally global; prefixing them defeats the framework. `COLLIDE_RENAMES` stays short (usually empty) — only a genuinely-colliding custom component class belongs there.
5. **Class-manager bloat is expected.** The cloned project already carries the framework's utilities, so imports add only your component classes — but the panel still shows the framework's full utility set. That's by design (cross-page consistency).

## When the project is ready to ship

- All pages built, imported, smoke-tested.
- All assets re-linked in Webflow Asset Manager.
- GSAP CDN in Footer Code, verified working on at least one page that uses GSAP.
- Sitemap, robots.txt, redirects (if any) set up in Webflow's project settings.
- Staging publish smoke-tested across desktop / tablet / mobile.
- User explicitly approves production publish.
- Use the `safe-publish` skill if available for the final go-live.
