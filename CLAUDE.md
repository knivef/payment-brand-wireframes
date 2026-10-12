# CLAUDE.md

Repo context. Read this first, before anything else. Treat it as binding.

## What this repo is

A multi-brand payment wireframe repo, generated from the brand book. The base URL
indexes every brand. Each card links to `/brands/<slug>/`.

Plain HTML and CSS. The deployed site is static. `scripts/build.py` is a content
generator, not a deploy step. Never introduce a framework, a bundler or a package
manager.

## Architecture, three layers

```
data/brand-book.json   Brands, price lists, pitches, lifted from Brand_Book.xlsx.
                       Licence, status, type and priority live here. Source of truth.
data/pages.json        Page content per brand. The only hand-written input.
scripts/build.py       Renders brands/<slug>/index.html + brand.css, rewrites the hub.
```

```
assets/base.css        Layout and structure. Shared by every brand.
assets/themes.css      Design styles. A style owns the look. Count is generated.
brands/<slug>/brand.css  Accent tokens only. Three lines.
```

Change a rate in `data/brand-book.json` and every brand using that price list
updates on the next build. That is the point.

## Canonical repo

Every change belongs in **https://github.com/knivef/payment-brand-wireframes**.
That is the only copy that matters. Work left in a local folder, a scratch
directory or a chat attachment does not count as done.

Push with:

```bash
./scripts/sync.sh "imperative one line, no em dashes"
```

It runs the health check first and refuses to push if the check fails. It wires
`origin` on first run, so a fresh folder needs no setup. Never push by hand with
raw git commands; use the script so the check cannot be skipped.

Push at the end of every task, not in a batch at the end of a session. A brand
page that builds and passes the check is a commit.

## The three rules

**1. Never hand-edit `brands/`.** Everything in there is generated. Edit
`data/pages.json` and run `python3 scripts/build.py`. `scripts/check.sh` fails if
the committed output is stale.

**2. Structure is shared, style is a theme, brand is an accent.**
`base.css` owns every layout rule. `themes.css` owns palette, type, border weight,
radius, shadow and rhythm, under `[data-style="..."]`. A brand's `brand.css` may
set only `--accent`, `--accent-fg`, `--accent-soft`. If a brand needs a layout
treatment that does not exist, add a reusable class to `base.css` and say so.

**3. Every change is pushed.** A task is not finished until
`./scripts/sync.sh "<message>"` has succeeded and reported the repo URL. If the
push fails, say so plainly and stop rather than carrying on with the next brand.

**4. Licence language follows the brand book.** `data/brand-book.json` says which
licence each brand holds. Zepapay and SPS hold a UAE PSP licence. NexFlow holds a
Canadian MSB licence. **Every other brand holds none.** A brand with no licence
must never state or imply one. It may describe a partner structure, and the
partner entity stays as `[CONFIRM: ...]` until legal signs it off.
`scripts/check.sh` enforces this.

## Design styles

12, in `assets/themes.css`. Set per brand via `"style"` in `data/pages.json`.

| Style | Reads as | In use |
|---|---|---|
| `terminal` | Near-black, monospace headings, tight corners, dense. Reads as payments infrastructure. Good for settlement, payouts, API-led brands. | Zepapay |
| `swiss` | White, oversized type, hairline rules, no radius, generous air. Reads as editorial and senior. Good for brands selling to institutions. | Sepa Mint |
| `brutal` | Hard 2px borders, offset shadows, flat blocks, zero radius. Loud and memorable. Good for a burnable brand that needs to be noticed fast. | Ape Card |
| `soft` | Light, rounded, layered shadows, roomy cards. The familiar modern fintech look. Lowest risk, highest trust with non-technical buyers. | Offrampr |
| `midnight` | Deep navy, serif display, warm accent, wide rhythm. Reads premium and relationship-led. Good for VIP, large ticket, private desks. | Secure Payment Services |
| `clinical` | Pale grey-blue, small radii, dense tables, utilitarian. Reads as compliance and operations. Good where the buyer reads the fine print. | Pure Labs |
| `mono` | Black and white, one accent, enormous headlines, no chrome. Reads as confident and unfussy. Good for a single-claim page. | free |
| `ledger` | Slate, structural dividers, strong tabular numerics, two-column rhythm. Reads as a settlement ledger. Built for brands selling two rails at once. | free |
| `stamp` | Ink-dark, condensed uppercase headings, heavy rules. Reads as approval and authority. Built for a brand whose whole promise is getting you approved. | free |
| `warm` | Cream, humanist type, large body copy, gentle rounding. Reads as helpful rather than institutional. Built for a small owner-operator buyer. | free |
| `wire` | Blueprint light, thin rules, monospace numerics, technical calm. Reads as a transfer rail. Built for fiat-in, crypto-out. | free |
| `frame` | Near-black, thin white hairlines, a visible outer frame and square nodes where lines cross. Light headings, muted body, white buttons, accent only on links, active tabs and checks. Flat. | AltPay |

This table is generated. `assets/themes.css` is the only source of truth, the
index page reads it at build time, and `scripts/build.py` prints the count. If a
doc and the stylesheet disagree, the stylesheet is right.

A style not listed as in use is free capacity. Past 12 brands, styles have to be
shared or new ones written. Sharing is acceptable for Burnable brands that will
never sit side by side with their twin; it is not acceptable for two Permanent
brands in the same vertical.

## Content source

