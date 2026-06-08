# Naming framework comparison: BEM vs Lumos vs Finsweet Client First

**All three are first-class in this skill.** For a new project the skill asks which you want, with **Lumos** and **Finsweet Client-First** as the headline options (real Webflow projects with Designer authoring) and **BEM** as the lightweight, fully self-contained option. You can also name any other framework. This file is the chooser; the framework-specific authoring rules live in:

- [frameworks/lumos.md](frameworks/lumos.md) — Lumos **v2** ruleset
- [frameworks/client-first.md](frameworks/client-first.md) — Client-First **v2.1** ruleset
- [css-rules.md](css-rules.md) — BEM (the self-contained default)

> **Lumos v2 vs v1.** This skill targets **Lumos v2** (variable + container-query driven, breakpointless). Lumos v1 (legacy attribute utilities like `mt2`, `fs1`) is not generated. See [frameworks/lumos.md](frameworks/lumos.md).

> **Self-contained vs cloneable-referencing.** BEM output is **self-contained** — it inlines every token to a literal and defines everything itself, so it imports into any Webflow site with no setup. Lumos and Client-First output is **cloneable-referencing** — it applies the framework's global utilities/variables and keeps `var()` refs intact, so the user must **clone the framework's official Webflow project first** (it carries the Global Styles embed). That setup step is the price of cross-page deduplication and Designer ergonomics.

---

## Quick decision rule

