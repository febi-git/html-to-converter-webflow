# Webflow Designer checklist

The Webflow-side workflow for getting your built `.webflow.{html,css,js}` bundle live. Walk the user through this end-to-end the first time; for subsequent imports, the user runs through it themselves.

This file documents both the **manual Designer flow** and the **MCP-assisted flow** (when Webflow MCP tools are connected). Use whichever is available; manual is always the fallback.

---

## Pre-import checklist (do once per Webflow project)

These are one-time setup steps. Do them before the first page import; they don't need to be redone for subsequent imports.

### 1. Add GSAP + ScrollTrigger CDN to Footer Code

If your code uses GSAP (most page animation patterns do):

**Manual:**
1. Webflow Designer → top-left **Webflow logo** → **Project Settings**.
2. **Custom Code** tab → **Footer Code** section.
3. Paste:
   ```html
   <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
   <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
   ```
4. Click **Save Changes**.
5. Click **Publish** (top-right) to apply across the site.

**MCP-assisted:**
```
mcp__claude_ai_Webflow__data_scripts_tool with action="list"
→ Verify GSAP + ScrollTrigger are present.

If missing:
mcp__claude_ai_Webflow__data_scripts_tool with action="add",
  url="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js",
  location="footer"
(Repeat for ScrollTrigger.)
```

**Verification:** load any page on the site, open DevTools console, type `typeof gsap`. Returns `"object"` if loaded correctly.

### 2. Set up the Webflow page

**Manual:**
1. Webflow Designer → **Pages panel** (left sidebar).
2. **+ Add new page** → set Slug, Title, parent folder, SEO metadata.
3. Save. The empty page is ready to import into.

**MCP-assisted:**
```
mcp__claude_ai_Webflow__data_pages_tool with action="create",
  slug="<page-slug>",
  title="<Page Title>",
  description="<SEO description, under 160 chars>"
```

---

## Per-import checklist

Run through these every time you import or re-import a page.

### Step 1 — If re-importing: DELETE the existing page first

**Critical for re-imports.** Re-importing without deleting leaves orphan classes from the old version, polluting the class manager.

**Manual:**
1. Pages panel → right-click the target page → **Delete page**.
2. Confirm. Webflow prunes classes that only lived on this page; site-wide classes (`.button`, `.section`) keep their existing rules unchanged.

**MCP-assisted:**
```
mcp__claude_ai_Webflow__data_pages_tool with action="delete",
  page_id="<page-id-from-list>"
```

After deletion, recreate the empty page (Step 2 of pre-import) with the same slug + SEO metadata.

### Step 2 — Open the converter

Navigate to **https://moden.club/tools/html-to-webflow** in your browser.

The converter has three tabs: **HTML**, **CSS**, **JS**.

### Step 3 — Paste each `.webflow.*` file into its tab

1. Open `pages/<slug>/_converter/<slug>.webflow.html` → copy entire contents → paste into the converter's **HTML** tab.
2. Open `pages/<slug>/_converter/<slug>.webflow.css` → copy entire contents → paste into the converter's **CSS** tab.
3. Open `pages/<slug>/_converter/<slug>.webflow.js` → copy entire contents → paste into the converter's **JS** tab.

### Step 4 — Convert + import to Webflow

The converter has a "Convert" button (or similar) — click it. The output should be a Webflow-compatible structure.

The converter typically gives you one of two flows:
- **Direct import:** the converter pushes the structure to Webflow via its API. Sign in with your Webflow credentials, select the project + page.
- **Copy structure:** copy the generated Webflow markup (looks like nested divs with attributes) and paste into Webflow Designer's canvas.

Follow whichever flow the converter uses. After import, you should see your structure rendered in the Webflow Designer canvas.

### Step 5 — Re-link images

Every `<img src="https://placehold.co/...">` in your source needs to be replaced with a Webflow Asset Manager URL.

**Manual:**
1. Webflow Designer → **Assets panel** (left sidebar) → drag-and-drop or click "+" to upload your real images.
2. For each image in the imported page:
   - Click the image in the canvas.
   - Right-side **Settings panel** → **Image Source** → click → select the uploaded asset.
3. Verify alt text is preserved.

**MCP-assisted:**
```
mcp__claude_ai_Webflow__asset_tool with action="upload",
  source_path="path/to/local-image.webp",
  alt_text="Descriptive alt text"

→ Returns the asset's Webflow URL.

Then update the image's src in Webflow (manual or via further MCP).
```

For batch uploads (e.g., 20+ images), MCP is significantly faster.

### Step 6 — Smoke-test in Designer canvas

Before publishing:

1. Scroll through the entire imported page in Designer.
2. Check:
   - [ ] No layout glitches (overlapping elements, broken grids).
   - [ ] Pill-shaped flex children aren't stretched (if they are, your `width: fit-content` rule didn't import — check).
   - [ ] Designer canvas scrolls smoothly (if laggy, your `inDesigner` guard isn't working — check the source).
   - [ ] All sections render at expected breakpoints (toggle Desktop / Tablet / Phone Landscape / Phone Portrait in Designer's top bar).
3. If anything looks off, edit the source files (NOT the `.webflow.*` outputs), re-run `_build.py`, and re-import (back to Step 1).

### Step 7 — Publish to staging

**Manual:**
1. Top-right **Publish** dropdown.
2. Select **Staging** (the `.webflow.io` URL).
3. Click **Publish to selected domains**.
4. Wait for confirmation.
5. Open the staging URL in a real browser (NOT inside Webflow Designer).
6. Smoke-test:
   - [ ] All animations fire correctly.
   - [ ] No console errors (check DevTools).
   - [ ] Internal links work.
   - [ ] Forms submit (if any).
   - [ ] Responsive design works on real devices (resize browser, or test on phone).

**MCP-assisted:** the existing `safe-publish` skill handles this with diff + confirmation. If installed, invoke it instead of manual publish.

### Step 8 — Re-link assets verification

On the published staging URL:

- [ ] All `<img>` elements load real images (no `placehold.co` URLs left).
- [ ] Image alt text is set in both source HTML AND Webflow Asset Manager metadata.
- [ ] No 404s in DevTools Network panel.

### Step 9 — Publish to production

Once staging is approved:

**Manual:**
1. Top-right **Publish** dropdown.
2. Select your custom domain.
3. Click **Publish to selected domains**.
4. Wait for confirmation.
5. Verify the production URL in a browser.

**MCP-assisted:** `safe-publish` skill, with the production domain selected. The skill shows a diff of what changed and requires explicit confirmation — useful for catching unintended changes.

---

## Post-import housekeeping

### Class manager check

Webflow → bottom-right **Style Manager** icon → **Classes** tab.

Look for:
- [ ] Your new prefixed classes (`acme-hero`, `acme-tool-card`, etc.) — should match what the build script emitted.
- [ ] No accidental duplication of existing site classes.
- [ ] No orphan classes from previous import attempts (if you forgot Step 1).

If you see orphans, the next re-import (with the page deleted first) will clear them.

### Save a Webflow Backup

After a successful import + publish:

1. Webflow Designer → **Project Settings** → **Backups** → **Create backup**.
2. Name it descriptively: "After <page-slug> page import — YYYY-MM-DD".

This is your rollback point if a future re-import breaks the page.

---

## When something goes wrong

### Symptom: imported page shows browser-default styling (black text, no padding)

Your CSS didn't import correctly. Likely cause: the `.webflow.css` had `var(--...)` references that the published site can't resolve (the `:root` block was stripped by the build, and the live site doesn't have those variables defined).

**Fix:** check the `.webflow.css` you pasted. Run `grep "var(--" path/to/<slug>.webflow.css`. If it returns anything, the build's sanity check should have caught it — re-run the build, paste the new output.

### Symptom: animations fire on every page including pages they shouldn't

Your `inDesigner` guard isn't gating the right things. Check the `.webflow.js` — `if (inDesigner) return;` should appear after the canvas inits but before GSAP setup. See [designer-canvas-fixes.md](designer-canvas-fixes.md).

### Symptom: animations don't fire at all on the published site

GSAP isn't loaded. Check Project Settings → Custom Code → Footer Code. Add the CDN tags. **Don't forget to publish project settings** for changes to take effect.

### Symptom: Class collision — a button on a different page changed colour

Your `.button` rule merged into the existing `.button`. **Add `button` and all its variants to `COLLIDE_RENAMES` in `_build.py`** — see [class-collisions.md](class-collisions.md). Rebuild, delete the imported page, re-import.

### Symptom: Designer canvas feels un-scrollable / laggy

Your `inDesigner` guard is missing or incorrect. ScrollTrigger animations are fighting Webflow's iframe scroll model. Check [designer-canvas-fixes.md](designer-canvas-fixes.md) and add the guard.

### Symptom: Mobile (479px) shows a thin gap on the right edge

`body { overflow-x: hidden }` is missing from your `base.css`. Add it. Rebuild. Re-import.

### Symptom: Re-import duplicated classes — class manager has `tool-card`, `tool-card-2`, `tool-card-3`

You forgot to delete the page in Webflow before re-importing. Webflow auto-suffixes new classes if a name conflict is detected. **Delete the page and the duplicate classes**, then re-import cleanly. The duplicate classes can be removed via Class Manager (right-click → delete) once nothing references them.

---

## Reference: when MCP isn't connected

If Webflow MCP tools aren't available in the user's session, every step above falls back to manual Designer actions. The flow is identical; the user clicks instead of you tool-calling.

Tell the user this up-front so they're not surprised by manual work.
