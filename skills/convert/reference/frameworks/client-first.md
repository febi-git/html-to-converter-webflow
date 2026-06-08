# Finsweet Client-First (v2.1) — authoring reference for the converter

Client-First is a CSS naming and structure system for Webflow by **Finsweet**, designed for agencies handing sites to non-technical clients. This skill targets **Client-First v2.1**. When the user picks Client-First in a new project, follow this file instead of the BEM rules in [css-rules.md](../css-rules.md). Source: `finsweet.com/client-first` (and the Client-First Quick Guide).

---

## Setup first — clone the cloneable (do this before importing anything)

Client-First is **not self-contained**. All utility classes (`heading-style-*`, `padding-section-*`, `container-*`, …) and the project variables live in the official **Client-First cloneable**, whose **Global Styles** HTML embed must be present on every page. Generated output **references** those utilities — it never redefines them.

**Before importing a single generated section, the user must:**

1. Clone the official **Client-First** Webflow cloneable from `finsweet.com/client-first`. It carries the Global Styles embed and the full utility class set.
2. Confirm the **`global-styles` embed is present on every page** that receives imported markup.

If the user has NOT cloned it, stop and tell them — Client-First output looks unstyled in Designer because the utility classes won't exist. There is no fallback "self-contained Client-First" mode; that's what BEM is for.

---

## Class types

| Type | Purpose | Naming | Example |
| --- | --- | --- | --- |
| **Utility** | A reusable CSS-property combo applied across the project. Global by nature. | dashes `-` only | `text-size-large`, `background-color-primary` |
| **Global** | Used across the whole project; a further classification. Utility or custom can be global. | `-` or `_` | `faq_item`, `header_background-layer` |
| **Custom** | Specific to a component / page / element. The underscore defines the "custom folder". | underscore `_` | `testimonial-slider_headshot`, `team-list_headshot-wrapper` |
| **Combo** | A variant of a base class that inherits and adds styles. | `is-` prefix | `button is-secondary`, `header_content is-home` |

**Meaningful, complete names.** A class name answers "what is the purpose of this class?" Use full words, no abbreviations: `testimonials_wrapper` ✅, `col-2`, `flex-mobile-a-c` ❌.

**General → specific.** Read a custom class left-to-right from broad to narrow: `team-list_headshot-wrapper` = the "team-list" component folder → the headshot → its wrapper. Custom classes sharing the folder prefix (`team-list_…`) group together in the Navigator.

---

## Page structure

```html
<body>
  <!-- nav lives OUTSIDE main-wrapper (not page-specific content) -->
  <div class="navbar"> … </div>

  <div class="page-wrapper">
    <main class="main-wrapper">

      <section class="section_[identifier]">
        <div class="padding-global">
          <div class="padding-section-[size]">      <!-- v2.1: on the same padding-global div -->
            <div class="container-[size]">
              <!-- content -->
            </div>
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- global custom CSS embed -->
  <div class="global-styles"> … </div>
</body>
```

- **`page-wrapper`** — outermost parent of everything on the page.
- **`main-wrapper`** — the page-specific content; use a `<main>` tag for accessibility.
- **`section_[identifier]`** — wraps a section of content; use a `<section>` tag. e.g. `section_hero`, `section_features`, `section_cta`.
- **`padding-global`** — site-wide left/right outer padding.
- **`padding-section-[size]`** — top/bottom section padding (v2.1: applied on the `padding-global` div to reduce nesting). `padding-section-small` = 3rem, `-medium` = 5rem, `-large` = 8rem.
- **`container-[size]`** — max-width + centers content. `container-small` / `-medium` / `-large`.
- **`navbar`** — outside `main-wrapper`.
- **`global-styles`** — the Global Styles embed (from the cloneable); must be on every page.

---

## Typography utilities (apply — never redefine)

- **Headings:** `heading-style-h1` … `heading-style-h6` (4 / 3 / 2 / 1.5 / 1.25 / 1rem). Use the correct HTML heading tag for hierarchy; only apply `heading-style-*` to **override** the tag's default look (e.g. an `<h1>` that should look like an H3 → `heading-style-h3`). Always respect heading hierarchy for SEO.
- **Text size:** `text-size-large` (1.5rem), `text-size-medium` (1.25rem), `text-size-regular` (1rem), `text-size-small` (0.85rem), `text-size-tiny` (0.75rem).
- **Text color:** `text-color-primary`, `text-color-secondary`, `text-color-neutral` (extend with more as the project needs).
- **Text weight:** `text-weight-light` (300), `text-weight-normal` (400), `text-weight-semibold` (600), `text-weight-bold` (700), `text-weight-xbold` (800).
- **Text align:** `text-align-left | center | right`.
- **Text style:** `text-style-allcaps`, `text-style-italic`, `text-style-strikethrough`, `text-style-muted` (opacity 0.7), `text-style-2lines` / `text-style-3lines` (truncate), `text-style-link`.