`content/brand-homepages.md` carries researched positioning, SEO, full copy,
pricing and FAQ for Swipe Wire Pay, Card Payz, Fiat Pay, Sepa Mint, Offrampr and
Onrampr. Build those six from it rather than writing fresh copy. Its section 7
lists nine open items that block publication.

## The index and the switcher

Two ways to move between brands, both generated:

- **The index at `/`** lists every brand with its status, licence, type, style
  and accent, filterable by status. `scripts/build.py` rewrites its registry
  block on every build.
- **The review switcher**, bottom left on every brand page. Lists all brands,
  marks the current one, and gives prev and next. Keys: `[` previous, `]` next,
  `b` index, `/` toggle.

The switcher renders **only while the page carries its wireframe `noindex` tag**.
Remove that tag for launch and the switcher disappears on its own. Never add a
hand-written cross-brand nav to a page; it would ship live.

The switcher's order matches the index order, so stepping with `]` follows the
cards. Only the list scrolls; Prev, Next and All brands stay reachable at any
brand count, and the current brand is scrolled into view when the panel opens.

`check.sh` verifies that every page's switcher lists every brand, which catches
the case where one brand was rebuilt alone and its menu went stale. If that fails,
run `python3 scripts/build.py` with no argument.

## Launching one brand at a time

`vercel.json` is generated. Launching is per brand, in one place:

```json
{ "slug": "zepapay", "launched": true, ... }   // in data/pages.json
```

Rebuild, and that brand's page loses its `noindex` meta tag and its
`X-Robots-Tag` header. Every other brand keeps both, and the index at `/` stays
out of search permanently. The review switcher also disappears from a launched
page, because it keys off the same `noindex` tag.

Never hand-edit `vercel.json`, and never remove the robots tag from a page
template. There is no repo-wide switch, which is the point.

## Dates and build churn

The registry's `updated` field only moves when a page's rendered output actually
changes. `data/build-state.json` holds a content hash per brand and is committed.
Rebuilding on a quiet day produces no diff. Do not delete that file to force a
refresh; change the page.

## Page section order

announcement, nav, hero, trust bar, problem, product, how it works, pricing,
estimator, segments, compliance, lead form, FAQ, final CTA, footer, sticky bar,
rail CTA, exit modal.

Framed layout: `"framed": true` puts `data-framed` on `<html>`. base.css then draws
one centred frame with an outer border, a full-width hairline between sections, a
divider between two-column layouts, and a 6px node wherever lines cross. Pair it with
the `frame` style (AltPay). Its tokens (`--frame-w`, `--line`, `--node`,
`--node-color`, `--col-pad`) live on `[data-framed]` and the theme can override them.

One exception: `"segments_first": true` moves segments to directly after the trust
bar, for a page that leads with who it serves (Offrampr). Nothing else reorders.

Sections appear only if that key exists in `data/pages.json`. **There is no
competitor comparison section.** It was dropped on purpose. Do not add one back
without being asked.

## Conversion layer

All wired in `assets/conversion.js`, all opt-in via data attributes.

| Element | Attribute |
|---|---|
| Announcement bar, dismissal remembered | `data-announce` |
| Countdown, fixed deadline or rolling window | `data-countdown` |
| Sticky nav | `data-nav` |
| Read progress bar | `data-progress` |
| Sticky bottom bar (mobile) and rail CTA (desktop) | `data-stickybar`, `data-railcta` |
| Exit modal, once per visitor | `data-exit-intent` |
| Scroll reveal | `.reveal` |
| FAQ accordion, feeds FAQPage schema | `.faq details` |
| Fee estimator, rates read from the markup | `data-estimator` |
| Multi-step form with per-step validation | `data-multistep` |
| Lead form: honeypot, timing check, free-email block, inline success | `data-lead-form` |
| Event stream for analytics | `wf:event` window event |

## House rules

- **No em dashes.** Anywhere. `check.sh` enforces it.
- **No invented facts.** Pricing comes from `data/brand-book.json`. Anything else
  unverified stays as `[CONFIRM: ...]` and gets a claims-register row.
- **No AI register.** Banned: seamless, robust, unlock, empower, leverage,
  landscape, "in today's", "we understand that", "it's not just X, it's Y".
- Published pricing is a deliberate conversion lever, and it is also an internal
  rate card. Confirm with kvn per brand before a page goes public.
- Every page keeps `noindex` until that brand launches. Remove per brand.
- Commit messages: imperative, one line, no em dashes. `sync.sh` rejects them.

## Commands

```bash
python3 scripts/build.py            # rebuild every page and the hub
python3 scripts/build.py zepapay    # rebuild one
./scripts/check.sh                  # run before every push, 7 sections
./scripts/sync.sh "message"         # check, commit and push to the canonical repo
python3 -m http.server 4321         # preview at localhost:4321
```

In Cowork, each shell call is a fresh short-lived shell. Start the preview server
detached and give the user the URL:

```bash
cd "<repo root>" && nohup python3 -m http.server 4321 >/dev/null 2>&1 &
```

If it does not survive, ask the user to run it in Terminal, or push and review the
Vercel preview. Pages link `/assets/base.css` absolutely, so `file://` will not
render them.

## Running in Cowork with the folder attached

The attached folder is the repo root. This file is not loaded automatically, so
read it first. Anchor every path from the repo root; do not rely on a previous
call's working directory or a background process.

## Ask, do not assume

- A claim needs a number that is not in the brand book
- A brand with no licence needs to say something about regulation
- Published pricing is about to go on a public page
- A page needs a layout `base.css` does not have
- A brand is missing from `data/brand-book.json`
