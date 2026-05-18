"""
Build a Webflow-ready bundle from hand-coded HTML/CSS/JS.

Pipeline:
  pages/<slug>/index.html  ─┐
  pages/<slug>/<slug>.css   ┤
  pages/<slug>/<slug>.js    ┤   →  pages/<slug>/_converter/<slug>.webflow.{html,css,js}
  pages/_shared/tokens.css  │       (paste these three into the converter at
  pages/_shared/base.css    │        https://moden.club/tools/html-to-webflow)
  pages/_shared/components.css┘

Steps:
  1. Extract <body> content from the source HTML; drop empty navbar/footer
     placeholders and <script> tags (those go in Webflow's Footer Code).
  2. Concatenate _shared CSS (tokens → base → components) + page CSS, with
     any @import lines (e.g. Google Fonts) promoted to the top.
  3. Read source JS (plain IIFE form).
  4. CSS: drop the :root token block, then inline EVERY var(--...) ref as a
     literal hex / value (so Webflow's color picker treats imported colors as
     standalone editable swatches rather than variable references).
  5. HTML + CSS + JS: prefix every class in COLLIDE_RENAMES with PREFIX so the
     import doesn't merge into existing live-site classes.
  6. JS: swap the outer `(function(){...})()` IIFE for
     `window.Webflow.push(function(){...})` so it runs after Webflow init.
  7. Sanity check: zero var(--...) refs may remain in the output CSS.

Run:  python pages/<slug>/_converter/_build.py
"""
import re
import os
import sys


# ===========================================================================
# === PROJECT CONFIG — fill these in for your project =======================
# ===========================================================================

# Page slug — the folder name under pages/. Output files are named <slug>.webflow.*
PAGE_SLUG = ""  # e.g. "home", "about", "pricing"

# Class-name prefix added to colliding classes. Keep it short (2–5 chars + dash).
# Examples: "acme-", "b3-", "site-"
PREFIX = "acme-"

# Class names that COLLIDE with the target Webflow site.
# Detection: grep the site's exported CSS for `^\.<name>(\s|\.|,|\{)`.
# Add the block name AND every element of the block (block_element_*).
COLLIDE_RENAMES = [
    # e.g. "container", "section", "section_dark", "button", "button_outline",
    # "hero", "hero_eyebrow", "hero_headline", "hero_subheadline",
]

# CSS custom property → literal value map. Leave EMPTY to auto-populate from
# tokens.css. Override only when a per-export literal differs from tokens.css.
VAR_TO_LITERAL = {}

# Optional: @import URLs to promote to the top of the generated CSS.
# Leave empty to auto-extract from base.css / tokens.css.
EXTRA_IMPORTS = []


# ===========================================================================
# === Path resolution (rarely needs editing) ================================
# ===========================================================================

PAGE_DIR     = os.path.dirname(os.path.abspath(__file__))             # pages/<slug>/_converter/
SRC_DIR      = os.path.dirname(PAGE_DIR)                              # pages/<slug>/
PROJECT_ROOT = os.path.dirname(os.path.dirname(SRC_DIR))               # repo root
SHARED_DIR   = os.path.join(SRC_DIR, "..", "_shared")

SRC_HTML = os.path.join(SRC_DIR, "index.html")
SRC_CSS  = os.path.join(SRC_DIR, f"{PAGE_SLUG}.css")
SRC_JS   = os.path.join(SRC_DIR, f"{PAGE_SLUG}.js")

DST_HTML = os.path.join(PAGE_DIR, f"{PAGE_SLUG}.webflow.html")
DST_CSS  = os.path.join(PAGE_DIR, f"{PAGE_SLUG}.webflow.css")
DST_JS   = os.path.join(PAGE_DIR, f"{PAGE_SLUG}.webflow.js")

TOKENS_CSS_PATH     = os.path.join(SHARED_DIR, "tokens.css")
BASE_CSS_PATH       = os.path.join(SHARED_DIR, "base.css")
COMPONENTS_CSS_PATH = os.path.join(SHARED_DIR, "components.css")


