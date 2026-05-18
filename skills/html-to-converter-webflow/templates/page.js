/* =============================================
   <PAGE_SLUG> — page-specific JS
   GSAP + ScrollTrigger driven animations.
   Loaded after gsap.min.js and ScrollTrigger.min.js (added to Webflow's
   Project Settings → Custom Code → Footer Code).
   Source stays as a plain IIFE — the build script wraps it in
   window.Webflow.push(...) on export.
   ============================================= */

(function () {
  // `inDesigner` is always false locally (no Webflow runtime). The build
  // script wraps this IIFE in Webflow.push when emitting the .webflow bundle,
  // so the Webflow runtime is guaranteed to be loaded by the time it runs.
  var inDesigner = (typeof Webflow !== "undefined" &&
                    Webflow.env &&
                    Webflow.env("design"));

  // Background canvases / heavy effects: each renders a single static
  // frame when prefers-reduced-motion is set OR when running in the Webflow
  // Designer canvas; otherwise loops via rAF.
  // Example: initHeroCanvas(inDesigner);

  // In Designer: skip all GSAP scroll-driven animations. The Designer canvas's
  // iframe scroll model + many installed ScrollTriggers cause the visible
  // outline to drift out of sync with the underlying scroll position, making
  // the page feel un-scrollable. Elements stay in their natural HTML/CSS state.
  if (inDesigner) return;

  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);


  /* =========================================
     SECTION 1 — HERO
     Add entrance animations here as needed.
     ========================================= */

  // Example:
  // gsap.from(".hero_eyebrow", { opacity: 0, y: 20, duration: 0.5 });

})();
