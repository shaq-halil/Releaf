# Content and release register

Current milestone: Home and Our Story implemented locally, followed by the requested site-wide readability refinements and targeted homepage simplification. The homepage uses the owner’s latest schoolbook-section copy, shared 1200px content container, three “Where you fit” enquiry cards, minimal direct WhatsApp contact and alternating white/forest content sections. Other pages and publication follow review. No deployment has been performed.

## Content implemented from the directive

- Atika Yakubu — Founder & Chief Executive Officer (CEO).
- Rosemary Elorn — Chief Operations Officer (COO).
- Halleo Shaq — Chief Technology Officer (CTO).
- WhatsApp: +233 55 540 1859 / `https://wa.me/233555401859`.
- Founder story: a mother observed used papers and exercise books coming home with her children and accumulating; she envisioned organised recovery with potential educational benefit.
- ReLeaf is developing its model and seeking partners. No school relationship, collection activity, production volume, savings or NGO partnership is presented as verified.

The names follow the newest PDF instruction, superseding old source spellings. Confirm them with the owner **before publication**, as the directive requests. No unsupported parent conversations, credentials, quotations or team biographies remain.

## Assets actually available

| File | Type / dimensions | Status |
| --- | --- | --- |
| `images/ceo.png` | PNG, 1086 × 1448 | Owner-supplied designated founder image. Used in a modest frame, preserving supplied proportions and appearance. |
| `images/1.jpg` | JPEG, 736 × 968 | Used for a modest material spread; no claim that it documents ReLeaf operations. |
| `images/Bundled Paper Stacks at Green-Framed Entrance.png` | PNG, 1086 × 1448 | Used on Our Story with an explicit non-operational caption. Provenance beyond owner supply is unverified. |
| `images/Cluttered Archive Room with Filing Shelves.png` | PNG, 1278 × 1230 | Audited, not used. Provenance beyond owner supply is unverified. |
| `2.jpg` | JPEG, 736 × 1308 | Not used; document writing visible. |
| `assets/images/originals/paper-next-chapter-concept.png` | PNG, 1672 × 941 | Original AI-generated hero concept, identified in image alternative text and asset notes. Prompt/tool provenance in `assets/images/GENERATION.md`. |
| Existing older founder/paper WebP files | Older derivatives | Preserved, no longer referenced by the redesigned pages except the schoolbook image. |
| Moooi reference MP4 files | Two proprietary reference videos | Not ReLeaf footage. Excluded from runtime and static export. |

No ReLeaf video, Rosemary portrait or Halleo portrait was found. Leadership therefore uses names and roles with equal typographic treatment, with no fictitious portraits or public placeholder biographies. No photographic permission is inferred from file presence. Final permission/provenance review remains with the owner.

## WhatsApp behaviour

Both pages now share one centered contact section with the owner’s exact heading, supporting sentence and a single “Contact Us” button linking to `https://wa.me/233555401859` in a new tab. The link uses `noopener noreferrer` and a locally rendered recognizable WhatsApp SVG. All forms, previews, validation controls, dropdowns, copy buttons and form/configuration scripts have been removed. No backend or message preparation remains. Schools, partners, businesses and navigation still target `#conversation`. The former footer privacy/enquiry anchor was replaced with a working contact link.

## Release dependencies

1. Review Home and Our Story against page 4 of the supplied directive, then approve or amend the direction before other pages are styled.
2. Run fresh browser checks/screenshots at phone, tablet and desktop widths, keyboard and reduced motion. This session’s sandbox prevents the preview server and Chromium startup; these checks are pending, not passed.
3. Confirm leadership spellings, image permissions/provenance and founder copy with the owner before publication.
4. Supply the final public hosting URL. Run `python3 scripts/build.py --site-url https://actual-host/actual-path`; current relative social image metadata and empty draft sitemap must be finalised before launch.
5. Complete remaining pages after direction approval. Only Home and Our Story existed in the current source; no established page was removed.
6. Test WhatsApp handoff on owner devices; no messages are sent by automated QA.
7. Use a clean static export so reference snapshots and unused source images are never published.