# ===========================================================================
# === Helpers ===============================================================
# ===========================================================================

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def parse_tokens_css(path):
    """Extract every `--name: value;` declaration from `:root { ... }` in
    tokens.css and return a {var(--name): value} map. Resolves single-level
    semantic shortcuts like `--color-text: var(--color-black)` to their final
    literal so the output never contains a leftover var() ref."""
    if not os.path.exists(path):
        return {}

    raw = _read(path)
    root_match = re.search(r":root\s*\{(.*?)\}", raw, flags=re.DOTALL)
    if not root_match:
        return {}

    body = root_match.group(1)
    decls = {}
    for m in re.finditer(
        r"--([a-zA-Z0-9_-]+)\s*:\s*([^;]+?)\s*;",
        body,
    ):
        name = m.group(1).strip()
        value = m.group(2).strip()
        decls[name] = value

    # Resolve var(--other-name) references one level deep.
    resolved = {}
    for name, value in decls.items():
        ref = re.match(r"^var\(--([a-zA-Z0-9_-]+)\)$", value)
        if ref and ref.group(1) in decls:
            resolved[f"var(--{name})"] = decls[ref.group(1)]
        else:
            resolved[f"var(--{name})"] = value

    return resolved


def _build_rename_map():
    return {n: PREFIX + n for n in COLLIDE_RENAMES}


def _apply_class_renames_in_attr(text, rename_map):
    """Rename matching class tokens inside class="..." attributes."""
    def repl(m):
        quote = m.group(1)
        tokens = m.group(2).split()
        return "class=" + quote + " ".join(rename_map.get(t, t) for t in tokens) + quote
    return re.sub(r'class=(["\'])([^"\']*)\1', repl, text)


def _apply_class_renames_in_selectors(text, rename_map):
    """Rename `.classname` occurrences (CSS selectors / JS string selectors).

    Sort longest-first so `.section_large` is matched before `.section`. The
    trailing boundary `(?![_\\-a-zA-Z0-9])` ensures we don't eat the prefix
    of a longer name we haven't already renamed."""
    for name in sorted(rename_map.keys(), key=len, reverse=True):
        pattern = r"\." + re.escape(name) + r"(?![_\-a-zA-Z0-9])"
        text = re.sub(pattern, "." + rename_map[name], text)
    return text


# ===========================================================================
# === Pipeline steps ========================================================
# ===========================================================================

def build_html(rename_map):
    raw = _read(SRC_HTML)

    # Extract <body>...</body>
    m = re.search(r"<body[^>]*>(.*?)</body>", raw, flags=re.DOTALL | re.IGNORECASE)
    if not m:
        raise SystemExit("Could not find <body>...</body> in source HTML.")
    body = m.group(1)

    # Strip empty navbar/footer placeholders + any <script> tags (those are
    # added in Webflow's Custom Code panel, not in the page markup).
    body = re.sub(r"<header class=\"site-nav\">.*?</header>", "", body, flags=re.DOTALL)
    body = re.sub(r"<footer class=\"site-footer\">.*?</footer>", "", body, flags=re.DOTALL)
    body = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.DOTALL | re.IGNORECASE)

    # Strip the comment blocks for nav/footer/scripts that are now empty noise.
    body = re.sub(
        r"<!-- ={5,}\s*\n\s*(NAVBAR|FOOTER|Scripts)[^\n]*\n.*?={5,} -->",
        "", body, flags=re.DOTALL,
    )

    body = body.strip() + "\n"

    header = (
        "<!-- =============================================\n"
        f"     {PAGE_SLUG.upper()} - generated by _build.py\n"
        "     Paste into the HTML tab of the Modern HTML to Webflow Converter\n"
        "     (https://moden.club/tools/html-to-webflow).\n"
        "     Body markup only. CSS goes in the CSS tab. JS in the JS tab.\n"
        "     Do not edit by hand - re-run the build script after changing source.\n"
        "     ============================================= -->\n\n"
    )

    out = header + _apply_class_renames_in_attr(body, rename_map)
    _write(DST_HTML, out)


