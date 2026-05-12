# CSS Authoring Rules

The 7 rules that make CSS importable into Webflow via the moden.club converter.

---

## Why these rules exist

The converter parses your CSS and creates Webflow classes from it. Anything that doesn't map to **one class on a single element** gets dropped or mangled. Webflow's class manager only understands flat class names; the converter has to translate everything else into something Webflow can model. The 7 rules below are the boundaries of "things the converter can model cleanly."

---

## Rule 1 — Use REM units, not PX

Webflow stores sizes as numbers — REM is the safe unit because it scales with root font-size and the converter preserves it.

✅ `padding: 1.5rem 2rem;`
❌ `padding: 24px 32px;`

**Exceptions:** `1px` borders, line-height (unitless), media query breakpoints (px is fine), letter-spacing (em).

## Rule 2 — BEM with single underscore

Block names in kebab-case. Element separator is **one** underscore (not two).

✅ `.tool-card`, `.tool-card_image`, `.tool-card_title`
❌ `.tool-card__image` (double underscore — this is BEM proper but the converter rule is single)
❌ `.toolCard_image` (camelCase block)

State modifiers use `is_` prefix and live as combo classes:

✅ `.tool-card.is_live { … }` applied as `<div class="tool-card is_live">`
❌ `.tool-card_live` (looks like an element, not a state)
❌ `.tool-card--live` (double-dash modifier)

## Rule 3 — Class-only styling

No ID selectors. No element selectors (except in the reset block of `base.css` for `*`, `html`, `body`, and unstyled defaults).

✅ `.heading_xl { font-size: 2.986rem; }`
❌ `h1 { font-size: 2.986rem; }`
❌ `#hero-title { … }`

In HTML: `<h1 class="heading_xl">` — the tag is for semantics, the class controls visuals.

## Rule 4 — No descendant selectors

The converter only understands one class per rule. A descendant selector creates a relationship Webflow can't model directly.

✅ `.tool-card_title { color: var(--color-orange); }`
❌ `.tool-card .title { color: var(--color-orange); }`
❌ `.tool-card > h3 { … }`
❌ `.tool-card h3 { … }`

If a child needs styles, give it its own class.

## Rule 5 — Simple selectors only

A "simple selector" = one class, optionally combined with another class on the **same element** (combo class), optionally with a basic state pseudo (`:hover`, `:focus`, `:active`).

✅ `.button { … }`
✅ `.button:hover { … }`
✅ `.button.button_outline { … }` ← combo class on same element, OK
✅ `.tool-card.is_live { … }` ← combo class on same element, OK
❌ `.tool-card:nth-child(2n+1) { … }`
❌ `.button + .button { … }` (sibling)
❌ `[data-state="live"] { … }`

## Rule 6 — Avoid heavy utility classes

Tailwind-style utilities (`.mt-4`, `.text-center`, `.flex`) explode into hundreds of one-off Webflow classes. Build components with semantic block names instead.

✅ `<div class="hero_actions">` (block name → one Webflow class)
❌ `<div class="flex gap-4 mt-8 items-center">` (4 utility classes → 4 Webflow classes for one element)

A small handful of layout helpers is fine (`.container`, `.section`). The line is: **if it represents a structural element, name it; if it represents a single CSS property, don't.**

**Exception:** Lumos and Finsweet Client First projects intentionally violate this rule for cross-page deduplication. See [frameworks-comparison.md](frameworks-comparison.md). For BEM (this skill's default), follow rule 6 strictly.

## Rule 7 — No complex pseudo-selectors

✅ `:hover`, `:focus`, `:focus-visible`, `:active`, `:disabled`
❌ `:nth-child(…)`, `:nth-of-type(…)`, `:has(…)`, `:not(…)`, `:where(…)`, `:is(…)`, `::before`, `::after`

Pseudo-elements (`::before`, `::after`) sometimes work via Webflow's "before/after" embed feature — but the converter doesn't import them reliably. If a section needs decorative content, use a real `<div>` or `<span>`.

---

## Naming Cheatsheet

| Concept             | Pattern                  | Example                                |
| ------------------- | ------------------------ | -------------------------------------- |
| Block               | `kebab-case`             | `.tool-card`, `.hero`, `.process-step` |
| Element of a block  | `block_element`          | `.tool-card_image`, `.hero_title`      |
| Sub-element         | `block_parent-child`     | `.tool-card_tag-list`                  |
| Variant of a block  | `block_variant` (combo)  | `.button`, `.button_outline`           |
| State modifier      | `is_state` (combo)       | `.tool-card.is_live`, `.nav.is_open`   |
| Layout primitive    | shared, kebab-case       | `.container`, `.section`               |

**One block per component.** A `tool-card` block owns: `tool-card_image`, `tool-card_body`, `tool-card_title`, `tool-card_description`, `tool-card_tags`, `tool-card_cta`. None of those names should appear under a different block.

---

## File organisation

| File                          | Contents                                                      |
| ----------------------------- | ------------------------------------------------------------- |
| `tokens.css`                  | All design tokens as CSS custom properties on `:root`.        |
| `base.css`                    | Reset, font imports, typography classes, `.container`, `.section`. |
| `components.css`              | Buttons + any component reused across 2+ pages.               |
| `pages/<slug>/<slug>.css`     | Page-specific section components.                             |

**Token rule:** never hardcode a color, font-size, or spacing value in a component or page CSS file. If you need a new value, add it to `tokens.css` first (with a name), then reference it. If unsure whether to add a token, ask the user before adding.

**Promotion rule:** a component starts in its page CSS file. Move it to `components.css` only when a second page needs it.

---

## HTML scaffolding pattern

Every section follows this structure:

```html
<section class="section [section_modifier]">
  <div class="container">
    <!-- block-level content -->
  </div>
</section>
```

The `.section` provides vertical rhythm; `.container` provides horizontal max-width. Section content is the actual component (e.g., `<div class="hero_content">…</div>`).

---

## Worked example: adding a "stats strip" with 3 stats

1. Pick a block name: `stats-strip`.
2. In the page CSS, add the block + its elements:
   ```css
   .stats-strip {
     display: grid;
     grid-template-columns: repeat(3, 1fr);
     gap: var(--space-l);
   }
   .stats-strip_item { … }
   .stats-strip_value { font-size: var(--font-size-h1); color: var(--color-orange); }
   .stats-strip_label { font-size: var(--font-size-s); color: var(--color-text-muted); }
   ```
3. In HTML, structure it flatly:
   ```html
   <div class="stats-strip">
     <div class="stats-strip_item">
       <p class="stats-strip_value">$125M+</p>
       <p class="stats-strip_label">Ad Spend Managed</p>
     </div>
     …
   </div>
   ```
4. No descendant selectors. Each visible thing has a class. Each class has one rule.