Stack **typography** utilities together for unique-yet-global combos (`text-color-blue text-weight-semibold`). Avoid stacking non-typography classes onto typography classes. For very unique / deeply-stacked type, make a **custom** class (`hero_subtitle`, `footer_copyright-text`).

---

## Spacing

Two methods:

- **Spacing wrapper** — content inside a div with padding utilities: `padding-[direction]` (`padding-top/right/bottom/left/vertical/horizontal`) + `padding-[size]` (`padding-tiny/xxsmall/xsmall/small/medium/large/xlarge/xxlarge/huge/xhuge/xxhuge`, `padding-0`). Margins follow the same structure: `margin-[direction]` + `margin-[size]`.
- **Spacing block** — an empty div between elements: `spacer-[size]` (same size scale as padding).

Size scale (rem): tiny 0.125, xxsmall 0.25, xsmall 0.5, small 1, medium 2, large 3, xlarge 4, xxlarge 5, huge 6, xhuge 8, xxhuge 12.

**Section padding:** `padding-section-small/medium/large` (3 / 5 / 8rem).

`spacing-clean` removes native Webflow component spacing.

For unique spacing not covered by utilities, use a **custom** class (e.g. `form_input` with its own `margin-bottom`).

---

## More utilities (apply — never redefine)

- **Buttons:** `button`, `button is-secondary`, `button is-text`. `button-group` for horizontal space between two buttons.
- **Icons:** `icon-[size]` (height: `icon-small/medium/large`), `icon-1x1-[size]` (height+width: `icon-1x1-small` 1rem / `-medium` 2rem / `-large` 2.5rem).
- **Hide:** `hide`, `hide-tablet`, `hide-mobile-landscape`, `hide-mobile-portrait`.
- **Overflow:** `overflow-hidden | scroll | auto`.
- **Background color:** `background-color-primary` (#f5f5f5), `background-color-secondary` (#fff), `background-color-dark` (#000) — extend as needed.
- **Max width:** `max-width-xxsmall` … `max-width-xxlarge` (12 / 16 / 20 / 32 / 48 / 64 / 80rem), plus `max-width-full` and responsive `max-width-full-tablet` / `-mobile-landscape` / `-mobile-portrait`.
- **Utility helpers:** `align-center` (`margin: 0 auto`), `layer` (absolute, inset 0), `display-inlineflex`, `pointer-events-none` / `pointer-events-auto`, `z-index-1` / `z-index-2`.

---

## Units & stacking

- **Use `rem` for everything** — typography, spacing, widths. Root is 16px (`1rem = 16px`). To convert in the Style field, type `value/16 rem`. Browsers respect user font-size settings and zoom when sizes are in rem. Avoid `vw`/`vh` for full accessibility compliance.
- **Minimal stacking.** Less stacking = more control. Avoid "deep stacking" many utility classes on one element. To reduce stacking:
  1. Use a single **custom** class.
  2. Merge stacked utilities into a **combo** class (`faq_item is-dark`).
  3. Nest another div (useful when mixing different utility types, e.g. typography + max-width).

---

## Folders (Navigator organization)

The underscore creates folders in Webflow: `folder-name_element-name` — the first word before the `_` is the folder. One underscore = one folder; `folder-1_folder-2_element` nests. Renaming the folder prefix (`hero_` → `team_`) renames every class in that folder. Custom classes (with `_`) group by folder; utility classes (no `_`) land in the auto "Utility" folder.

---

## Designer-import requirements (what makes it import clean)

1. **Vanilla HTML/CSS only.** No utility/variable redefinitions and no reset in the output — the cloned project's Global Styles embed provides them.
2. **Reference utilities, don't recreate them.** Apply `padding-section-large`, `heading-style-h2`, etc.; never write CSS rules for them.
3. **Class-only selectors**, no descendant selectors — give each visible element its own class (custom or utility). No `::before`/`::after`; use a real div.
4. **Keep `var()` references intact** for any project variables (theme colors, etc.) — they resolve against the cloned project. The build does NOT inline them for Client-First.
5. **The `global-styles` embed must be present** on every page that receives imports.

These class-only / no-descendant / rem constraints overlap with BEM rules in [css-rules.md](../css-rules.md), but Client-First **keeps utilities and `var()` refs** (the opposite of BEM rules 5/6 and the inline-everything build). Don't apply the BEM token-inlining model here.

---

## Build behavior (Client-First)

With `FRAMEWORK = "client-first"` in [`_build.py`](../../templates/_build.py):

- **Keep `var()` references** — no inlining to literals.
- **No `:root` drop**, no `tokens.css`/`base.css`/`components.css` bundling — generated CSS is **custom-class only** (utilities come from the cloneable).
- The "zero `var()` may remain" sanity check is **disabled**.
- `COLLIDE_RENAMES` prefixing still exists but should stay short and **must never include Client-First utility classes** (`padding-global`, `container-large`, `heading-style-h2`, …) — they are intentionally global.
