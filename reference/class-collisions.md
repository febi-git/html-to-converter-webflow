# Class collision handling

The single biggest cause of "import looks fine in Designer but is broken on the published site" issues. Read this carefully.

---

## The problem

When the converter imports your code into Webflow, every class becomes a real entry in Webflow's class manager. **If a class with the same name already exists on the site, Webflow merges your rules into the existing class** — and you can't tell from the Designer.

Example: your code has `.button { background: orange }`. The live site already has `.button { background: blue; padding: 1rem 2rem; border-radius: 0.5rem }`. After import, the site's `.button` becomes:

```css
.button {
  background: orange;       /* your rule wins */
  padding: 1rem 2rem;       /* preserved from existing */
  border-radius: 0.5rem;    /* preserved from existing */
}
```

Two consequences:
1. **Every other page on the site that uses `.button` is now affected.** You changed the brand button colour everywhere without intending to.
2. **Your import looks correct on its page, because the merged class still has your rule.** You won't notice until a stakeholder reports "why did all the buttons turn orange?"

---

## The solution: prefixing colliding classes

The build script in [templates/_build.py](../templates/_build.py) maintains a list of class names that exist on the live Webflow site. Every name in that list gets prefixed with `acme-` (or whatever prefix you configure) in the generated `.webflow.{html,css,js}` files.

Source code stays unprefixed (so local preview matches your mental model). The build adds the prefix on the way out.

**Source HTML:**
```html
<a class="button button_outline">Click me</a>
```

**Generated `.webflow.html`:**
```html
<a class="acme-button acme-button_outline">Click me</a>
```

**Generated `.webflow.css`:**
```css
.acme-button { ... }
.acme-button_outline { ... }
```

After import, Webflow has `.acme-button` and `.acme-button_outline` as new classes. The live site's existing `.button` is untouched. No bleed-through.

---

## Building the `COLLIDE_RENAMES` list

### If you have a Webflow site export

Webflow's "Export Code" feature dumps the entire site as `.zip`. Inside, look for `<site-name>.webflow/css/<site-name>.css`. The `:root` block at the top has all the CSS variables; the rest of the file has every class definition.

Extract every top-level class name:

```bash
grep -oE '^\.[a-zA-Z][a-zA-Z0-9_-]*' path/to/<site-name>.css | sort -u
```

Every class returned exists on the live site. **Any class your new code uses that matches one of these is a collision.** Add to `COLLIDE_RENAMES` in your `_build.py`.

### If you don't have an export

Two options:

1. **Export the site first.** Webflow Designer → Settings → Export Code → Download. Then run the grep above.
2. **Default to prefixing every class.** Defensive, zero-collision, but pollutes your generated CSS with `acme-` everywhere. Acceptable for a one-off component (mode A).

---

## Detection workflow during authoring

When you create a new block name in your source code, immediately check whether it collides:

```bash
grep -E '^\.<your-block-name>(\s|\.|,|\{)' path/to/<site-name>.css
```

If any line returns, you have a collision. Add the block name (and all its elements) to `COLLIDE_RENAMES`.

For example, if you create `.tool-card` and grep finds it on the live site, add to `COLLIDE_RENAMES`:

```python
COLLIDE_RENAMES = [
    # ... existing ...
    "tool-card",
    "tool-card_top",
    "tool-card_image",
    "tool-card_title",
    "tool-card_description",
    "tool-card_cta",
    # add every element of the block too
]
```

---

## Why prefix every element of a colliding block?

If `.tool-card` collides, `.tool-card_image` probably does too (same designer made them, same naming convention). Prefixing the block but not the elements creates a confusing mix:

```html
<!-- BAD: only block prefixed -->
<div class="acme-tool-card">
  <img class="tool-card_image">    <!-- this still collides -->
  <h3 class="tool-card_title">     <!-- this still collides -->
</div>
```

vs

