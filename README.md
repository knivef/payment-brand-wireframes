# Payment brand wireframes

**Canonical repo: https://github.com/knivef/payment-brand-wireframes**
Every change goes there. Push with `./scripts/sync.sh "message"`, which runs the
health check first and refuses to push if it fails.

One repo, many payment brands, generated from the brand book. The base URL indexes
every brand. Each card opens that brand's page at `/brands/<slug>/`.

Plain HTML and CSS, served statically by Vercel. No build step at deploy time.

---

## Brands live

| Brand | Style | Sells | Licence |
|---|---|---|---|
| Zepapay | `terminal` | Crypto to fiat settlement, two way | UAE PSP |
| Secure Payment Services | `midnight` | Client collection and IBAN for forex | UAE PSP |
| AltPay | `frame` | Client collection for forex, crypto settlement | None |
| Ape Card | `brutal` | Crypto cards, four tiers | None |
| Pure Labs | `clinical` | Pre-screening for peptide and nutra merchants | None |
| Offrampr | `soft` | Mass payouts funded in crypto | None |
| Sepa Mint | `swiss` | Crypto to EUR on SEPA | None |
| Swipe Wire Pay | `ledger` | Card acquiring plus crypto offramp, sold as a bundle | None |
| Card Payz | `stamp` | High-risk merchant accounts, four programmes | None |
| Fiat Pay | `warm` | Cards and crypto to bank for small peptide stores | None |
| Onrampr | `wire` | Fiat in, stablecoins out, for business treasury | None |

Old hand-built pages from before the generator live in
`archive/legacy-pre-generator/`. They are not built or linked.

Each page uses a different style on purpose, so they can be judged side by side
before any of them goes to design.

---

## Structure

```
data/brand-book.json     Brands, price lists, pitches, from Brand_Book.xlsx. Source of truth.
data/pages.json          Page content per brand. The only hand-written input.
scripts/import-book.py   Re-extract the JSON after editing the workbook.
scripts/build.py         Render every page and rewrite the hub registry.
scripts/check.sh         Health check. Run before every push.
scripts/sync.sh          Check, commit and push to the canonical repo.
scripts/bootstrap.sh     One-time vercel link for a fresh clone.
assets/base.css          Layout. Shared by every brand.
assets/themes.css        Design styles. Count generated into the index page.
assets/conversion.js     Sticky bars, countdown, exit intent, estimator, forms.
assets/review.js         Review switcher, bottom left on every wireframe page.
brands/<slug>/           Generated. Never hand-edit.
prompts/                 How to add or define a brand.
```

---

## Commands

```bash
python3 scripts/build.py                      # rebuild everything
python3 scripts/build.py zepapay              # rebuild one brand
python3 scripts/import-book.py Brand_Book.xlsx   # after editing the workbook
./scripts/check.sh                            # before every push
./scripts/sync.sh "message"                   # check, commit, push
python3 -m http.server 4321                   # preview at localhost:4321
```

---

## Reviewing the set

The index at `/` lists every brand with status, licence, type, style and accent,
filterable by status. From any brand page the review switcher sits bottom left:
it lists all brands, marks where you are, and gives prev and next.

Keyboard: `[` previous brand, `]` next brand, `b` back to the index, `/` toggle
the panel. Typing in a form field never triggers them.

The switcher renders only while a page carries its wireframe `noindex` tag, so
it removes itself at launch. It cannot ship live by accident.

## The three rules

**Never hand-edit `brands/`.** It is generated. Edit `data/pages.json` and rebuild.
`check.sh` fails if the committed output is stale.

**Structure is shared, style is a theme, brand is an accent.** `base.css` owns
layout. `themes.css` owns the look under `[data-style="..."]`. A brand's
`brand.css` is three accent lines. Fix a mobile bug once, every brand inherits it.

**Licence language follows the brand book.** Zepapay and SPS hold a UAE PSP
licence. NexFlow holds a Canadian MSB licence. Every other brand holds none and
must never state or imply one. Partner framing is allowed, with the partner entity
left as `[CONFIRM: ...]`. `check.sh` enforces this per brand.

---

## Conversion layer

Published pricing is the main lever. Most providers in these categories hide their
rates, so putting the real rate card on the page is the cheapest differentiator
available. Pricing comes from the shared price lists, so changing a rate in the
workbook changes every page that uses it.

On top of that: announcement bar with a countdown, sticky nav, read progress,
sticky bottom bar on mobile and a rail CTA on desktop, exit modal once per visitor,
scroll reveal, single-open FAQ feeding FAQPage schema, a fee estimator that shows
the effective rate at the buyer's own volume, multi-step forms with per-step
validation, honeypot plus timing plus free-email blocking, and a Telegram CTA
alongside every primary CTA because that is the channel these buyers use.

Every interaction fires a `wf:event` window event for whatever analytics gets
bolted on.

There is **no competitor comparison section**. It was dropped on purpose.

---

## Burnable versus Permanent

The brand book marks each brand. Permanent brands are worth deep SEO and a content
backlog. Burnable brands get one page, fast, and are built to be replaced. Do not
spend permanent effort on a burnable.

---

## Before anything goes public

- Open placeholders on every page, mostly partner entities, supported assets and
  timings. `check.sh` lists every one, in full, per brand, with the current total.
- Launching is per brand. Set `"launched": true` on that brand in
  `data/pages.json` and rebuild. Its page loses the `noindex` meta tag and its
  `X-Robots-Tag` header, and every other brand keeps both. `vercel.json` is
  generated, so there is no repo-wide switch to get wrong.
- Published pricing is an internal rate card. Confirm per brand before it goes on
  a public page.

---

## Vercel

Framework preset **Other**. Build command: none. Output directory `.`
`vercel.json` handles clean URLs, cache headers and the noindex header.
