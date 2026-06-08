# Lumos (v2) — authoring reference for the converter

Lumos is a CSS framework for Webflow by **Timothy Ricks**. This skill targets **Lumos v2** — the current, variable-driven, breakpointless system (container queries + CSS-variable state machinery). When the user picks Lumos in a new project, follow this file instead of the BEM rules in [css-rules.md](../css-rules.md).

> **v1 vs v2.** Lumos v1 (2023) was an attribute-selector utility system (`mt2`, `pd4`, `fs1`, matched via `[class*="…"]`). It is **not** what this skill generates. Everything below is **v2**, mirroring Timothy Ricks' own machine-readable generation spec (`github.com/lumosframework/skill` → `lumos-skill/SKILL.md`), which is the canonical source. If anything here is ambiguous for an edge case, that spec wins.

---

## Setup first — clone the cloneable (do this before importing anything)

Lumos v2 is **not self-contained**. All utilities (`u-*`) and variables (`--_theme---*`, `--_spacing---*`, …) are defined in a **Global Styles** HTML embed that ships with the official Lumos v2 Webflow project. Generated output **references** those globals — it never redefines them.

**Before importing a single generated section, the user must:**

1. Clone the official **Lumos v2** Webflow project (the cloneable carries the Global Styles embed, all variables, and base utilities). Start from `lumos.timothyricks.com` / `github.com/lumosframework`.
2. Confirm the **Global Styles embed is present on every page** that will receive imported markup. Imported component CSS assumes the embed already defines the utilities and variables it references.

If the user has NOT cloned the project, stop and tell them — Lumos output will look unstyled in Designer because the utilities and variables won't exist. There is no fallback "self-contained Lumos" mode in this skill; that's what BEM is for.

---

## Naming

**Custom (component) classes** — `[component]_[type]_[element]`, underscores separating parts:

- `card_testimonial_title`, `cta_secondary_visual_img`, `nav_link_wrap`.
- Broadest first → specific → element. Preferred element names: `_title` (not `_heading`), `_text` (not `_paragraph`), `_img` (not `_image`), `_link`, `_icon`, `_list`, `_item`.
- **`_wrap` marks a component or subcomponent root.** `tabs_wrap` is the component root; `tabs_link_wrap` is a subcomponent root. Any interactive root (`<a>`, `<button>`) and any element that contains component-classed children ends in `_wrap`.
- **Max 3 underscores.** When you'd need a 4th, start a new subcomponent name: `cta_secondary_icon_wrap`, **not** `cta_secondary_visual_icon_wrap`.
- **Hyphens only inside a multi-word part**, never as the `_wrap` separator: `tabs_link_wrap` ✅, `tabs_link-wrap` ❌.

**Utility classes** — always prefixed `u-`: `u-text-style-h2`, `u-section`, `u-container`. **Never write CSS for `u-*` classes** — they are defined by the Global Styles embed. You only apply them.

**Composition** — component class **first**, then utilities. Every element carries a component class; no bare element with only a utility class:

```html
<h2 class="hero_title u-text-style-h2">…</h2>   <!-- ✅ -->
<h2 class="u-text-style-h2">…</h2>              <!-- ❌ no component class -->
```

**Combo / variant classes** — `is-` prefix (`is-active`, `is-reversed`, `is-1`). In CSS they **must always be scoped to a component class**, never bare:

```css
.hero_card_wrap.is-reversed { … }   /* ✅ */
.is-reversed { … }                  /* ❌ never bare */
```

Combo classes must **physically appear in the HTML** or Webflow purges them on import. For a combo that only a JS toggle adds (and that has CSS), seed it inside a hidden div: `<div class="[component]_hidden u-display-none">`.

**States** — the only state class used for JS toggling is `.is-active`. Don't invent `.is-open`, `.is-visible`, etc. Beyond `.is-active`, v2 expresses state through the CSS-variable trigger system (`--_trigger---on/off`, `--_state---true/false`) rather than state classes in selectors.

---

## Page / section structure

Every section uses this triad:

```html
<section class="[name]_wrap u-section">
  <div class="[name]_contain u-container">
    <div class="[name]_layout">
      <!-- content -->
    </div>
  </div>
</section>
```

- `u-section` — flex column, applies theme background/text and top/bottom section spacing.
- `u-container` — max-width + horizontal margins; it is `container-type: inline-size`, so `@container` queries target **its children**.
- `[name]_layout` — the actual grid/flex layout div. **Never put grid/display directly on `u-container`** — because container queries target children, the layout must live on a child `_layout` div.
- The **first section on the page** uses page-top section spacing (`--_spacing---section-space--page-top`) to clear the nav, instead of `--main`.