```html
<!-- GOOD: block + all elements prefixed -->
<div class="acme-tool-card">
  <img class="acme-tool-card_image">
  <h3 class="acme-tool-card_title">
</div>
```

Always add the full block + elements list to `COLLIDE_RENAMES`. The build script's selector-rename regex is greedy in the right way — it matches longest names first so `.section_large` is handled before `.section`.

---

## What the build script does internally

In [templates/_build.py](../templates/_build.py), three functions handle this:

1. **`COLLIDE_RENAMES` list** — names you want prefixed.
2. **`_apply_class_renames_in_attr(text)`** — replaces matching tokens inside HTML `class="..."` attributes.
3. **`_apply_class_renames_in_selectors(text)`** — replaces matching `.classname` occurrences in CSS rules and JS string selectors.

Run order: HTML → CSS → JS. Each pass uses the same `RENAME_MAP = {n: PREFIX + n for n in COLLIDE_RENAMES}`.

The renamer sorts longest-first so prefix matches don't cascade — without that, `.section_large` would become `.acme-section_large`'s prefix being applied to `.section` first, breaking the longer name. Sort order solves this.

---

## What gets prefixed automatically vs manually

| Type                                 | Auto-prefixed?        | Notes                                                                       |
| ------------------------------------ | --------------------- | --------------------------------------------------------------------------- |
| Classes in `class="..."` attributes  | ✅ Yes                | If the class name is in `COLLIDE_RENAMES`.                                  |
| `.classname` in CSS selectors        | ✅ Yes                | Including combo classes (`.section.section_dark`).                          |
| `.classname` in JS query selectors   | ✅ Yes                | `gsap.from(".hero", ...)` becomes `gsap.from(".acme-hero", ...)`.            |
| `data-*` attributes                  | ❌ No                 | Out of scope — the build doesn't transform them.                            |
| Class names inside JSON / config     | ❌ No                 | If your JS has class names in a JSON literal, you'll need to handle manually. |

---

## Choosing a prefix

The default is `acme-`. Pick something short and project-specific:

- `acme-` for an Acme Corp project.
- `b3-` for an internal third-revision build.
- `site-` for a generic single-site project.

Update `PREFIX` in your `_build.py`. Two-to-five characters works best — long enough to be distinctive, short enough to not bloat the markup.

---

## When NOT to prefix

If you're building a completely new Webflow site and you have control over every class on the site, you don't need prefixing — there's nothing to collide with. Set `COLLIDE_RENAMES = []`. The build script becomes a CSS bundler + variable inliner, nothing more.

For the multi-page-project mode (mode C), this is the common case at the start of a project. As the project grows, classes you imported earlier may end up colliding with classes you introduce in later pages. Document the existing classes in a project README or `pages/_shared/CONVENTIONS.md` so future contributors don't reuse names.

---

## Real example

A typical marketing site has classes named `.container`, `.section`, `.button`, `.hero`, `.tool-card` (among others). A full `COLLIDE_RENAMES` for that site looks like:

```python
COLLIDE_RENAMES = [
    "container",
    "section", "section_small", "section_large", "section_hero",
    "section_dark", "section_orange", "section_alt",
    "button", "button_outline", "button_dark", "button_light",
    "button_large", "button_small", "button_ghost-light",
    "hero-section",
    "hero", "hero_content", "hero_eyebrow", "hero_headline",
    "hero_headline-line", "hero_subheadline", "hero_actions",
    "hero_stats", "hero_stat", "hero_stat-value", "hero_stat-label",
    "tool-card", "tool-card_top", "tool-card_icon", "tool-card_icon-svg",
    "tool-card_status", "tool-card_status-dot", "tool-card_status-label",
    "tool-card_title", "tool-card_description",
    "tool-card_features-eyebrow", "tool-card_features",
    "tool-card_feature", "tool-card_feature-tick", "tool-card_feature-label",
    "tool-card_cta",
]
```

Every block + element of every block that collides. Adding a block name without its elements is a partial fix that will bite you later.
