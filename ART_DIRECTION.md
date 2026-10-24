# ReLeaf — a quieter kind of possibility

Review milestone: Home and Our Story, following the supplied *ReLeaf Codex Creative Redesign Directive*. Open `qa/art-direction.html` for the mini visual board and links to both pages. Publication and the remaining pages await the directive’s review checkpoint.

## What was actually inspected

Local reference folders are present. They are saved web snapshots, not complete development repositories. Their HTML, compiled CSS and JavaScript were inspected directly. No live browser reference interaction was observed in this session: Chromium is blocked by the sandbox. The interaction conclusions below come from actual source inspection.

- **charity: water**: `chariTywaTer/index.html`, builder styles and related CSS. A short primary message, clear section hierarchy, consistent alignment, generous spacing and obvious calls to action inform the content rhythm. Its donation components, statistics and images are unsuitable for ReLeaf and are not reused.
- **Moooi**: `moooi/index.html` and local styles. Hero media uses a cover video with `muted`, `playsinline`, a restrained overlay and real HTML headings. Two MP4 files exist, but both are Moooi reference assets, not supplied ReLeaf footage. Neither is reused.
- **Floema**: `floema/css/groq.CepGutwA.css` navigation rules and `floema/js/Mqeh8a45.js` Navigation/MetaRow code. It measures children, draws rounded SVG shapes and connecting bridges, changes link margins with an elastic easing, and uses pointer-follow lighting. ReLeaf implements independently written capsule and curved-neck geometry with finite transitions. It does not copy the source, gradient glow, GSAP, Vue or the reference’s compositions.

No reference images, logos, fonts, source components, tracking scripts or videos are imported into the ReLeaf runtime. Reference snapshots have no established reuse licence here and must be excluded from a public export.

## Direction

- Instrument Serif regular/italic is the display voice; DM Sans is the readable text face. Both are already locally hosted under SIL Open Font Licences.
- Forest `#173d30`, paper `#f7f5ee`, ink `#262f28`, beige `#e9e4d8`. Forest is reserved for the model and principles; paper is the default reading surface.
- Hero: original AI-generated architectural concept still, produced with the built-in image tool. Sunlit exercise-book and office sheets descend toward a desk stack. The image alternative text and generation notes identify its concept provenance; the direct homepage edit removing the hero caption is preserved. There is **no ReLeaf video** and no CSS animation presented as Blender footage. Generation prompt and provenance: `assets/images/GENERATION.md`.
- Navigation: original connected capsules with a small elastic expansion on hover and focus. Keyboard links remain ordinary links. Reduced motion disables the transition and animation loop. Mobile uses a menu disclosure with Escape and focus return.
- Rhythm: cinematic opening → centred short declaration → intimate material spread → four-step proposed cycle → modest founder feature → useful audience invitations → three FAQ questions → WhatsApp enquiry. No repeated full-bleed image banners or decorative card procession.
- Our Story: typographic opening → real founder, maximum 360px frame → material and educational purpose → three equal leadership columns → principles → current development stage → conversation.

## Image map

| Source | Implementation |
| --- | --- |
| New original concept still, 1672 × 941 | Home hero. Responsive 640/1024/1672 WebP; visible AI label. |
| `images/1.jpg`, 736 × 968 | Home material spread. Existing 360/736 WebP. Kept at modest display size. |
| `images/ceo.png`, 1086 × 1448 | Founder on both pages. New 360/640/1086 WebP; no face generation or alteration. |
| `images/Bundled Paper Stacks at Green-Framed Entrance.png`, 1086 × 1448 | Our Story material image. New responsive WebP; caption avoids an operational claim. |
| `images/Cluttered Archive Room with Filing Shelves.png`, 1278 × 1230 | Inspected; not used in the two review pages. Derivatives available. |
| Root `2.jpg`, 736 × 1308 | Not used: writing/documents require privacy and permissions review. |

There are no blur filters, low-resolution portrait upscales, fabricated team photos, invented biographies or verified-impact counters.

## Readability refinement

The follow-up preserves this direction while consolidating body text at 18px desktop / 17px mobile and section headings at 40–56px desktop / 36–44px mobile. Captions and utility copy are 14px; labels and controls are 16px or larger. Section padding now caps at 72px desktop, falls to 52px on tablets and 44px on phones. Column gaps, founder/leadership spacing and short section introductions are reduced. Paragraphs wrap without forced line breaks and stay within comfortable reading widths. Narrative layouts stack below 900px; the disclosure menu starts at 840px. The hero text stays visible throughout its short entrance. No new sections or decorative content were added.

## Current homepage refinement

One shared `.site-container` establishes a 1200px maximum and `clamp(20px, 5vw, 72px)` gutters. All section backgrounds remain full width, while the header, hero text, six section interiors and footer share its edges. Homepage-specific layout is in `assets/css/homepage.css`; legacy homepage overrides have been removed from the shared stylesheet.

Look Again and Founder share the same two-column feature grid, vertical centring and label treatment. Their labels sit consistently at the start of the text column, as the latest directive specifies for Look Again. On phones both follow the image at the common left boundary. No labels were introduced elsewhere.

“Where you fit.” contains exactly three cards: Schools & PTAs, Recovery & Industry, Businesses. Each has the supplied single-line description and links to the shared contact anchor. FAQ questions remain unchanged under “Good questions. Clear answers.” The contact section is now a centered forest-green call to action: the requested “Let's get connected.” heading, one supporting sentence and a rounded white WhatsApp button. Forms and their scripts/styles have been removed from both pages. The button works without JavaScript, and the `conversation` anchor remains unchanged. The footer is darker forest. The header uses nearly opaque translucent white over the hero; scrolling or an open menu gives it an opaque white background. Dark navigation text retains strong contrast throughout the transition.

Source checks cover both pages at 320, 360, 390, 650, 651, 768, 840, 841, 900, 1024, 1440 and 1920px. They check typography, common container rules, feature labels, stacked grids, card count, direct contact link and colour rhythm. Isolated header-event checks pass. These are not browser screenshots or rendered-layout passes; Chromium startup is still blocked by the sandbox.

## Review and verification limits

Source and static export checks are recorded in `qa/static-results.json`. JavaScript syntax was checked. Browser QA could not run: local socket creation was denied and Chromium failed at sandbox startup; automatic approval review rejected elevated server execution because this session disallows it. Do not describe old screenshots or old Lighthouse results as evidence for this version. Those artifacts are archived in `qa/previous-design-results/`.