There is no separate `page-wrapper` / `main-wrapper` requirement (that's Client-First). The `_wrap → _contain → _layout` triad is the structural unit.

---

## Utilities (reference — apply, never redefine)

**Section / container:** `u-section`, `u-container`

**Typography (visual size, independent of the HTML tag):**
- Headings: `u-text-style-display`, `u-text-style-h1` … `u-text-style-h6`
- Body: `u-text-style-large`, `u-text-style-main`, `u-text-style-small`
- The HTML tag (`h1`–`h6`) is semantic; the `u-text-style-*` utility controls the visual size. Use a real heading tag for hierarchy, override the look with the utility only when needed.

**Text wrappers (max-width handling):** `u-heading`, `u-text`. `u-text-trim-off` disables line-height trim. `u-rich-text` for CMS rich-text blocks.

**Alignment / spacing helpers:** `u-alignment-center`, `u-margin-trim` (strips first child's top / last child's bottom margin), `u-ignore-trim`, `u-child-contain`.

**Buttons:** wrap buttons in `u-button-wrapper`. There is **no button utility class** — button visuals go on the component class, using the button theme variables.

**Display / visibility:** `u-display-none`, `u-display-contents`, `u-hide-if-empty`, `u-hide-if-empty-cms`, `u-cover-absolute`. Responsive (container-query driven): `u-grid-above`, `u-grid-below`, `u-all-unset-above`, `u-all-unset-below`, `u-order-unset-above`, `u-order-unset-below`.

**Line clamp:** `u-line-clamp-1` … `u-line-clamp-4`.

**Embeds:** `u-embed-js`, `u-embed-css` (display:none holders).

**Accessibility:** `u-sr-only`.

**Theme:** `u-theme-light` (default), `u-theme-dark`, `u-theme-brand` — flip the `--_theme---*` variables for everything inside.

**Clickable component:** `clickable_wrap`.

---

## Variables (reference — apply, never redefine)

Use these instead of raw values. The Global Styles embed defines them; exact numeric defaults are set per-project in the Designer variable panel.

- **Spacing scale:** `--_spacing---space--1` … `--_spacing---space--8` (`--1`/`--2` are too small for text; use `--3`+).
- **Section padding:** `--_spacing---section-space--none | --small | --main | --large | --page-top`.
- **Max widths:** `--max-width--small` (≈50rem), `--max-width--main` (≈90rem), `--max-width--full` (100%).
- **Radius:** `--radius--small | --main | --round`. **Border width:** `--border-width--main`.
- **Typography:** `--_typography---font--primary-regular | primary-medium | primary-bold`; `--_typography---letter-spacing--tight` (= -0.03em). Never write raw `400/500/700` or `-0.03em`.
- **Theme:** `--_theme---background`, `--_theme---background-2`, `--_theme---text`, `--_theme---border`, link vars `--_theme---text-link--*`, button vars `--_theme---button-primary--*` and `--_theme---button-secondary--*` (background/text/border + `-hover`).
- **Trigger / state:** `--_trigger---on: 1` / `--_trigger---off: 0`; `--_state---true: 1` / `--_state---false: 0`.

These `var(--…)` references are **kept intact** in the generated CSS — the build script does NOT inline them (see [`_build.py`](../../templates/_build.py) with `FRAMEWORK = "lumos"`). They resolve against the cloned project's variables in Webflow.

---

## Custom vs utility — what you write CSS for

- **Write CSS only for component classes** (and `@container` rules on `_layout` children). **Never** write CSS for `u-*` utilities or redefine variables.
- Every element gets a component class; utilities stack after it.
- SVG `<path>` / `<line>` that need stroke styling get their own sibling-named component class (`enterprise_button_path`, not `…_svg_path`).

---

## Units

- **No `px`.** Default to **`rem`**. Root is assumed 16px (`1rem = 16px`).
- Text `max-width` in **`ch`**. Container-query breakpoints in **`em`**. Scalable visual compositions in **`em`** (one `font-size: 1cqw` anchor). Never `vw` for fonts.
- Input `font-size` must be ≥ `1rem` (below triggers iOS auto-zoom).

---

## Designer-import requirements (what makes it import clean)

Generated output must satisfy all of these — they're the difference between a clean import and a broken one:

1. **Vanilla HTML/CSS/JS only.** No CSS resets, no `:root`, no `body` styles, no utility or variable redefinitions — the Global Styles embed already provides them.
2. **`<style>` is the first child** inside the section `_wrap`; **`<script>` is the last child.**
3. **No inline `style=""`.** All CSS lives in the `<style>` block.
4. **Class-only selectors.** No tag selectors, IDs, `data-*` attribute selectors, or descendant selectors. No `::before` / `::after` — use a real `<div>` with a class.
5. **Combo classes must appear in the HTML** (Webflow purges unused). Seed JS-only combos in a `[component]_hidden u-display-none` div.
6. **Empty/decorative divs need `padding: 0`** — Webflow injects default padding on empty elements.
7. **Text blocks use `<div>`**; `<span>` only inside `h1`–`h6` / `p`.
8. **Buttons wrapped in `u-button-wrapper`**, styled via the button theme variables.

These constraints (class-only, no descendants, no complex pseudos, rem) overlap with several BEM rules in [css-rules.md](../css-rules.md) — but Lumos **keeps utilities and `var()` refs** (the opposite of BEM rule 5/6 and the inline-everything build). Don't apply the BEM token-inlining model here.

---

## Build behavior (Lumos)

With `FRAMEWORK = "lumos"` in [`_build.py`](../../templates/_build.py):

- **Keep `var()` references** — no inlining to literals.
- **No `:root` drop**, no `tokens.css`/`base.css`/`components.css` bundling — generated CSS is **component-class only**.
- The "zero `var()` may remain" sanity check is **disabled** (framework var refs are expected and correct).
- `COLLIDE_RENAMES` prefixing still exists but should stay short and **must never include `u-*` utilities or framework variables** — those are intentionally global.

---

## Sources

- `github.com/lumosframework/skill` → `lumos-skill/SKILL.md` — official v2 generation ruleset (canonical).
- `github.com/lumosframework/lumos-v2` → `Global Styles.html` — the v2 global embed (variables, utilities, container thresholds, form components).
- `lumos.timothyricks.com` — official docs.
