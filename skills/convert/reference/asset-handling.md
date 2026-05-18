# Asset handling

The build script doesn't transform image / video / file paths. Whatever `<img src="…">` you have in source is exactly what gets imported. This file explains the workflow that handles this cleanly.

---

## During authoring: use `placehold.co`

For every `<img>` in source HTML, use a `placehold.co` placeholder URL:

```html
<img src="https://placehold.co/640x640/1f1f1f/FF4F41?text=Hero" alt="Description">
```

Format: `https://placehold.co/<width>x<height>/<bg-color-hex>/<fg-color-hex>?text=<label>`

Why placeholders during authoring:

1. **No 404s in local browser preview.** The placeholder URL is reachable from anywhere.
2. **No relative-path breakage when imported into Webflow.** The Webflow-hosted page can fetch from `placehold.co`.
3. **Visual signal during QA.** Anyone reviewing the staged page can immediately see "this image is a placeholder, replace before publish."
4. **Works during section-by-section authoring.** You don't have to gather final assets before iterating on layout.

---

## After Webflow import: re-link to Asset Manager

Once the page is imported into Webflow, **before publishing to production**:

1. Upload the real images to Webflow's Asset Manager:
   - Webflow Designer → **Assets panel** (left sidebar) → drag-and-drop or click "+" to upload.
   - Or use `mcp__claude_ai_Webflow__asset_tool` programmatically.

2. For each `<img>` in the imported page:
   - Click the image in Webflow Designer.
   - In the right-side **Settings panel** → Image Source → click the URL field → select the uploaded asset from Asset Manager.

3. Verify alt text is preserved from your source HTML. (The converter keeps `alt=""` attributes intact, but double-check on critical images.)

4. **Test responsive image variants.** Webflow auto-generates responsive image sizes when you upload to Asset Manager. The placeholders had a single size; uploaded assets adapt.

---

## Local preview during authoring

If you want the local browser preview to show real images (not placeholders), use a relative path to a local asset directory:

```html
<img src="../assets/hero.webp" alt="Hero">
```

Where `assets/` lives at the project root (sibling to `pages/`).

**Don't commit this for the Webflow-bound bundle** — relative paths break when imported. Either:

- Switch to placeholder URLs *before* running the build, OR
- Use a build flag / config to swap real paths for placeholders at export time (this is custom; not in the default `_build.py`).

The simplest workflow: keep `placehold.co` URLs in source; preview shows placeholders too. Trade-off: local preview doesn't show real assets, but you can always check the asset directly in a separate browser tab while authoring.

---

## Reference example: live site export images

If you have a Webflow site export at `Webflow code/<site-name>.webflow/`, the export includes the images in `<site-name>.webflow/images/`. For local preview, you can reference those:

```html
<img src="../../Webflow code/<site-name>.webflow/images/hero.webp" alt="Hero">
```

This lets you preview with real assets locally without uploading anything new.

**For the Webflow-bound bundle**, switch to `placehold.co` placeholders before running the build. The build script doesn't transform `<img src>` so whatever's in source is what gets imported.

---

## MCP-assisted asset upload

If `mcp__claude_ai_Webflow__asset_tool` is available, you can upload assets programmatically:

```
1. List existing site assets (avoid duplicates):
   mcp__claude_ai_Webflow__asset_tool with action="list"

2. Upload new asset:
   mcp__claude_ai_Webflow__asset_tool with action="upload",
   source_path="local/path/to/hero.webp",
   alt_text="Hero image — students at graduation"

3. Get the uploaded asset's Webflow URL.

4. Use the URL as the new <img src> in the imported page (manually or via further MCP calls).
```

This is faster for batch uploads (e.g., 20 images for a new page) than dragging each one into the Asset Manager.

If MCP isn't connected, fall back to the manual Designer flow.

---

## Image format recommendations

| Format     | Use for                                          | Notes                                                                    |
| ---------- | ------------------------------------------------ | ------------------------------------------------------------------------ |
| **WebP**   | Photos, illustrations                            | Smallest file size at high quality. Webflow auto-serves modern formats.  |
| **AVIF**   | Photos (highest compression)                     | Even smaller than WebP. Browser support is broad now.                    |
| **SVG**    | Logos, icons, decorative shapes                  | Vector → infinitely scalable. Inline `<svg>` is even better than `<img src="*.svg">` for small icons. |
| **PNG**    | Transparency-heavy graphics, screenshots         | Use sparingly; WebP usually wins.                                        |
| **JPEG**   | Legacy support only                              | WebP is strictly better.                                                 |

Webflow's Asset Manager will accept any of these. For best published-site performance, prefer WebP or AVIF.

---

## SVG tip: inline vs `<img>`

For decorative or icon SVGs that need to inherit `currentColor` from CSS (so they match text colour, change on hover, etc.), inline them as `<svg>` directly in HTML — don't use `<img src="*.svg">`:

```html
<button class="button">
  <span class="button_label">Download</span>
  <svg class="button_icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
    <polyline points="7 10 12 15 17 10"/>
    <line x1="12" x2="12" y1="15" y2="3"/>
  </svg>
</button>
```

`stroke="currentColor"` makes the icon inherit the button's text colour. `<img src="icon.svg">` cannot do this — the SVG has its own context and ignores the parent's CSS.

The converter preserves inline SVG verbatim. No special handling needed.

---

## Don't forget alt text

For every meaningful image:

```html
<img src="..." alt="Hand holding a magnifying glass over an enrollment analytics dashboard">
```

For purely decorative images (background patterns, abstract shapes that add no semantic content):

```html
<img src="..." alt="" role="presentation">
```

Webflow's Asset Manager has its own alt text field too — **set it both in source HTML and in Asset Manager**. They're separate metadata stores; missing one means screen readers / SEO bots see only what's in the other.

---

## Pre-publish asset checklist

Before going live:

- [ ] Every `<img>` references a real Webflow asset (no `placehold.co` URLs left).
- [ ] Every `<img>` has alt text in the HTML AND in the Webflow Asset Manager.
- [ ] All assets are WebP / AVIF / SVG (no large JPEG/PNG).
- [ ] No assets larger than 500KB unless absolutely needed.
- [ ] Hero image has `loading="eager"` (and `decoding="async"`); below-fold images have `loading="lazy"`.

The skill's `templates/page-template.html` doesn't enforce loading strategy — set it explicitly based on whether the image is hero (visible without scrolling) or below-fold.
