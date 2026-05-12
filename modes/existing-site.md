# Mode B: Edit an existing Webflow site

The user has an existing Webflow site and wants to add or modify pages via the converter workflow. This mode covers three sub-flows. The first thing to do is figure out which one.

## Identify the sub-flow

Ask the user (use AskUserQuestion):

> Which of these are you doing?
> **B1)** I have a Webflow site export (`.zip` or unzipped folder), and I want to extract its design system / class names to seed a new page.
> **B2)** I want to add a brand-new page to an existing Webflow site that's already live.
> **B3)** I want to modify a page that's already on the live site.

Then jump to the corresponding section below.

---

## B1 — Working from a Webflow export

The user has either a `.zip` of their Webflow site (downloaded via Webflow's Export Code button) or an unzipped folder. We'll mine it for the design system, then proceed to B2 or B3.

### Steps

1. **Locate the export's main CSS file.** Webflow exports into a folder named like `<site-name>.webflow/css/<site-name>.css`. That file's `:root` block at the top contains every CSS variable defined on the site. Read it.

2. **Build the project's `tokens.css`.** Copy the variables from the Webflow export's `:root` into your project's `tokens.css`. Match Webflow's variable names exactly so you can reference them in source CSS. The build script will inline these to literals at export time.

3. **Build `COLLIDE_RENAMES` for the project.** Grep the export's main CSS for every top-level class:

   ```bash
   grep -oE '^\.[a-zA-Z][a-zA-Z0-9_-]*' path/to/<site-name>.css | sort -u
   ```

   Every class returned is a class on the live site. Any class your new code uses that matches one of these is a collision. Save the full list to `_build.py`'s `COLLIDE_RENAMES` so the build prefixes them automatically.

4. **Verify GSAP/ScrollTrigger inclusion (if needed).** If the site already has GSAP loaded, your animation code can reuse it. Check `<site-name>.html` (the homepage export) for `<script>` tags loading GSAP. If GSAP isn't there, plan to add it to **Project Settings → Custom Code → Footer Code** before publishing — see [reference/webflow-runtime.md](../reference/webflow-runtime.md).

5. **Identify the live site's typography / brand classes.** Look in the export CSS for classes like `.heading-style-h1`, `.button`, `.text-eyebrow`. Decide whether your new code should *use* these (referencing the live site's design system) or *re-implement* them under a prefixed name (avoiding collision). Reuse is cleaner; prefix is safer.

Once you have `tokens.css` populated and `COLLIDE_RENAMES` filled in, hand off to **B2** (add new page) or **B3** (modify existing page).

---

## B2 — Add a new page to an existing Webflow site

The user wants a brand-new page on a Webflow site that's already live. The existing site is reference-only — your code becomes a new URL on the same site.

### Steps

1. **Confirm B1 was done.** You need `tokens.css` and `COLLIDE_RENAMES` populated from the existing site. If not, do B1 first.

2. **Scaffold the new page.** Create a project structure:

   ```
   project-root/
   ├── pages/
   │   ├── _shared/
   │   │   ├── tokens.css         # populated from the live site export
   │   │   ├── base.css           # from templates/base.css
   │   │   └── components.css     # from templates/components.css (or empty if reusing live components)
   │   └── <new-page-slug>/
   │       ├── index.html         # from templates/page-template.html
   │       ├── <slug>.css         # from templates/page.css (empty)
   │       ├── <slug>.js          # from templates/page.js (optional)
   │       └── _converter/
   │           └── _build.py      # from templates/_build.py
   ```

3. **Author the new page section by section.** Build hero first, show the user, iterate. Don't write the whole page in one go. Once approved, move to section 2. Repeat. Follow [reference/css-rules.md](../reference/css-rules.md).

4. **Use placehold.co for images during authoring.** See [reference/asset-handling.md](../reference/asset-handling.md). Re-link in Webflow's Asset Manager after import.

5. **Run the build:**

   ```bash
   python pages/<new-page-slug>/_converter/_build.py
   ```

6. **Import into Webflow.** Follow [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md):
   - Create the new page in Webflow's Pages panel (right-click → New Page → set slug, title, parent).
   - Open https://moden.club/tools/html-to-webflow, paste HTML/CSS/JS into respective tabs.
   - Convert and import to the new Webflow page.
   - Re-link images via Webflow Asset Manager.
   - Confirm GSAP is in Footer Code if you used animations.
   - Publish to staging, smoke-test, publish to production.

