# Variable mapping at export

Why your source code uses `var(--color-orange)` but the published Webflow site shows `#ff4f41`. And why this is intentional.

---

## The strategy: inline tokens as literals

The build script in [templates/_build.py](../templates/_build.py) does two things to the bundled CSS at export time:

1. **Drops the `:root { … }` token block.** The `:root` block in `tokens.css` defines `--color-orange: #ff4f41`, `--font-size-h1: 2.986rem`, etc. The build removes it entirely from the output.
2. **Replaces every `var(--token)` reference with its literal value.** `color: var(--color-orange)` becomes `color: #ff4f41`.

So the generated `.webflow.css` has:
- ❌ No `:root { ... }` block.
- ❌ No `var(--...)` references.
- ✅ Only literal hex codes, rem values, font stacks, etc.

---

## Why inline literals instead of preserving variables

Webflow's Style panel has a colour picker. When the imported CSS contains `color: var(--color-orange)`, Webflow shows it as a *variable reference* — to edit the colour, you have to find the variable definition first.

When the imported CSS contains `color: #ff4f41`, Webflow's colour picker treats it as a standalone editable swatch. Click → change to a different hex → done. No hunting for the variable.

For agency / client handover scenarios, this is the right call. The client doesn't care about token systems; they want to click and change colours.

**Tradeoff:** future edits to your local `tokens.css` don't propagate to already-imported pages. Each page must be rebuilt + reimported when the design system changes. This is a known cost of the strategy.

---

## How the mapping works

In `_build.py`:

```python
VAR_TO_LITERAL = {
    "var(--color-orange)":      "#ff4f41",
    "var(--color-dark-orange)": "#cf4111",
    "var(--color-black)":       "#1f1f1f",
    # ... etc, one entry per token
    "var(--space-l)":           "2rem",
    "var(--font-size-h1)":      "2.986rem",
    "var(--transition-base)":   "200ms ease",
    # ...
}
```

In `build_css()`:

```python
for k, v in VAR_TO_LITERAL.items():
    bundled = bundled.replace(k, v)
```

Plain string replacement. No regex needed because `var(--...)` references have no nesting and no spacing variations the source can introduce (you write `var(--color-orange)` exactly).

---

## Auto-population from `tokens.css` (recommended)

The default `_build.py` ships with `VAR_TO_LITERAL = {}` and a helper that auto-populates it from your `tokens.css`. The helper:

1. Reads `tokens.css`.
2. Parses every `--<name>: <value>;` line inside `:root { … }`.
3. Resolves `var(--<other-name>)` references (semantic shortcuts like `--color-text: var(--color-black)`) to their underlying literal.
4. Emits a complete `var(--name)` → `<value>` map.

You only have to write `VAR_TO_LITERAL` by hand if you want to override a token's literal at build time — for example, exporting one page in a darker variant without changing `tokens.css`.

---

## The sanity check

After the build runs all replacements, it scans the output CSS for any leftover `var(--...)` references:

```python
def sanity_check_vars(css):
    leftover = sorted(set(re.findall(r"var\(--[a-z][a-z0-9_-]*\)", css)))
    if leftover:
        print("ERROR: var() refs remain in output (build inlines all tokens):")
        for u in leftover:
            print(" ", u)
        print()
        print("Add a mapping for each missing token to VAR_TO_LITERAL in this file.")
        sys.exit(1)
    print("OK: all token vars inlined as hex / literals.")
```

If any `var()` ref leaks through, the build **fails** with a list of unmapped tokens. The user must either:

1. Add the missing token to `VAR_TO_LITERAL` (or to `tokens.css` if it should be auto-detected), then rebuild.
2. Replace the source reference with a literal value (probably indicates a bug — why is the source using a token that doesn't exist in `tokens.css`?).

The sanity check is non-negotiable. Without it, an unmapped token references a CSS variable that doesn't exist on the published Webflow site (because the `:root` block was stripped), and the affected element renders with browser defaults — usually black text or no padding. Subtle, hard to debug, easy to miss in QA.

---

## What if I want to keep variables in the export?

You can — change the strategy. Two approaches:

**Approach A: Don't strip the `:root` block.** Comment out the `re.sub(r":root\s*\{[^}]*\}\s*", "", bundled, count=1)` line in `build_css()`. The output keeps your `:root` block intact, and `var(--...)` refs resolve normally.

Trade-off: Webflow Designer treats variables as references, not editable swatches. Class manager fills with `--color-orange` style entries.

**Approach B: Map our tokens to Webflow's existing variables.** If the Webflow site already has its own variables (e.g., `--brand-primary`, `--neutral-darkest`), you can map yours to theirs:

```python
VAR_TO_LIVE = {
    "var(--color-orange)": "var(--brand-primary)",
    "var(--color-black)":  "var(--neutral-darkest)",
    # ...
}
for k, v in VAR_TO_LIVE.items():
    bundled = bundled.replace(k, v)
```

This makes your imported page reference the live site's design tokens. When the live site's tokens change, your imported page updates automatically — the cleanest "design system" outcome. Trade-off: you need to know the live site's variable names (read its export CSS to learn them), and the live site must already have those variables defined or your import shows browser defaults.

**Approach C: Hybrid.** Use `VAR_TO_LITERAL` for design values that should be page-specific (e.g., a one-off marketing campaign colour) and `VAR_TO_LIVE` for site-wide design tokens. The script can support both — apply `VAR_TO_LIVE` first, then `VAR_TO_LITERAL` for whatever didn't match.

The default `_build.py` template implements Approach A only. For B and C, modify the script as described.

---

## When to override `VAR_TO_LITERAL` manually

If `tokens.css` defines:

```css
--color-orange: #ff4f41;
```

But for one specific page export you want orange to be `#ff6b5a` (a marketing campaign variant), override:

```python
VAR_TO_LITERAL = {
    "var(--color-orange)": "#ff6b5a",  # campaign variant; rest auto-populated
}
```

The auto-population fills in everything else but respects manual overrides.

---

## Checklist before importing

- [ ] `tokens.css` has every variable your source code references.
- [ ] Build script ran successfully (no sanity check failures).
- [ ] Generated `.webflow.css` has zero `var(--...)` references (you can verify: `grep "var(--" path/to/<slug>.webflow.css` should return nothing).
- [ ] Generated `.webflow.css` has no `:root { ... }` block (the live site's tokens stay clean).

If any of these is off, fix the source / build script first. Don't import broken CSS.
