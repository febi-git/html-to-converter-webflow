# Mode A: Build a single component or section

Use this mode when the user wants to ship one block to Webflow — a hero, a CTA strip, a single card, a stats row. No full-page scaffold needed; minimum viable workflow.

## When NOT to use this mode

- If the user is going to add more sections later, mode (c) `multi-page-project.md` is the better fit — it sets up a project structure that scales.
- If the user is patching an existing live page in Webflow, mode (b) `existing-site.md` is better.

If unsure, ask.

## Flow

### Step 1 — Confirm the basics

Before scaffolding, confirm with the user:

1. **What is the component?** (e.g. "a hero with a wave canvas", "a 4-up service grid", "a stats strip")
2. **Will it be embedded in an existing Webflow site?** If yes, you need to know whether the site already has classes that might collide. Skim [reference/class-collisions.md](../reference/class-collisions.md). If the user has the existing site's CSS export, do a quick collision check.
3. **What's the design source, and what are you actually going for?** Don't settle for a one-word answer here — this is where the component succeeds or fails. Invite the user to:
   - **Explain the idea in their own words** — the purpose of the component, the feel they want, anything they specifically like or want to avoid.
   - **Share references**: a screenshot or mockup, a Figma link, a live URL to emulate, or an existing component/codebase to match the style of. If they paste or point to reference code, read it before authoring.
   - If they have nothing to share, say so and proceed with sensible defaults — but ask before assuming. (This is the per-mode reinforcement of the global "Gather the design intent" step in [SKILL.md](../SKILL.md).)
4. **Does the component need animation?** If yes, you'll wire GSAP — confirm the user understands GSAP must be added to Webflow's Footer Code (covered in [reference/webflow-runtime.md](../reference/webflow-runtime.md)).

### Step 2 — Scaffold a minimal working directory

For a single component, a flat structure is fine:

```
my-component/
├── index.html         # local preview (open in browser)
├── component.css      # the component's styles only
├── component.js       # optional, only if the component needs JS
└── _build.py          # parameterized build script
```

Copy from templates:
- [templates/page-template.html](../templates/page-template.html) — strip everything except the `<head>` boilerplate and the `<main>` shell. Drop the navbar/footer placeholders.
- [templates/_build.py](../templates/_build.py) — set `PAGE_SLUG = "component"` (or whatever name fits).

You don't need separate `tokens.css` / `base.css` / `components.css` files for a single component. Either:
- **Embed tokens directly in `component.css`** under a `:root` block at the top, OR
- **Inline literal values throughout** and skip tokens entirely — fine for a one-off.

If the component is going into a site that already has its own token system, **don't** add a `:root` block — that pollutes the live site's variables. Inline literals only.

### Step 3 — Author the component

Follow the 7 CSS rules in [reference/css-rules.md](../reference/css-rules.md). The most common mistakes for a single component are:

- Using descendant selectors (`.hero h2 { ... }`) instead of a class on the child element (`.hero_headline { ... }`).
- Using PX instead of REM.
- Stacking utility classes on elements (`<div class="flex gap-4 items-center">`) — name the block instead.

Test the component locally by opening `index.html` directly in a browser.

If the component needs animation:

1. Write the JS as a plain IIFE in `component.js`.
2. Include the `inDesigner` guard at the top of the IIFE — see [templates/inDesigner-canvas-snippet.js](../templates/inDesigner-canvas-snippet.js) and [reference/designer-canvas-fixes.md](../reference/designer-canvas-fixes.md). This single fix saves the most pain in Webflow Designer.
3. Don't wrap it in `Webflow.push()` yourself — the build script does that.

### Step 4 — Configure `_build.py` for collision avoidance

Open `_build.py` and fill in:

- `PAGE_SLUG` — your component name.
- `COLLIDE_RENAMES` — every class your component uses **that already exists on the target Webflow site**. To detect:
  - If the user has the site's exported CSS, grep it: `grep -E '^\.<class-name>(\s|\.|,|\{)' path/to/site.css`
  - If the user doesn't have an export, default to prefixing every class your component defines (zero-collision, defensive).
- `VAR_TO_LITERAL` — only if you used CSS variables. If you inlined literal values directly, leave it empty.

See [reference/class-collisions.md](../reference/class-collisions.md) for the detection workflow.

### Step 5 — Run the build

```bash
python _build.py
```

It produces three files: `<slug>.webflow.html`, `<slug>.webflow.css`, `<slug>.webflow.js`. The sanity check fails the build if any unexpected `var()` refs leak through — see [reference/variable-mapping.md](../reference/variable-mapping.md).

### Step 6 — Import into Webflow

Walk the user through [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md). For a single component, the abridged version is:

1. Open the converter at https://moden.club/tools/html-to-webflow.
2. Paste each `.webflow.*` file into its respective tab (HTML / CSS / JS).
3. Click **`→ Convert to Webflow`**. The converter copies a Webflow-pasteable markup snippet to your clipboard — there is no API push or sign-in, clipboard copy is the only flow.
4. Note that the converter inlines your CSS/JS as `<style>`/`<script>` Embed nodes inside the component. For a reusable component, relocate them to site Custom Code after pasting — see *"What the converter actually outputs"* in [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md).
5. **For an existing page:** switch to Webflow Designer and paste into the canvas at the insertion point (or into a Webflow Embed element on that page). **For a brand-new page:** create the page in Webflow's Pages panel first, then paste into its canvas.
6. Re-link any images: see [reference/asset-handling.md](../reference/asset-handling.md).
7. If using GSAP: confirm the GSAP + ScrollTrigger CDN tags are in **Project Settings → Custom Code → Footer Code**. See [reference/webflow-runtime.md](../reference/webflow-runtime.md).
8. Publish to staging, smoke-test in the Designer canvas (no scroll lag, no layout glitches), publish to production.

### Step 7 — Show the user, iterate

After import, ask the user to confirm the component looks correct in Designer + on the published site. If not, edit the source files (NOT the `.webflow.*` outputs), re-run `_build.py`, and re-import.

**Re-import cleanup (important — there is no page to delete in this mode).** Mode B re-imports delete the whole page, which prunes orphan classes for you. Re-importing a single component does *not* — Webflow keeps every class from the previous paste forever, and auto-suffixes (`acme-card`, `acme-card-2`, …) if the new paste collides. Before pasting the rebuilt version:

1. Delete the **old pasted instance** from the page (select it in the canvas/Navigator → Delete).
2. Open the **Class Manager** (Style Manager → Classes) and delete the previous version's classes that nothing else references (right-click → Delete) — especially any you renamed or removed in the rebuild.
3. Then paste the new converter output.

Skipping this is the #1 source of class-manager bloat for single-component workflows. See [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md) → *Class manager check*.

## Common one-component pitfalls

- **Component disappears on the published site even though Designer looks fine** → likely a class collision. Check whether your component class name is already used elsewhere on the live site. Add to `COLLIDE_RENAMES` and rebuild.
- **GSAP animations don't fire in the published site** → GSAP CDN missing from Footer Code, OR the IIFE wasn't wrapped in `Webflow.push()` (your build script should have done it; check the `.webflow.js` output).
- **Pill-shaped flex children stretch full-width in Designer canvas** → add `width: fit-content` to those elements. See [reference/designer-canvas-fixes.md](../reference/designer-canvas-fixes.md).
- **ScrollTrigger animations fire from a stale layout on cold load** → use a custom rAF-throttled scroll listener instead of `scrub`. See [reference/designer-canvas-fixes.md](../reference/designer-canvas-fixes.md).

## When the user is done

- Run the build one final time.
- Confirm the `.webflow.*` files committed are current.
- Note in any project doc / Linear ticket: "uses the `/html-to-webflow:convert` skill; rebuild via `python _build.py` before re-importing."
