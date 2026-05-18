# html-to-converter-webflow

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-D77757)](https://code.claude.com/docs/en/plugins)
[![Works with Webflow](https://img.shields.io/badge/Works%20with-Webflow-146EF5)](https://webflow.com)

A Claude Code skill (works in other AI coding agents too) that turns hand-coded or vibe-coded HTML/CSS/JS into clean, Webflow-importable bundles via the **Modern HTML to Webflow Converter** ([moden.club/tools/html-to-webflow](https://moden.club/tools/html-to-webflow)).

**Install in Claude Code (two commands):**

```
/plugin marketplace add febi-git/html-to-converter-webflow
/plugin install html-to-converter-webflow@febinsha-webflow
```

[Other agents (Cursor, Cline, …) →](#install)

It encodes ~48 fixes that came out of shipping a real production page through this workflow — the things you'd otherwise re-discover the hard way: class collisions with the live site, Designer canvas scroll lag, GSAP/ScrollTrigger timing issues, asset re-linking, and Webflow re-import cleanup.

## Who is this for

You're a **Webflow designer** who occasionally writes (or has AI write) HTML/CSS — and you want to drop it into your Webflow site without your live-site classes mysteriously turning orange, your Designer canvas lagging, or your animations refusing to fire. You don't need to be a developer; you just need an AI coding agent (Claude Code is the smoothest fit) and Python installed.

If you don't write code at all and only use Webflow's visual Designer, this skill isn't for you. If you write code *or* have AI write code that you then need to bring into Webflow, this is exactly what it's for.

## What it does

When you invoke the skill, it asks one question: **what are you doing?**

- **a) Building a single component or section** — quick scaffold, no full-page setup. Ship one card, one CTA strip, one hero, etc.
- **b) Editing an existing Webflow site** — point at a `.zip` export of your live site; the skill reads it, detects class collisions, and walks you through adding a new page, modifying an existing one, or extracting variables for reuse.
- **c) Starting a new multi-page project** — full scaffold with tokens / base / components / per-page CSS. Defaults to BEM single-underscore convention; documents Lumos and Finsweet Client First as alternatives for very large projects.

Each mode walks through authoring → building → importing into Webflow → re-linking assets → publishing.

## What you'll need

- An AI coding agent — **Claude Code** is the smoothest fit; Cursor, Cline, and Roo Code also work.
- **Python 3** on your machine (already installed on most macOS and Linux; on Windows install from [python.org](https://www.python.org/downloads/) if missing).
- A **Webflow site** you can publish to (any plan — Starter is fine for testing).
- About **15 minutes** for your first end-to-end run.

## Install

### Claude Code (recommended) — plugin marketplace

Two commands inside Claude Code. No cloning, no manual restart.

```
/plugin marketplace add febi-git/html-to-converter-webflow
/plugin install html-to-converter-webflow@febinsha-webflow
```

That's it. The skill is then available as `/html-to-converter-webflow:html-to-converter-webflow` and auto-triggers when you mention Webflow conversion topics. To scope it to one project instead of your user account, append `--scope project` to the install command.

> **Non-interactive (terminal) equivalent:**
> ```bash
> claude plugin marketplace add febi-git/html-to-converter-webflow
> claude plugin install html-to-converter-webflow@febinsha-webflow
> ```

### Cursor

```bash
git clone https://github.com/febi-git/html-to-converter-webflow ~/.cursor/rules/html-to-converter-webflow
```

Then add this line to your project's `.cursor/rules/index.mdc` (create the file if it doesn't exist):

> When the user mentions importing HTML to Webflow, the moden.club converter, or Webflow paste tool, follow the workflow in `html-to-converter-webflow/skills/html-to-converter-webflow/SKILL.md`.

### Cline / Roo Code

```bash
git clone https://github.com/febi-git/html-to-converter-webflow ./.clinerules/html-to-converter-webflow
```

Cline and Roo will pick up the rules folder automatically.

### Any other agent

Clone the repo anywhere on disk, then tell your agent:

> Read `skills/html-to-converter-webflow/SKILL.md` in [path/to/cloned/repo] and follow its workflow when I mention importing HTML to Webflow.

The skill is plain Markdown — any LLM-based agent can follow it.

## Updating

### Claude Code (plugin)

Plugins update through the marketplace — no `git pull`, no re-clone:

```
/plugin update html-to-converter-webflow@febinsha-webflow
```

Updates are delivered only when the plugin's `version` is bumped (it tracks the `version:` in `SKILL.md`). Changes are listed in [CHANGELOG.md](CHANGELOG.md).

### Cursor / Cline / other agents (clone-based)

Run `git pull` in whichever folder you cloned into (`.cursor/rules/...`, `.clinerules/...`):

```bash
git -C ~/.cursor/rules/html-to-converter-webflow pull
```

To check whether you're behind, compare the `version:` field at the top of your local [`SKILL.md`](https://github.com/febi-git/html-to-converter-webflow/blob/main/skills/html-to-converter-webflow/SKILL.md) against GitHub. If you locally edited your copy (custom prefix, `COLLIDE_RENAMES` baseline), `git pull` may report merge conflicts — resolve them or re-clone fresh.

## First run (5 steps)

1. **Install** using the commands for your agent (above). Claude Code plugin users are ready immediately — no restart.
2. **Open your agent** in any folder — a scratch folder works fine for the first run.
3. **Type** `/html-to-converter-webflow:html-to-converter-webflow` (Claude Code) or "use the html-to-converter-webflow workflow" (other agents).
4. **Answer "a"** for "Building a single component or section" — the smallest, fastest path to your first successful Webflow import.
5. **Follow the prompts.** The skill asks for your component idea, writes the HTML/CSS/JS, runs the build script, and walks you step-by-step through pasting into [moden.club](https://moden.club/tools/html-to-webflow) and importing into Webflow.

After your first successful component, try mode **b** (editing an existing site) or mode **c** (new multi-page project).

## Use

In Claude Code:

```
/html-to-converter-webflow:html-to-converter-webflow
```

Or just describe what you want — the skill auto-triggers on phrases like:

- "I want to import this page into Webflow"
- "Convert HTML to Webflow"
- "Use the moden.club converter"
- "Webflow paste tool"
- "Help me ship this code into Webflow"

## What the skill ships

```
html-to-converter-webflow/                  # plugin + marketplace repo
├── .claude-plugin/
│   ├── plugin.json                     # plugin manifest
│   └── marketplace.json                # marketplace: febinsha-webflow
├── README.md                           # you are here
├── LICENSE                             # MIT
├── CHANGELOG.md
└── skills/
    └── html-to-converter-webflow/
        ├── SKILL.md                    # entry — frontmatter + mode router
        ├── modes/
        │   ├── component-or-section.md       # mode (a)
        │   ├── existing-site.md              # mode (b)
        │   └── multi-page-project.md         # mode (c)
        ├── reference/
        │   ├── css-rules.md                  # 7 BEM rules with examples
        │   ├── designer-canvas-fixes.md      # inDesigner guard + workarounds
        │   ├── webflow-runtime.md            # Webflow.push, GSAP CDN, body overflow-x
        │   ├── class-collisions.md           # detection + COLLIDE_RENAMES protocol
        │   ├── variable-mapping.md           # VAR_TO_LITERAL inlining + sanity check
        │   ├── asset-handling.md             # placehold.co + Asset Manager re-link
        │   ├── frameworks-comparison.md      # BEM vs Lumos vs Client First tradeoffs
        │   └── webflow-designer-checklist.md # full Webflow-side steps + MCP integration
        └── templates/
            ├── _build.py                     # parameterized build script
            ├── page-template.html            # starter scaffold
            ├── tokens.css                    # empty design tokens
            ├── base.css                      # reset + typography + layout
            ├── components.css                # button placeholder
            ├── page.css                      # empty page CSS
            ├── page.js                       # IIFE + inDesigner guard
            └── inDesigner-canvas-snippet.js  # canonical canvas guard, copy-pasteable
```

## What problems it solves

| Problem encountered | Fix encoded |
| ------------------- | ----------- |
| Class names from your import collide with the live Webflow site and silently merge | Build script prefixes colliding names with `acme-` (configurable). `COLLIDE_RENAMES` list maintained in `_build.py`. |
| Webflow Designer canvas lags / scroll feels broken when you have ScrollTrigger animations | `inDesigner` guard pattern: detect Designer mode and short-circuit scroll-driven animations to a static frame. |
| Inline-flex pill badges stretch full-width in Designer | `width: fit-content` workaround for flex children in Designer. |
| ScrollTrigger entrance animations fire from a stale layout on cold load (first-load mismatch) | Custom rAF-throttled scroll listener instead of `scrub`; refresh on image / font load. |
| Page CSS variables disappear or behave unpredictably after import | Inline every `var(--...)` as a literal hex/value at build time. Sanity check fails the build if any leak through. |
| Asset paths (`<img src=...>`) are useless after import | Use `placehold.co` placeholders in source; re-link to Webflow Asset Manager assets after import. Skill walks through it. |
| Re-importing a page leaves orphan classes from the previous attempt | Skill walks through "delete the page in Webflow first" before re-importing. |
| Page JS runs before Webflow's runtime is ready | Build script wraps source IIFE in `Webflow.push()`. Source stays as plain IIFE so local preview works. |
| `body` shows a thin horizontal gap on Webflow's mobile breakpoints | `body { overflow-x: hidden }` in `base.css` template. |

## Conventions

The skill ships with one opinionated default: **single-underscore BEM** with state modifiers as combo classes. Example:

```css
.tool-card { ... }
.tool-card_title { ... }
.tool-card.is_live { ... }
```

This convention plays cleanest with the converter. Mode (c) (`multi-page-project`) discusses **Lumos** and **Finsweet Client First** as alternatives, with a tradeoff table — but the skill doesn't natively support them out of the box.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

If you've found a Webflow converter quirk that isn't in the reference docs, PRs welcome — please include:

1. The exact symptom (screenshot if it's visual).
2. The minimum source code that reproduces it.
3. Whether it shows up in Designer canvas, the published site, or both.
4. The fix, with comments explaining *why*.
