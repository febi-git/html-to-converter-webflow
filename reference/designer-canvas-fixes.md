# Webflow Designer canvas fixes

Webflow has two environments where your code runs: **Designer canvas** (the iframe inside the Webflow editor) and **the published site** (what visitors see). They behave differently in subtle ways. These fixes solve the cases where Designer is broken even though the published site works fine — usually the Designer is the problem, not the user's code.

---

## Fix 1 — The `inDesigner` guard (most important)

**Problem:** Scrub-based ScrollTrigger animations break the Webflow Designer canvas. The Designer's iframe scroll model + many installed ScrollTriggers cause the visible outline to drift out of sync with the underlying scroll position. The page feels un-scrollable.

**Solution:** Detect Designer mode at the top of every page IIFE and short-circuit scroll-driven animations:

```js
(function () {
  // True only inside the Webflow Designer canvas. False in local browser preview
  // (no Webflow runtime) and false on the published site (Webflow.env returns
  // "publish" or undefined, never "design").
  var inDesigner = (typeof Webflow !== "undefined" &&
                    Webflow.env &&
                    Webflow.env("design"));

  // Background canvases run independently of GSAP. Each renders a single static
  // frame when prefers-reduced-motion is set OR when running in the Webflow
  // Designer canvas; otherwise loops via rAF.
  initHeroWave(inDesigner);
  initHowTwinkle(inDesigner);

  // In Designer: skip all GSAP scroll-driven animations. Elements stay in
  // their natural HTML/CSS state — no "magically appearing" scroll reveals,
  // but the canvas remains usable.
  if (inDesigner) return;

  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);

  // ... your animations here
})();
```

**Why this works:**
- `Webflow.env("design")` is the Webflow runtime's official "are we in the Designer?" check.
- The local browser preview has no Webflow runtime, so `typeof Webflow !== "undefined"` is `false` → `inDesigner` is `false`. Local preview gets full animations.
- The published site loads the Webflow runtime but `Webflow.env("design")` returns falsy → `inDesigner` is `false`. Published site gets full animations.
- Only inside the Designer canvas iframe does `Webflow.env("design")` return truthy → `inDesigner` is `true`. ScrollTrigger gets bypassed.

The canonical snippet is in [templates/inDesigner-canvas-snippet.js](../templates/inDesigner-canvas-snippet.js), ready to copy-paste.

---

## Fix 2 — Static-frame canvas rendering in Designer

**Problem:** Background `<canvas>` animations driven by `requestAnimationFrame` cause the Designer canvas to lag heavily — the rAF loop competes with Webflow's own selection / overlay logic.

**Solution:** Inside each canvas-init function, render exactly one frame in Designer mode and skip the rAF loop:

```js
function initHeroWave(inDesigner) {
  var canvas = document.querySelector(".hero_canvas");
  if (!canvas) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var staticFrame = reduce || inDesigner;

  // ... canvas setup ...

  function draw(t) {
    // ... drawing logic ...
  }

  if (staticFrame) {
    draw(0);  // single frame, frozen at t=0
  } else {
    var loop = function (t) {
      draw(t);
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }
}
```

**Why this works:** A single static frame renders the canvas's "representative state" (whatever t=0 looks like). It still shows in the Designer so the user can see the visual, but nothing animates.

---

## Fix 3 — Skip mouse listeners in Designer