| Project scope                            | Recommendation                                                              |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| 1 component / 1 section                  | **BEM** (this skill's default). Anything else is overkill.                  |
| ≤ 5 pages, single-team, code-first       | **BEM**. Project stays clean without the framework overhead.                |
| 6–10 pages, mixed code/Designer authoring | **BEM** still works. Lumos if the team already knows it.                    |
| 10+ pages, designer-heavy authoring      | **Lumos** or **Client First** — class deduplication pays off.               |
| 20+ pages, agency-built for client handoff | **Client First**. Built specifically for this scenario.                     |

The deciding factors:
- **How many pages?** Frameworks pay off through cross-page deduplication.
- **Who edits the site?** Designers in Webflow benefit from frameworks; code-first teams don't.
- **Will it be handed off to a non-technical client?** Client First is designed for this.

---

## Side-by-side

| Aspect                          | BEM (single underscore)                          | Lumos                                              | Finsweet Client First                              |
| ------------------------------- | ------------------------------------------------ | -------------------------------------------------- | -------------------------------------------------- |
| **Naming pattern**              | `.tool-card_title` (block_element)               | `.tool-card_title` + utility classes               | `padding-section-large`, `text-size-large`, etc.   |
| **Utility usage**               | Forbidden (rule #6)                              | Heavy — global utilities for spacing / typography  | Heavy — utilities are the foundation               |
| **Class manager hygiene at scale** | Clean: blocks group naturally                  | Mixed: utilities pollute the alphabetical list     | Pollutes heavily but consistently                  |
| **Designer ergonomics**         | Requires CSS knowledge                           | Designer-friendly (utilities = visual props)       | Most Designer-friendly of the three                |
| **Converter compatibility**     | ✅ Cleanest fit                                  | ⚠️ Conflicts with rule #6 (heavy utilities)        | ⚠️ Conflicts with rule #6                          |
| **Class collision risk**        | Low (named blocks are unique)                    | Medium (utility names are generic — `.padding-large` is everywhere)  | High (utility names extremely generic)             |
| **Learning curve (new dev)**    | Hours                                            | Days                                               | Day or two                                         |
| **Team handoff cleanliness**    | Best when team writes CSS                        | Best when team uses Designer + utilities           | Best for client handoff                            |
| **Documentation**               | This skill                                       | Free public docs, paid courses (Timothy Ricks)     | Free public docs, mature community                 |
| **CSS file size**               | Small (~30KB / 5 pages typical)                  | Medium (utility classes balloon)                   | Medium-large                                       |

---

## BEM (this skill's default)

**Naming pattern:** Block (kebab-case), single-underscore element, `is_` state combo classes.

```css
.tool-card { ... }
.tool-card_title { ... }
.tool-card_image { ... }
.tool-card.is_live { background: green; }
.tool-card.is_archived { opacity: 0.5; }
```

**Pros:**
- Each component is self-contained: one block = one set of related styles.
- Class manager in Webflow groups them naturally (alphabetical sort puts `tool-card`, `tool-card_image`, `tool-card_title` together).
- No collision with utility-class names from third-party imports.
- Plays cleanly with the converter (one class per element, no descendant rules).

**Cons:**
- Common values (eyebrow text style, default heading) get duplicated across components — same `font-size: 1.44rem` declaration in 4 places.
- Adding a new state means new combo class rules; no quick utility shortcut.
- For large projects, the typing cost of writing `.section-name_element-name` over and over adds up.

**When this skill's default works well:** ≤ 10 pages, code-first authoring, small team, converter pipeline. The BEM convention shines for projects in this range.

**When it starts to creak:** 15+ pages, designer-heavy authoring, frequent need to repeat the same 5–10 utility patterns (eyebrow / button / heading scale / spacing / etc.). Time to consider Lumos or Client First.

---

## Lumos

**Created by:** Timothy Ricks (lumosframework.com).

**Philosophy:** Hybrid. Use utility classes for global concerns (typography, spacing, color) and BEM-like custom classes for unique components.

**Naming pattern:**

```html
<!-- Section uses utility classes for layout -->
<section class="padding-section-large background-color-orange">
  <div class="container-large">
    <!-- Component uses BEM-style custom class -->
    <div class="hero_component">
      <h1 class="hero_headline heading-style-h1">...</h1>
      <p class="hero_eyebrow text-size-medium">...</p>
    </div>
  </div>
</section>
```

**Notable utility classes:**
- Layout: `padding-global`, `padding-section-small/medium/large`, `padding-vertical/horizontal`, `container-small/medium/large`.
- Typography: `heading-style-h1` through `heading-style-h6`, `text-size-tiny/small/medium/large`, `text-color-grey/orange/etc`.
- Display: `display-flex`, `display-grid`, `flex-row/column`, `align-center`, `gap-small/medium/large`.

**Pros:**
- **Cross-page deduplication.** Define `.heading-style-h1` once in Lumos's global stylesheet; every page that uses it gets the same rendering for free.
- **Designer-friendly.** A designer can drag/style elements in Webflow Designer using the utility palette without writing CSS.
- **Mature ecosystem.** Free docs, paid course, Discord community. Real industry adoption.
- **Predictable naming.** Once you learn Lumos, every Lumos site looks roughly the same — easier to onboard new contributors.

**Cons:**
- **Conflicts with converter rule #6.** Utility-heavy by design. Importing a Lumos page through the converter creates 200+ classes in Webflow's class manager.
- **Class manager pollution.** Webflow's class panel becomes a wall of utilities, harder to find your custom blocks.
- **Combo-class ergonomics in Designer.** A typical element has 4–6 classes stacked (e.g. `<div class="hero_content padding-vertical-large align-center text-color-white display-flex">`); Designer's combo class chain UI gets unwieldy.
- **Generic utility names collide easily.** `padding-global`, `text-size-medium`, etc. — chances are high another part of the site, a future import, or a team member's improvisation reuses one of these names with different values.

**When to use:** 10+ page projects where designers actively edit in Webflow Designer (not just code-first). The deduplication and Designer ergonomics outweigh the converter friction.

**Tradeoffs to accept if you go Lumos:**
- Disable converter rule #6 (or accept the bloat).
- Plan extra time for class collision detection across the site.
- Document the utility palette for the team / client.

---

## Finsweet Client First

**Created by:** Finsweet (finsweet.com/client-first).

**Philosophy:** Designed specifically for **agencies handing off Webflow sites to non-technical clients**. The naming convention prioritises clarity for someone who will edit the site without writing code.

**Naming pattern:**

```html
<section class="section_hero">
  <div class="padding-global">
    <div class="container-large">
      <div class="padding-section-large">
        <div class="hero_component">
          <h1 class="hero_heading heading-style-h1">...</h1>
          <p class="hero_subheading text-size-medium">...</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

**Notable patterns:**
- Section wrappers: `section_hero`, `section_features`, `section_cta`.
- Padding: `padding-global` (horizontal page padding), `padding-section-small/medium/large` (vertical section padding).
- Containers: `container-small/medium/large`.
- Components: `<name>_component`, `<name>_content`, etc.
- Utilities: `heading-style-h1` ~ `h6`, `text-size-tiny/small/medium/large/huge`, `text-weight-light/normal/medium/bold`, `text-align-left/center/right`.

**Pros:**
- **Clearest naming** of the three for non-technical clients to maintain. A client can look at `padding-section-large` and understand it without reading docs.
- **Most consistent across projects.** Every Client First site uses the same vocabulary. Hiring a Client First-trained designer to update an existing Client First site is frictionless.
- **Strong documentation.** Public, mature, step-by-step.

**Cons:**
- **Most class manager bloat** of the three. A typical page has 300+ classes.
- **Same converter rule conflict** as Lumos.
- **Verbosity in HTML.** Section markup is heavier (multiple wrapper divs for global padding / container / section padding).
- **Client First updates over time.** Versions 1, 2 — naming and structure change. Re-imports of older sites need migration.

**When to use:** Agency / freelance projects that will be handed to a non-technical client to maintain. The verbosity is the point — the client can edit the site without breaking it.

---

## What this skill supports natively

**All three.** Each framework has its own authoring reference, templates, and build behavior:

| Framework | Authoring rules | Templates | Build (`_build.py`) | Output |
| --- | --- | --- | --- | --- |
| **BEM** | [css-rules.md](css-rules.md) (the 7 rules) | `templates/` (root) | `FRAMEWORK = "bem"` | Self-contained: `:root` dropped, every `var()` inlined to a literal |
| **Lumos v2** | [frameworks/lumos.md](frameworks/lumos.md) | `templates/lumos/` | `FRAMEWORK = "lumos"` | Cloneable-referencing: component CSS only, `var()` + `u-*` kept intact |
| **Client-First v2.1** | [frameworks/client-first.md](frameworks/client-first.md) | `templates/client-first/` | `FRAMEWORK = "client-first"` | Cloneable-referencing: custom-class CSS only, utilities + `var()` kept |

When the user picks Lumos or Client-First:

1. **Read the matching `frameworks/*.md` reference end-to-end** before scaffolding — it carries the exact naming, structure, and utility vocabulary.
2. **Clone the framework's official Webflow project first.** Lumos v2 and Client-First both depend on a Global Styles embed that defines the utilities/variables the generated CSS references. See the "Setup first" section of each reference. Without the cloneable, imported markup renders unstyled.
3. **Rule #6 (avoid utilities) does not apply** — these frameworks are utility-driven by design. Authoring rules come from the framework reference, not the BEM 7 rules.
4. **Use the framework's templates and build preset** — `templates/lumos/` or `templates/client-first/`, each with a `_build.py` that has the right `FRAMEWORK` flag set.

For **any other framework** the user names, follow that framework's official docs and apply the same cloneable-referencing pattern (apply globals, keep `var()`, set `FRAMEWORK` to a non-BEM value so the build doesn't inline tokens).

---

## Recommendation

For a **real Webflow project** that designers or a client will edit in the Designer — pick **Lumos** (best designer-developer ergonomics, breakpointless, if the team is comfortable with it) or **Client-First** (cleanest handoff to non-technical clients, most consistent across projects). Both require cloning the framework's cloneable first.

Pick **BEM** when you want **zero setup and fully self-contained output** — a one-off component, a small site, or importing into a site that has no framework. It needs no cloneable and imports anywhere.

**Don't switch frameworks mid-project** unless you're prepared to rewrite every page — the structure and class vocabulary differ enough that a switch is a rewrite.
