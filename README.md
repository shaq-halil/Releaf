# ReLeaf Collective — Every page deserves another life

A redesign in plain HTML, CSS and JavaScript, following the supplied **ReLeaf Codex Creative Redesign Directive**. This milestone contains **Home and Our Story** for review. The site has no framework, database, runtime dependencies or analytics.

## Review

- Art-direction board: `qa/art-direction.html`.
- Home: `index.html`.
- Our Story: `our-story/index.html`.
- Reference study: `ART_DIRECTION.md`.
- Content, assets and publication dependencies: `CONTENT_STATUS.md`.
- Hero source, final prompt and built-in generation-tool provenance: `assets/images/GENERATION.md`.

For full navigation and clipboard testing, run a local HTTP server from this directory:

```sh
python3 -m http.server 8080
```

Visit `http://localhost:8080/`, `http://localhost:8080/our-story/` and `http://localhost:8080/qa/art-direction.html`. You can also open the art-direction HTML directly to see the board and follow its direct file links to both pages; directory-style navigation requires an HTTP server.

The directive requests review of these two pages before the style is applied to other pages. No publication or remaining-page rollout has been performed. Home and Our Story were the only implemented pages in this checkout.

## Shared homepage alignment

The homepage now uses one `.site-container` for the header, hero text, all six content sections and footer. Its width is `min(100% - 2 × clamp(20px, 5vw, 72px), 1200px)`. Section wrappers provide only vertical spacing. Former homepage width caps and horizontal overrides have been removed from the shared stylesheet; focused homepage rules live in `assets/css/homepage.css`.

Look Again and Founder use the same `.feature-layout`: two equal tracks with the same gap, stacked below 901px. Both small labels use `.section-label`, aligned at the start of the text column on desktop and the content boundary on mobile. No labels were added to the other homepage sections. The schoolbook composition uses the latest requested recovery/education copy and story link.

“Where you fit.” contains exactly three equal desktop cards, stacked on smaller screens. They scroll to the shared WhatsApp contact section. The FAQ keeps its original questions and native disclosure behaviour under “Good questions. Clear answers.” Divider, indicator and open-state styling are more visible.

Contact is now a centered forest-green section shared by Home and Our Story: “Let's get connected.”, the owner’s single supporting sentence, and a rounded white “Contact Us” link with a recognizable WhatsApp SVG. It opens `https://wa.me/233555401859` in a new tab. There are no forms, fields, dropdowns, message previews, validation messages or copy controls. The former form/configuration scripts, journey attributes and unused form CSS were removed. The existing contact shortcut still hides while the main contact section is visible.

The post-hero sequence remains white / forest / white / forest / white / forest. The footer uses darker forest. The fixed homepage header begins with a nearly opaque translucent white background over the hero, switches to opaque white after 24px of scrolling, and stays white while the menu is open. Without JavaScript it stays an ordinary white header. Elastic navigation and reduced-motion behaviour are preserved.

Body text remains 18px desktop / 17px phone, section headings 40–56px desktop / 36–44px phone, captions 14px and labels/controls 16px. Spacing tokens set homepage section padding to 72px desktop, 56px tablet and 44px phone. No new sections, images or runtime dependencies were added.

Source-derived checks in `qa/readability-results.json` cover both pages at 12 widths including 360, 390, 768, 1024 and 1440px. `qa/header-state-check.cjs` exercises the actual header script against isolated event/state fixtures. Neither replaces browser rendering. Chromium remains blocked by the sandbox; fresh screenshots and visual/interaction QA are pending.

## The redesign

The new opening uses an original AI-generated concept still, identified in its image alternative text and asset notes: papers settling toward a stack in a sunlit interior. It is a static visual, not Blender footage. No ReLeaf footage was found; the two reference videos belong to Moooi and are not used. The full-resolution concept and responsive WebP derivatives are retained in `assets/images/`.

Instrument Serif headlines, readable DM Sans, warm paper, forest green and restrained grain establish a calmer editorial identity. The connected navigation uses independently written SVG geometry with short elastic transitions, keyboard focus support and a reduced-motion still treatment. Phones use a disclosure menu.

Atika’s newly supplied `images/ceo.png` is used at its natural proportions, in a supporting frame at most 360px wide on desktop and 280px on phones. Our Story presents **Atika Yakubu (Founder & CEO), Rosemary Elorn (COO) and Halleo Shaq (CTO)** in three editorial columns, stacked on phones. Names follow the newest directive and need owner confirmation before publication. No biographies, portraits or established outcomes were invented.

