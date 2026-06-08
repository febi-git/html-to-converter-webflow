/* =============================================
   <PAGE_SLUG> — page-specific JS (Client-First project)
   GSAP + ScrollTrigger driven animations.
   Loaded after gsap.min.js and ScrollTrigger.min.js (added to Webflow's
   Project Settings → Custom Code → Footer Code).
   Source stays as a plain IIFE — the build script wraps it in
   window.Webflow.push(...) on export.

   Client-First note: target custom classes (e.g. ".hero_eyebrow") rather than
   shared utilities you don't own. See reference/frameworks/client-first.md.
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
  // gsap.from(".hero_eyebrow", { opacity: 0, y: 20, duration: 0.5 });

})();
