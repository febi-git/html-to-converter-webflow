# Lumos v2 — project setup

Read [reference/frameworks/lumos.md](../../reference/frameworks/lumos.md) first. The short version:

## 1. Clone the framework (required, before any import)

Lumos v2 is **cloneable-referencing** — the `u-*` utilities and `--_…` variables
live in the official Lumos v2 Webflow project's **Global Styles embed**, not in
the generated output.

- Clone the official Lumos v2 Webflow project (`lumos.timothyricks.com` /
  `github.com/lumosframework`).
- Confirm the **Global Styles embed is present on every page** that will receive
  imported markup.

Without this, imported sections render unstyled in Designer (utilities and
variables won't exist).

## 2. Local preview

Generated CSS contains **component-class rules only** — it references `u-*`
utilities and `var(--_…)` it does not define. For local browser preview, export
your cloned project's CSS and link it in the page `<head>`
(`<link rel="stylesheet" href="lumos-global.css">`). This local file is NOT
shipped to Webflow. Local preview is approximate; the real check is in the
Designer canvas after import, where the cloned project's globals apply.

## 3. Build

Copy [templates/_build.py](../_build.py) into the page's `_converter/` folder and set:

```python
FRAMEWORK = "lumos"     # cloneable-referencing: keep var() refs, no token inlining
PAGE_SLUG = "home"      # the page folder name
COLLIDE_RENAMES = []    # usually empty — NEVER add u-* utilities or framework vars
```

Then `python pages/<slug>/_converter/_build.py` and paste the three
`.webflow.*` files into https://moden.club/tools/html-to-webflow.

## 4. Authoring rules

- Component class first, then utilities: `class="hero_title u-text-style-h1"`.
- `_wrap` / `_contain` / `_layout` section triad; grid/flex on `_layout`, never `u-container`.
- `is-` combo classes must appear in the HTML; scope them to a component class in CSS.
- rem (text max-width in `ch`, container queries in `em`); no px, no `:root`, no utility redefs.

Full rules: [reference/frameworks/lumos.md](../../reference/frameworks/lumos.md).