def build_css(var_map, rename_map):
    # Bundle order: tokens -> base -> shared components -> page CSS.
    parts = []
    for path in (TOKENS_CSS_PATH, BASE_CSS_PATH, COMPONENTS_CSS_PATH):
        if os.path.exists(path):
            parts.append(_read(path))
    if os.path.exists(SRC_CSS):
        parts.append(_read(SRC_CSS))
    bundled = "\n\n".join(parts)

    # Pull out @import lines (e.g. Google Fonts in base.css) and EXTRA_IMPORTS.
    # @import must precede other rules to be valid, so we put them at the top.
    imports = re.findall(r"^\s*@import[^;]+;\s*$", bundled, flags=re.MULTILINE)
    bundled = re.sub(r"^\s*@import[^;]+;\s*$\n?", "", bundled, flags=re.MULTILINE)
    for extra in EXTRA_IMPORTS:
        if extra not in imports:
            imports.append(extra)

    # Drop the entire :root token block - the live site (or future
    # imports) defines variables; duplicating them under different names
    # just clutters the Webflow class panel.
    bundled = re.sub(r":root\s*\{[^}]*\}\s*", "", bundled, count=1)

    # Inline every var(--...) ref as a literal hex / value.
    for k, v in var_map.items():
        bundled = bundled.replace(k, v)

    # Class renames.
    bundled = _apply_class_renames_in_selectors(bundled, rename_map)

    header = (
        f"/* =============================================\n"
        f"   {PAGE_SLUG.upper()} - generated by _build.py\n"
        f"   Paste into the CSS tab of the Modern HTML to Webflow Converter\n"
        f"   (https://moden.club/tools/html-to-webflow).\n"
        f"   Bundles _shared/(tokens|base|components).css + the page CSS,\n"
        f"   inlines every token var as a literal hex / value,\n"
        f"   and prefixes colliding classes with `{PREFIX}`.\n"
        f"   Do not edit by hand - re-run the build script after changing source.\n"
        f"   ============================================= */\n\n"
    )

    body_text = "\n".join(imports) + "\n\n" + bundled.strip() + "\n"
    _write(DST_CSS, header + body_text)

    return bundled  # returned so we can sanity-check leftover var refs


def build_js(rename_map):
    if not os.path.exists(SRC_JS):
        return  # JS is optional

    src = _read(SRC_JS)

    # Rename class selectors first (still inside the original IIFE wrapper).
    src = _apply_class_renames_in_selectors(src, rename_map)

    # Swap the outer IIFE for a Webflow.push wrapper so it runs after Webflow init.
    src = re.sub(
        r"^\(function \(\) \{",
        "window.Webflow = window.Webflow || [];\nwindow.Webflow.push(function () {",
        src, count=1, flags=re.MULTILINE,
    )
    src = re.sub(r"\}\)\(\);\s*$", "});\n", src, count=1)

    header = (
        "/* =============================================\n"
        f"   {PAGE_SLUG.upper()} - generated by _build.py\n"
        "   Paste into the JS tab of the Modern HTML to Webflow Converter\n"
        "   (https://moden.club/tools/html-to-webflow).\n"
        "   Requires GSAP + ScrollTrigger to be loaded BEFORE this script.\n"
        "   Add the two CDN <script> tags to Webflow's Project Settings ->\n"
        "   Custom Code -> Footer Code (one-time setup):\n"
        "     https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js\n"
        "     https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js\n"
        "   Do not edit by hand - re-run the build script after changing source.\n"
        "   ============================================= */\n\n"
    )
    _write(DST_JS, header + src)


def sanity_check_vars(css):
    leftover = sorted(set(re.findall(r"var\(--[a-z][a-z0-9_-]*\)", css)))

    print("Wrote:", DST_HTML)
    print("Wrote:", DST_CSS)
    if os.path.exists(SRC_JS):
        print("Wrote:", DST_JS)
    print()
    if leftover:
        print("ERROR: var() refs remain in output (build inlines all tokens):")
        for u in leftover:
            print(" ", u)
        print()
        print("Fix by either:")
        print("  - Adding the missing token to tokens.css (auto-populated next build), OR")
        print("  - Adding an explicit override to VAR_TO_LITERAL in this file.")
        sys.exit(1)
    print("OK: all token vars inlined as hex / literals.")


def main():
    if not PAGE_SLUG:
        raise SystemExit("Set PAGE_SLUG at the top of _build.py before running.")

    # Build the rename map and var map.
    rename_map = _build_rename_map()
    var_map = dict(VAR_TO_LITERAL)
    if not var_map:
        var_map = parse_tokens_css(TOKENS_CSS_PATH)

    build_html(rename_map)
    css_after = build_css(var_map, rename_map)
    build_js(rename_map)
    sanity_check_vars(css_after)


if __name__ == "__main__":
    main()