The local charity: water, Moooi and Floema snapshots were inspected as source references. Their images, fonts, scripts, branding and videos are not imported into ReLeaf. The export excludes these reference folders.

## WhatsApp

The recipient is `233555401859`, configured by the `WA` constant in `scripts/build.py`. The contact button links directly to `https://wa.me/233555401859` with `target="_blank"` and `rel="noopener noreferrer"`. It works without JavaScript. No enquiry data is collected or prepared by the website, and no backend is involved.

The SVG brand glyph is included inline with its original Font Awesome Free attribution comment. See `assets/icons/WHATSAPP_LICENSE.md`. It inherits forest green inside the contact button and ivory inside the existing floating shortcut.

## Editing and building

`index.html` and `our-story/index.html` are generated deployable files. Make shared markup/content changes in `scripts/build.py`, then run:

```sh
python3 scripts/build.py
```

Shared styles and containers are in `assets/css/styles.css`; homepage composition is in `assets/css/homepage.css`; navigation and scroll-header behaviour in `assets/js/main.js`. Fonts are local and include their SIL Open Font Licences. Original owner images remain unchanged.

A dependency-free export produces a clean static folder containing only the implemented pages and required local assets:

```sh
python3 scripts/export.py --output /tmp/releaf-review-export
```

Use a new or empty destination. The exporter never deletes existing content. It follows HTML/srcset/CSS dependencies, includes the social preview, font licences, robots, sitemap and `.nojekyll`, and excludes proprietary reference snapshots, QA artifacts, unused media and original source photographs. GitHub Pages or another static host needs no framework build.

## Metadata and publication

A real public URL has not been supplied. Titles, descriptions and the local 1200 × 630 social preview are present. Absolute canonicals/social URLs, sitemap entries and the robots Sitemap directive are finalised with the actual public URL, including any GitHub Pages repository path:

```sh
python3 scripts/build.py --site-url https://your-real-host/your-real-path
```

The URL above is an instruction placeholder; do not publish it. Reuse the actual URL on every later build. The current sitemap is intentionally empty until the final host is known. No unsupported impact, product or organisation schema is emitted.

After direction review, remaining pages, fresh browser QA and owner content/image approval, regenerate metadata and export to a clean folder. For GitHub Pages, publish that folder as a Pages artifact or copy its contents into the intended Pages source. Do not publish this entire workspace: it contains unlicensed reference snapshots. Validate direct `/our-story/` loading, paths under the actual repository subpath, social previews and real-device WhatsApp handoff on the final host.

## Verification

Fresh source/static checks:

```sh
python3 qa/static-check.py
python3 qa/readability-check.py
node qa/header-state-check.cjs
```

The readability audit additionally uses Node PostCSS and postcss-selector-parser, provided in this environment. Runtime pages have no dependency on these tools.

The optional audit requires Python BeautifulSoup and Pillow, available in this workspace. It checks local links and anchors, unique IDs, image files and dimensions, absence of form controls, the direct WhatsApp destination and its new-tab attributes, leadership names, the hero disclosure, JavaScript syntax, clean export contents, sitemap XML and canonical/social/sitemap generation under a test repository subpath in an isolated temporary copy. It writes `qa/static-results.json`.

**Fresh browser QA is pending.** This session blocked local socket creation and Chromium startup; automatic approval review rejected elevated execution because sandbox approvals are disabled. No responsive/browser, keyboard, reduced-motion, accessibility or performance pass is claimed for this redesign. Previous screenshots and Lighthouse results have been archived under `qa/previous-design-results/` and do not validate this version.

When a browser can run, serve the project and execute the existing browser checks using an installed Playwright package, optionally axe-core:

```sh
PLAYWRIGHT_MODULE=/absolute/path/to/playwright AXE_CORE_PATH=/absolute/path/to/axe.min.js node qa/browser-check.cjs
PLAYWRIGHT_MODULE=/absolute/path/to/playwright node qa/subpath-check.cjs
```

The browser suite covers both pages at 320, 360, 390, 650, 651, 768, 840, 841, 900, 1024, 1440 and 1920px, image decoding, shared container boundaries, feature-label alignment, three equal audience cards, centered contact content, scroll-header state, portrait size, desktop leadership alignment, the elastic navigation, the direct WhatsApp recipient, absence of forms, keyboard menu, FAQ, reduced motion and no-JavaScript content. It captures new screenshots into `qa/previews/` when run. The contact link is checked without sending messages. Run fresh Lighthouse and manual screen-reader/device checks before publication.
