/* =============================================
   inDesigner Canvas Guard — copy-pasteable snippet

   The single most important Webflow Designer fix. Drop this at the top of
   your page IIFE and gate scroll-driven animations + canvas rAF loops with
   the `inDesigner` boolean. See reference/designer-canvas-fixes.md for
   the full rationale.

   Why this works:
   - `Webflow.env("design")` is the Webflow runtime's official "are we in
     the Designer?" check.
   - Local browser preview has no Webflow runtime, so inDesigner is false.
     Local preview gets full animations.
   - The published site loads the runtime but Webflow.env("design") returns
     falsy, so inDesigner is false. Published site gets full animations.
   - Only inside the Designer canvas iframe does Webflow.env("design")
     return truthy. Designer gets simplified static behaviour.
   ============================================= */

(function () {

  // ===== 1. Detect Designer mode =========================================
  var inDesigner = (typeof Webflow !== "undefined" &&
                    Webflow.env &&
                    Webflow.env("design"));


  // ===== 2. Initialise canvas effects (static frame in Designer) =========
  // Pass `inDesigner` to each canvas-init function. Inside the function:
  //
  //   var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  //   var staticFrame = reduce || inDesigner;
  //   if (staticFrame) {
  //     drawOnce();           // single frozen frame
  //   } else {
  //     loopWithRAF();        // animated
  //   }
  //
  // Also skip mouse listeners in Designer:
  //   if (!staticFrame) host.addEventListener("mousemove", ...);

  initHeroCanvas(inDesigner);
  initBackgroundCanvas(inDesigner);


  // ===== 3. Skip ScrollTrigger entirely in Designer ======================
  if (inDesigner) return;


  // ===== 4. Bail if GSAP isn't loaded or user prefers reduced motion =====
  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  gsap.registerPlugin(ScrollTrigger);


  // ===== 5. Your scroll-driven animations live below =====================

  // Entrance animations (forgiving, ScrollTrigger handles them well):
  gsap.from(".hero_eyebrow", {
    opacity: 0, y: 20, duration: 0.5,
    scrollTrigger: { trigger: ".hero-section", start: "top 80%" },
  });

  // Refresh entrance triggers as images / fonts settle:
  function refreshEntrances() {
    if (typeof ScrollTrigger !== "undefined") ScrollTrigger.refresh();
  }
  document.querySelectorAll(".your-image-class").forEach(function (img) {
    if (img.complete) return;
    img.addEventListener("load", refreshEntrances, { once: true });
    img.addEventListener("error", refreshEntrances, { once: true });
  });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(refreshEntrances);
  }

  // Scrub-style scroll progress: use a custom rAF-throttled scroll listener,
  // NOT ScrollTrigger.scrub. See reference/designer-canvas-fixes.md fix #5.
  // (Stub — adapt for your specific element.)
  /*
  var progressEl = document.querySelector(".timeline-progress");
  var wrapEl = document.querySelector(".timeline-wrap");
  if (progressEl && wrapEl) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var rect = wrapEl.getBoundingClientRect();
      var center = window.innerHeight * 0.5;
      var p = (center - rect.top) / rect.height;
      if (p < 0) p = 0;
      else if (p > 1) p = 1;
      progressEl.style.height = (p * 100).toFixed(2) + "%";
    };
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }
  */

})();


/* =============================================
   Example canvas init — paste-and-adapt
   ============================================= */

function initHeroCanvas(inDesigner) {
  var canvas = document.querySelector(".hero_canvas");
  if (!canvas) return;
  var ctx = canvas.getContext("2d");

  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var staticFrame = reduce || inDesigner;

  function resize() {
    var dpr = window.devicePixelRatio || 1;
    var rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.scale(dpr, dpr);
  }
  resize();
  window.addEventListener("resize", resize);

  function draw(t) {
    var rect = canvas.getBoundingClientRect();
    ctx.clearRect(0, 0, rect.width, rect.height);
    // ... your drawing logic ...
  }

  if (staticFrame) {
    draw(0);
  } else {
    var loop = function (t) {
      draw(t);
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }

  // Pause when fully off-screen so the rAF doesn't burn cycles.
  if (!staticFrame && "IntersectionObserver" in window) {
    var running = true;
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
  }
}

function initBackgroundCanvas(inDesigner) {
  // Same pattern as initHeroCanvas — adapt as needed.
}
