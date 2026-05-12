# Webflow runtime integration

The published Webflow site loads its own JS runtime (`webflow.js`) on every page. Your page-level code has to coexist with it. This file covers the four things that always need to be true.

---

## 1. GSAP + ScrollTrigger via Webflow's Footer Code

If your code uses GSAP (and most of this skill's animation patterns do), GSAP and ScrollTrigger have to be loaded *before* your page IIFE runs.

**Where to add the CDN:**

Webflow Designer → **Project Settings → Custom Code → Footer Code** (NOT Head Code) →

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

**Save and publish** the project settings. This is a one-time per-site step. After it's done, every page on the site has GSAP + ScrollTrigger available.

**Why Footer Code (not Head):** scripts in `<head>` block rendering. Animation libraries don't need to run before paint, so footer is faster. Webflow's runtime initialises after these scripts load.

**MCP equivalent:** if `mcp__claude_ai_Webflow__data_scripts_tool` is available, you can verify or register these scripts programmatically. See [webflow-designer-checklist.md](webflow-designer-checklist.md).

---

## 2. Page JS via `Webflow.push()`

Webflow's runtime initialises its DOM listeners, class toggles, and built-in animations at runtime. If your JS runs before that, selectors may not exist, or Webflow's own behaviour may overwrite yours.

**The convention:** wrap page JS in `Webflow.push()` so it executes after the Webflow runtime is ready.

**In source code, write a plain IIFE:**

```js
(function () {
  // your page code
})();
```

**The build script transforms this into:**

```js
window.Webflow = window.Webflow || [];
window.Webflow.push(function () {
  // your page code
});
```

The `window.Webflow = window.Webflow || []` is a defensive shim — it handles the rare case where your script loads *before* Webflow's runtime, by treating the `Webflow` global as a queue. When Webflow's runtime loads, it processes the queue.

**Don't hand-write `Webflow.push()` in source.** It would break local browser preview (no `Webflow` global locally) and the build script would double-wrap. Keep source as a plain IIFE.

The transformation is in `build_js()` of [templates/_build.py](../templates/_build.py).

---

## 3. `body { overflow-x: hidden }` mobile safety

**The bug:** Webflow's mobile breakpoints (especially the 479px range) sometimes show a thin horizontal gap on the right edge of the viewport — sub-pixel rounding errors in Webflow's responsive grid system.

**The fix:** add to your `base.css` reset:

```css
body {
  overflow-x: hidden;
}
```

That's it. The `<body>` clips the sub-pixel overflow, and the user never sees the thin gap.

**Why this is in the reset:** it's defensive. Even if no current section overflows horizontally, future ones might (a wide hero animation, a padded canvas), and you don't want to retrofit the fix later.

**When NOT to use:** if your design legitimately needs horizontal scroll (a horizontal-scrolling timeline section, for example), you'll need to scope the fix differently — `overflow-x: hidden` on the body would break it. In that case, wrap the rest of the page in a container with the fix, and let the horizontal-scroll section stand alone.

---

## 4. `Webflow.env("design")` for Designer detection

The Webflow runtime exposes `Webflow.env(key)` to identify the environment. Two keys matter:

- `Webflow.env("design")` → truthy inside the Designer canvas iframe; falsy on the published site.
- `Webflow.env("preview")` → truthy in Webflow's preview mode (the eye icon → Preview); falsy elsewhere.

**Use `Webflow.env("design")`** to short-circuit animations / scroll listeners that break the Designer canvas. See [designer-canvas-fixes.md](designer-canvas-fixes.md).

**Don't use `Webflow.env("preview")`** for anything load-bearing — preview mode behaves like the published site for almost everything, and the user expects "what I see in Preview = what visitors see."

---

## Putting it together

A correctly-set-up Webflow project has:

1. ✅ GSAP + ScrollTrigger CDN tags in **Footer Code**, published.
2. ✅ Each page's `.webflow.js` wrapped in `Webflow.push()` (verify in the converter output).
3. ✅ `body { overflow-x: hidden }` in the reset (`base.css`).
4. ✅ Page-level JS gated with `inDesigner` checks (see [designer-canvas-fixes.md](designer-canvas-fixes.md)).

If any of these is missing on the published site, expect:

| Missing                              | Symptom                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| GSAP CDN in Footer                   | Animations fail silently; your IIFE bails on `typeof gsap === "undefined"`.   |
| `Webflow.push()` wrapper             | Selectors return null; first-page-load animations don't fire.                 |
| `overflow-x: hidden`                 | Thin horizontal gap on mobile breakpoints, especially 479px.                  |
| `inDesigner` guard                   | Designer canvas feels un-scrollable; clients can't edit other elements.       |

---

## Things you should NOT do

- **Don't add `<script>` tags in your source HTML for GSAP.** Use Webflow's Footer Code (one place per site, not per page).
- **Don't wrap source code in `Webflow.push()` manually.** Build script does it. Manual wrapping breaks local browser preview.
- **Don't use `DOMContentLoaded` or `window.onload` instead of `Webflow.push()`.** Those fire before Webflow's runtime is fully initialised — selectors might exist but Webflow-managed classes won't have settled yet.
- **Don't depend on `jQuery` being available** unless you've explicitly added it to Footer Code. Webflow's runtime uses jQuery internally but doesn't expose it as a global by default.
