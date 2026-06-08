/* =============================================
   <PAGE_SLUG> — page-specific JS (Lumos v2 project)
   GSAP + ScrollTrigger driven animations.
   Loaded after gsap.min.js and ScrollTrigger.min.js (added to Webflow's
   Project Settings → Custom Code → Footer Code).
   Source stays as a plain IIFE — the build script wraps it in
   window.Webflow.push(...) on export.

   Lumos note: target component classes (e.g. ".hero_title"), not u-* utilities.
   A combo class a toggle adds at runtime (e.g. ".is-active") must already
   exist somewhere in the page HTML, or Webflow purges it on import — seed it
   in a `[component]_hidden u-display-none` div. See reference/frameworks/lumos.md.
   ============================================= */

(function () {
  // `inDesigner` is always false locally (no Webflow runtime). The build
  // script wraps this IIFE in Webflow.push when emitting the .webflow bundle,
  // so the Webflow runtime is guaranteed to be loaded by the time it runs.
  var inDesigner = (typeof Webflow !== "undefined" &&
                    Webflow.env &&
                    Webflow.env("design"));

  // In Designer: skip all GSAP scroll-driven animations. The Designer canvas's
  // iframe scroll model + many installed ScrollTriggers cause the visible
  // outline to drift out of sync with the underlying scroll position.
  if (inDesigner) return;

  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);


  /* =========================================
     SECTION 1 — HERO
     ========================================= */

  // Example:
  // gsap.from(".hero_title", { opacity: 0, y: 20, duration: 0.5 });

})();
