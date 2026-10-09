# Prompt 03 - Wireframe build

Turns `brands/<slug>/brief.md` into a live page. Run after research and SEO are
approved.

---

```
Build the wireframe page for BRAND_NAME from its approved brief.

Read in this order:
1. brands/BRAND_SLUG/brief.md
2. brands/_template/index.html
3. brands/_template/brand.css
4. assets/base.css
5. assets/conversion.js
6. index.html at the repo root

## Stage A - Scaffold

Copy brands/_template/index.html and brands/_template/brand.css into
brands/BRAND_SLUG/. Copy nothing else.

In brand.css, set only the token values: --accent, --accent-fg, --accent-soft,
and optionally --bg, --surface, --surface-2, --radius and --font-sans. Derive
--accent-soft as the accent at 12 percent alpha. If you change --font-sans, add
the font link to the page head.

Do not add a single layout rule to brand.css. If a section needs a layout
treatment that base.css does not have, add a reusable class to base.css instead
and tell me you did it. Brand pages must stay swappable.

Check contrast before you commit to the accent. Accent on background and
accent-fg on accent both need to clear WCAG AA. If the brief's colour fails,
darken or lighten it and note the change in the brief.

## Stage B - Fill the markup

Replace every [BRACKET] in index.html with copy from the brief. Reproduce the
brief copy exactly. Do not rewrite, tighten or improve it at this stage. If a
line does not fit the layout, change the layout or come back to me, do not
change the copy silently.

Section order is fixed by the template and matches the seven-beat narrative:
announcement, nav, hero, trust bar, problem, product, how it works, USP,
segments, comparison, pricing, proof, lead form, FAQ, final CTA, footer, sticky
bar, exit modal.

You may delete a section that the brief has nothing for. You may not reorder
them, and you may not add one without telling me why.

Specific rules:
- Delete the proof section entirely if the brief still has placeholder figures
  in it. An empty section is better than an invented merchant count.
- Delete the announcement bar and countdown if the brief's urgency source says
  "none".
- The comparison table has two renderings, a real table and a stacked card
  fallback below 820px. Populate both with the same data. They must not drift.
- Every FAQ answer that appears on the page must also appear in the FAQPage
  JSON-LD. Generate the JSON-LD from the same source rather than typing it twice.
- Keep every data attribute the template uses: data-nav, data-announce,
  data-countdown, data-stickybar, data-stickybar-after, data-modal,
  data-exit-intent, data-lead-form, data-cta. conversion.js binds to these and
  silently does nothing if they are missing.
- Give every CTA a distinct data-cta label so click events are attributable.
- Set data-key on the announcement bar, the countdown and the exit modal to
  BRAND_SLUG plus a version suffix, so dismissals do not leak between brands on
  the same preview domain.

## Stage C - SEO block

Fill the head from section 7 of the brief: title, meta description, canonical,
Open Graph, Twitter card. Leave the noindex meta tag in place while this is a
wireframe. Add the Organization, FAQPage and BreadcrumbList JSON-LD before the
closing body tag.

## Stage D - Register the brand

Add one object to the JSON block with id="brand-registry" in index.html at the
repo root:

{
  "slug": "BRAND_SLUG",
  "name": "BRAND_NAME",
  "tagline": "[the one-liner from the brief]",
  "accent": "[the accent hex]",
  "verticals": ["...", "..."],
  "status": "draft",
  "updated": "[today, YYYY-MM-DD]"
}

Keep the JSON valid. The index page parses it at runtime and renders nothing if
it breaks.

## Stage E - Serve and report

Run: python3 -m http.server 4321
Tell me the two URLs: the index at localhost:4321 and the brand page at
localhost:4321/brands/BRAND_SLUG/

Then report:
- Every bracket still left in the page, with its line number
- Every section you deleted and why
- Any base.css class you added
- The contrast ratios for accent on background and accent-fg on accent
```

---

## Design constraints baked into base.css

These are deliberate. Do not work around them.

| Constraint | Reason |
|---|---|
| One accent colour per brand | Two accents means nothing is emphasised, and CTA hierarchy collapses |
| No gradients on text, no glassmorphism, no parallax | Payment buyers read this as a startup that will be gone in a year |
| Scroll reveal is a 16px lift only, disabled under reduced motion | Animation that delays reading costs conversions |
| Comparison table has a mobile card fallback, never horizontal scroll | Horizontal scroll tables are effectively invisible on phones |
| Sticky bottom CTA is mobile only | On desktop it competes with the sticky nav CTA |
| Exit modal fires once per visitor, stored in localStorage | A modal on every visit reads as hostile |
| Free-email blocking is a visible inline message | Silent rejection loses leads you would have qualified manually |

## Wireframe mode

Add `class="wf"` to the body tag to strip all colour and shadow and review pure
structure. Useful when the question is "does the argument hold" rather than
"does it look good". Remove it before shipping.