**Problem:** Mouse listeners for cursor-following effects (e.g., a CTA box's wave that follows the cursor) fight Webflow Designer's selection overlay. Clicks register as canvas events instead of Designer selections.

**Solution:** Wrap mouse listener setup in `if (!staticFrame)`:

```js
function initCtaBoxWave(inDesigner) {
  var host = document.querySelector(".cta-box");
  if (!host) return;

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var staticFrame = reduce || inDesigner;

  if (!staticFrame) {
    // Skip mouse listeners in Designer — they'd fight the selection overlay
    // and there's no rAF loop to consume the targetX/Y anyway.
    host.addEventListener("mousemove", onMouseMove);
    host.addEventListener("mouseleave", onMouseLeave);
  }

  // ... draw logic
}
```

---

## Fix 4 — `width: fit-content` for inline-flex children

**Problem:** Webflow Designer canvas applies an implicit `align-self: stretch` to flex children, ignoring `inline-flex`'s content-width sizing. A pill-shaped status badge that should be 60px wide gets stretched to fill the parent column in the Designer.

**Solution:** Pin `width: fit-content` on the affected children:

```css
.tool-card_status {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.1875rem 0.5625rem;
  border-radius: 0.25rem;
  flex-shrink: 0;
  /* Webflow Designer canvas applies an implicit `align-self: stretch` to flex
     children, ignoring inline-flex's content width. Pinning fit-content keeps
     the pill tight in Designer; published browsers behave the same. */
  width: fit-content;
}
```

**Why this works:** `width: fit-content` overrides the implicit stretch and forces the element to size to its content, both in Designer and in published browsers. Published browsers don't *need* this fix (they respect inline-flex), but it doesn't hurt them either.

**When to apply:** Any flex child whose width should be content-determined (badges, pills, chips, icon containers, inline buttons inside a flex container).

---

## Fix 5 — Custom scroll listener instead of ScrollTrigger.scrub

**Problem:** ScrollTrigger captures pixel positions at trigger-creation time. On a cold load, fonts/images settle just *after* the trigger is created. A scrub trigger born into a stale layout doesn't recover cleanly via `.refresh()` — first-load and reload behave differently.

**Solution:** For scrub-style effects (progress bars, parallax, anything tied to scroll position), use a plain rAF-throttled scroll listener instead of ScrollTrigger:

```js
var progressEl = document.querySelector(".how_process_timeline-progress");
var wrapEl = document.querySelector(".how_process_wrap");

if (progressEl && wrapEl) {
  if (inDesigner) {
    // Designer: pre-fill so the section reads correctly without binding a
    // scroll listener to the laggy designer canvas.
    progressEl.style.height = "100%";
  } else {
    var ticking = false;
    var updateTimelineProgress = function () {
      ticking = false;
      var rect = wrapEl.getBoundingClientRect();
      var center = window.innerHeight * 0.5;
      var p = (center - rect.top) / rect.height;
      if (p < 0) p = 0;
      else if (p > 1) p = 1;
      progressEl.style.height = (p * 100).toFixed(2) + "%";
    };
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(updateTimelineProgress);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    updateTimelineProgress();
  }
}
```

**Why this works:** Reading layout each scroll frame side-steps the race — the math is always against the *current* DOM, so first-load and reload behave identically.

**When to use:** Any time you'd reach for `scrollTrigger: { scrub: true }` or `scrub: <number>`. For entrance animations (fade-in-on-scroll), stick with ScrollTrigger — those are forgiving and `.refresh()` works.

---

## Fix 6 — Refresh entrance ScrollTriggers on image / font load

**Problem:** Entrance ScrollTriggers (`start: "top 80%"`) are forgiving but still capture position at creation. If images haven't loaded yet, the trigger fires too early.

**Solution:** Refresh ScrollTrigger after images load and fonts settle:

```js
function refreshEntrances() {
  if (typeof ScrollTrigger !== "undefined") ScrollTrigger.refresh();
}

document.querySelectorAll(".your-image-class").forEach((img) => {
  if (img.complete) return;
  img.addEventListener("load", refreshEntrances, { once: true });
  img.addEventListener("error", refreshEntrances, { once: true });
});

if (document.fonts && document.fonts.ready) {
  document.fonts.ready.then(refreshEntrances);
}
```

**Why this works:** Entrance triggers (`start: "top 80%"`) tolerate post-creation `.refresh()` calls. Scrub triggers don't (use Fix 5 for those).

---

## Fix 7 — IntersectionObserver pause for off-screen canvases

**Problem:** An always-running rAF canvas burns CPU/GPU even when the user has scrolled past it.

**Solution:** Pause the rAF loop when the canvas is fully off-screen:

```js
var observer = new IntersectionObserver(function (entries) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting && !running) {
      running = true;
      requestAnimationFrame(loop);
    } else if (!entry.isIntersecting && running) {
      running = false;
    }
  });
});
observer.observe(canvas);
```

**Why this matters:** A 2500px-tall section with a canvas at the top will keep its rAF firing while the user reads the bottom of the page. Pausing saves battery on laptops and mobile.

---

## When in doubt

If a section behaves differently in Designer vs published, the root cause is usually one of:

1. ScrollTrigger scrub / pin fighting the Designer's iframe scroll model.
2. Inline-flex children stretching due to implicit `align-self: stretch`.
3. Mouse listeners colliding with the Designer's selection overlay.
4. Animation rAF loops competing with Designer's own rAF.

Apply the matching fix above. Don't try to override Webflow's Designer behaviour — it changes between releases. The fixes above are stable because they bypass Designer-specific behaviour rather than fighting it.