7. **Show the user the published URL.** Confirm it renders correctly on desktop, tablet, mobile breakpoints (Webflow's standard 991/767/479px).

---

## B3 — Modify an existing live page

The user wants to change a page that's already live in Webflow. This is the trickiest sub-flow because re-importing a modified version doesn't merge cleanly with the existing page.

### Critical rule

**Always delete the existing page in Webflow BEFORE re-importing the modified version.** Otherwise, classes from the old version stay attached and create class manager pollution. Webflow prunes classes that only lived on the deleted page; shared classes (e.g., `.button`, `.section`) keep their original site-wide rules.

If MCP is available, use `mcp__claude_ai_Webflow__data_pages_tool` to delete the page programmatically. Otherwise, walk the user through manual deletion in Webflow's Pages panel.

### Steps

1. **Backup first.** Confirm the user has either:
   - A recent Webflow Backup (Settings → Backups → create one now if not).
   - A code export of the current state (Settings → Export Code).

   This is reversible insurance — if the re-import goes sideways, the backup restores the page.

2. **Confirm B1 was done** for the parent site (tokens + collisions).

3. **Get the original page's source.** If the user has the source code (in a repo, in the conversion pipeline they used originally), open it. If they don't — they're working from "what's in Webflow now" — export the site, find the page's HTML in `<page-slug>.html`, and reverse-engineer source files (`<slug>.css` + `<slug>.js`) from the export's CSS / JS. This is grunt work; warn the user.

4. **Author the modifications section by section.** Edit the source files (`<slug>.css`, `<slug>.js`, `index.html`). Don't touch other sections, don't refactor unrelated code. Show the user the change, iterate, get approval.

5. **Run the build:**

   ```bash
   python pages/<slug>/_converter/_build.py
   ```

6. **DELETE THE PAGE IN WEBFLOW.** Use [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md). Verify deletion completed before proceeding.

7. **Re-import** via the converter at https://moden.club/tools/html-to-webflow:
   - Recreate the page in Webflow's Pages panel (with the same slug, title, SEO settings as the deleted one).
   - Paste HTML/CSS/JS, convert, import to the new (empty) page.
   - Re-link images (Asset Manager).
   - Re-apply page-level SEO settings if they didn't carry over.

8. **Smoke-test on staging.** Publish to staging FIRST. Walk through the page in the Designer canvas + on staging URL. Confirm:
   - No layout glitches.
   - Animations fire correctly.
   - Images are linked.
   - Internal links work.
   - SEO metadata is intact.

9. **Publish to production.** Use the [`safe-publish`](../) skill if available — it shows a diff of what changed since the last publish and asks for confirmation. Otherwise: Webflow → Publish → Production → Confirm.

10. **Notify stakeholders.** Re-imports are visible to anyone who had the page bookmarked. Mention it in your team channel / changelog.

---

## MCP integration (B2 + B3)

Where Webflow MCP tools are available, prefer them over manual Designer steps:

| Step                            | MCP tool                                                          |
| ------------------------------- | ----------------------------------------------------------------- |
| Inspect existing pages          | `mcp__claude_ai_Webflow__data_pages_tool`                         |
| Delete a page (B3)              | `mcp__claude_ai_Webflow__data_pages_tool`                         |
| Upload images (Asset Manager)   | `mcp__claude_ai_Webflow__asset_tool`                              |
| Verify GSAP CDN is registered   | `mcp__claude_ai_Webflow__data_scripts_tool`                       |
| Inspect existing components     | `mcp__claude_ai_Webflow__data_components_tool`                    |
| Publish (with diff + confirm)   | `safe-publish` skill                                              |

If MCP isn't connected, fall back to the manual steps in [reference/webflow-designer-checklist.md](../reference/webflow-designer-checklist.md).

## Common pitfalls

- **Forgetting to delete the page in B3** → class pollution. Class manager fills up with `tool-card`, `tool-card-2`, `tool-card-3` over multiple re-import attempts.
- **Re-using the original variables but the build inlined literals** → live-site theme changes don't propagate to your imported page. This is a known tradeoff; document it for the user. See [reference/variable-mapping.md](../reference/variable-mapping.md).
- **Importing without checking GSAP CDN** → animations fail silently on the published site. The Designer might cache the script from a previous page that loaded it, masking the issue.
- **Not refreshing Webflow's class manager view** → after deleting a page and re-importing, the class manager sometimes shows stale entries. Refresh the panel or close/reopen the project to force a re-read.
