# Mode C: Build a complete multi-page project from scratch

The user wants a full multi-page Webflow site, authored locally and pushed via the converter. This is the largest scope and benefits most from project structure decisions made up front.

## First decision: which CSS naming framework?

The default for this skill is **single-underscore BEM** with state combo classes (`.tool-card`, `.tool-card_title`, `.tool-card.is_live`). It's what the converter handles cleanest and what the rest of this skill is tuned for.

For projects with **10+ pages**, frameworks like **Lumos** and **Finsweet Client First** offer scaling benefits — class deduplication, faster cross-page edits, easier onboarding for team members familiar with those systems. They have tradeoffs against the converter, though.

Read [reference/frameworks-comparison.md](../reference/frameworks-comparison.md) and walk the user through the choice before scaffolding. Decision rule of thumb:

| Project scope | Recommendation                                                                    |
| ------------- | --------------------------------------------------------------------------------- |
| ≤ 5 pages     | **BEM** (this skill's default). Lumos/Client First is overkill.                   |
| 6–10 pages    | BEM still works fine. Consider Lumos if the team already knows it.                |
| 10+ pages     | **Lumos or Client First** for class deduplication. Accept the converter tradeoffs (rule #6 conflict). |

Capture the decision before continuing. The rest of this mode assumes BEM; if Lumos or Client First, see the framework-specific notes at the bottom.

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

Copy from templates:
- `pages/_shared/tokens.css` ← [templates/tokens.css](../templates/tokens.css)
- `pages/_shared/base.css` ← [templates/base.css](../templates/base.css)
- `pages/_shared/components.css` ← [templates/components.css](../templates/components.css)

Open `tokens.css` and fill in the project's actual brand colors, type scale, spacing, etc. Don't add tokens speculatively — start with what the design needs and grow it as new sections demand new values. Discuss any new token addition with the user before adding.

### 2. Add a project CLAUDE.md

Capture project rules in a `CLAUDE.md` at the project root so this skill behaves consistently across sessions. Template:

```markdown
# <Project Name> — Webflow Workflow

This project authors pages locally in vanilla HTML/CSS/JS, then ships to Webflow via the Modern HTML to Webflow Converter (https://moden.club/tools/html-to-webflow). Workflow is managed by the html-to-converter-webflow skill.

## Hard rules
- Build pages section by section. Never write a full page in one go.
- CSS follows the 7 rules in `pages/_shared/CONVENTIONS.md`.
- Source code uses unprefixed class names; build script adds prefixes.
- Don't hand-edit `_converter/<slug>.webflow.{html,css,js}` files — they're generated.
- All design values go through `tokens.css`. No literals in component CSS.

## Where things live
- `pages/_shared/` — design system (tokens, base, components, conventions)
- `pages/<slug>/` — per-page source
- `pages/<slug>/_converter/` — generated bundle + per-page build script

## Class collision baseline
- Live site export: `Webflow code/<site-name>.webflow/` (read-only reference)
- Add new colliding class names to `COLLIDE_RENAMES` in each page's `_build.py`
```

### 3. Set up the first page (home)

Use sub-flow B2 (`existing-site.md` → "Add a new page"), but starting from blank. The flow is:

1. Copy [templates/page-template.html](../templates/page-template.html) → `pages/home/index.html`.
2. Create `pages/home/home.css` (empty).
3. Create `pages/home/home.js` if needed (use [templates/page.js](../templates/page.js)).
4. Copy [templates/_build.py](../templates/_build.py) → `pages/home/_converter/_build.py`. Set `PAGE_SLUG = "home"`.
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

## Lumos / Client First — if the user picks one of these

If the user opts for Lumos or Finsweet Client First instead of BEM:

1. **Read [reference/frameworks-comparison.md](../reference/frameworks-comparison.md) end-to-end** — the constraints differ from BEM in ways that affect the build script.
2. **Disable converter rule #6** (avoid utilities). Lumos / Client First are utility-heavy by design.
3. **Skip class prefixing for utility classes.** Lumos's `padding-section-large` and Client First's `padding-global` are intentionally global; prefixing them defeats the framework. But: if the live site already has a `padding-global` class with different rules, you have a structural collision that no prefix can fix. Check before importing.
4. **Class manager bloat is the cost.** Document for the user that they'll see hundreds of classes in Webflow's class panel. That's by design — Lumos and Client First trade visual clutter in the panel for cross-page consistency.
5. **The build script's `COLLIDE_RENAMES` becomes less useful** because Lumos / Client First class names rarely collide accidentally (they're explicit and namespaced). Keep the mechanism but expect short lists.

The skill's templates assume BEM. If the user picks Lumos or Client First, fork the templates locally — don't try to make a single template support all three.

## When the project is ready to ship

- All pages built, imported, smoke-tested.
- All assets re-linked in Webflow Asset Manager.
- GSAP CDN in Footer Code, verified working on at least one page that uses GSAP.
- Sitemap, robots.txt, redirects (if any) set up in Webflow's project settings.
- Staging publish smoke-tested across desktop / tablet / mobile.
- User explicitly approves production publish.
- Use the `safe-publish` skill if available for the final go-live.
