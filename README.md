# Payment brand wireframes

One repo, many payment brands, one prompt chain. The base URL is an index of
every brand. Clicking a card opens that brand's conversion wireframe at
`/brands/<slug>/`.

Plain HTML and CSS. No build step, no framework, no bundler. Vercel serves it
as static output.

---

## Structure

```
.
├── index.html              Brand index. Reads the JSON registry inside it.
├── vercel.json             Clean URLs, cache headers, noindex while in wireframe stage.
├── assets/
│   ├── base.css            All structural CSS. Shared by every brand.
│   └── conversion.js       Sticky bars, countdown, exit intent, accordion, forms.
├── brands/
│   ├── _template/          Fork this for a new brand. Never ship it.
│   │   ├── index.html      17 sections, every conversion mechanic wired up.
│   │   ├── brand.css       Token overrides only.
│   │   └── brief.md        The research output format.
│   └── <slug>/             One folder per brand, same three files.
├── prompts/
│   ├── 00-orchestrator.md  Runs the whole chain with approval gates.
│   ├── 01-research.md      Competitor teardown, positioning, narrative, copy.
│   ├── 02-seo.md           Keyword selection, on-page assets, schema.
│   ├── 03-wireframe.md     Brief to live page.
│   └── 04-qa-deploy.md     QA checklist, commit, deploy.
└── scripts/
    └── check.sh            Repo health check. Run before every push.
```

---

## Adding a brand

```bash
# 1. From the repo root, open Claude Code and paste prompts/00-orchestrator.md
#    with the variables filled in. Approve at each of the four gates.

# 2. Preview locally
python3 -m http.server 4321
# index:       http://localhost:4321/
# brand page:  http://localhost:4321/brands/<slug>/

# 3. Check and push
./scripts/check.sh
git add -A && git commit -m "Add <slug> wireframe" && git push
```

Vercel deploys on push. Every branch gets a preview URL, which is the cheap way
to A/B two versions of a hero with a real stakeholder.

---

## The two rules that keep this scalable

**Structure is shared, brand is tokens.** `assets/base.css` owns every layout
rule. A brand folder's `brand.css` may set `--accent`, `--accent-fg`,
`--accent-soft`, `--bg`, `--surface`, `--surface-2`, `--radius` and
`--font-sans`, and nothing else. `scripts/check.sh` fails the build if a
`brand.css` grows a layout rule. This is what lets you fix a mobile bug once and
have every brand inherit the fix.

**The brief is the only input to the build.** If a claim is not in
`brands/<slug>/brief.md`, it does not go on the page. That keeps copy decisions
in a reviewable markdown file instead of buried in HTML.

---

## Conversion mechanics available

All wired in the template, all opt-in via data attributes. Delete the markup for
any you do not want.

| Element | Attribute | Behaviour |
|---|---|---|
| Announcement bar | `data-announce` | Sticky top, dismissible, remembers dismissal |
| Countdown | `data-countdown` | Fixed `data-deadline`, or a rolling `data-hours` window per visitor |
| Sticky nav | `data-nav` | Gains a border after 32px of scroll |
| Sticky bottom CTA | `data-stickybar` | Mobile only, appears once the hero leaves the viewport |
| Exit modal | `data-exit-intent` | Mouse-out on desktop, dwell plus scroll depth on mobile, once per visitor |
| Scroll reveal | `.reveal` | 16px lift, disabled under reduced motion |
| FAQ accordion | `.faq details` | One open at a time, feeds FAQPage schema |
| Lead form | `data-lead-form` | Honeypot, timing check, free-email block, inline success |
| CTA tracking | `data-cta` | Fires a `wf:cta` window event for any analytics script |

---

## House rules

- No em dashes. Anywhere. `scripts/check.sh` enforces it.
- No invented numbers, merchant counts, volumes, testimonials or certifications.
  Unverified content stays as a `[BRACKETED PLACEHOLDER]` and gets a row in the
  claims register in `brief.md`.
- The comparison table must contain at least one row where the brand honestly
  loses or ties.
- Delete the proof section rather than publish placeholder figures.
- Drop the countdown rather than invent a deadline.
- Every page carries `noindex` while it is a wireframe. Remove it per brand at
  launch, not before.

---

## Wireframe mode

Add `class="wf"` to a brand page's `<body>` to strip all colour and shadow and
review structure alone. Useful when the question is whether the argument holds,
not whether it looks good.

---

## Vercel setup

Framework preset: **Other**. Build command: none. Output directory: `.`
`vercel.json` handles the rest.

Point each brand's real domain at the project later with a rewrite, or split the
brand into its own project once it is past wireframe stage.
