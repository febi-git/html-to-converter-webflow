# Finsweet Client-First v2.1 — project setup

Read [reference/frameworks/client-first.md](../../reference/frameworks/client-first.md) first. The short version:

## 1. Clone the framework (required, before any import)

Client-First is **cloneable-referencing** — the utility classes
(`heading-style-*`, `padding-section-*`, `container-*`, `text-size-*`, …) and
project variables live in the official Client-First cloneable's **global-styles
embed**, not in the generated output.

- Clone the official Client-First cloneable from `finsweet.com/client-first`.
- Confirm the **`global-styles` embed is present on every page** that will
  receive imported markup.

Without this, imported sections render unstyled in Designer (the utility classes
won't exist).

## 2. Local preview

Generated CSS contains **custom-class rules only** — it references Client-First
utilities and `var(--…)` it does not define. For local browser preview, export
your cloned project's CSS and link it in the page `<head>`
(`<link rel="stylesheet" href="client-first-global.css">`). This local file is
NOT shipped to Webflow. Local preview is approximate; the real check is in the
Designer canvas after import.

## 3. Build

Copy [templates/_build.py](../_build.py) into the page's `_converter/` folder and set:

```python
FRAMEWORK = "client-first"   # cloneable-referencing: keep var() refs, no token inlining
PAGE_SLUG = "home"           # the page folder name
COLLIDE_RENAMES = []         # usually empty — NEVER add Client-First utilities
```

Then `python pages/<slug>/_converter/_build.py` and paste the three
`.webflow.*` files into https://moden.club/tools/html-to-webflow.

## 4. Authoring rules

- Structure: `page-wrapper` → `main-wrapper` → `section_[id]` → `padding-global`
  (+ `padding-section-[size]`) → `container-[size]` → content.
- Apply utilities (`heading-style-h1`, `text-size-large`, `padding-section-large`);
  never redefine them. Use custom classes (`hero_eyebrow`) for unique styling.
- **Minimal stacking** — prefer one custom class / a combo (`is-…`) / a nested
  div over deep utility stacks.
- rem throughout (16px root); `value/16 rem` in the Style field to convert.

Full rules: [reference/frameworks/client-first.md](../../reference/frameworks/client-first.md).
