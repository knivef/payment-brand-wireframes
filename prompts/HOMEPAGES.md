# Six homepages, six designs

Content source: `content/brand-homepages.md`. It carries the positioning, SEO,
full copy, pricing and FAQ for all six brands. The prompts below point at it by
section number so you never have to paste copy into a prompt.

**Everything lands in https://github.com/knivef/payment-brand-wireframes.**
Every prompt below ends with a push. A page that is not in that repo is not done.

**Comparison tables are skipped.** Section 1 of the content file includes one for
Swipe Wire Pay. Do not build it. Every prompt below says so.

## Style and accent, already assigned and contrast checked

| Brand | Style | Accent | Accent on background | Text on accent |
|---|---|---|---|---|
| Swipe Wire Pay | `ledger` | `#38bdf8` | 8.62 | 8.82 |
| Card Payz | `stamp` | `#c6f24e` | 14.52 | 14.52 |
| Fiat Pay | `warm` | `#c2410c` | 4.99 | 5.18 |
| Sepa Mint | `swiss` | `#d7263d` | 4.96 | 4.96 |
| Offrampr | `soft` | `#4f46e5` | 6.29 | 6.29 |
| Onrampr | `wire` | `#0f766e` | 5.19 | 5.47 |

All six clear WCAG AA on both axes. Four of the styles are new in
`assets/themes.css`:

- **ledger** Slate, structural dividers, monospace numerics, left accent rule on
  every card. Reads as a settlement ledger. Fits a brand selling two rails.
- **stamp** Ink-dark, condensed uppercase Oswald headings, 2px rules, near-zero
  radius. Reads as approval and authority.
- **warm** Cream, Nunito, 18px body, gentle rounding. Reads as helpful rather
  than institutional. Fits an owner-operator buyer.
- **wire** Blueprint light, IBM Plex, thin rules, 2px radius, monospace numerics,
  top accent rule on cards. Reads as a transfer rail.

Sepa Mint keeps `swiss` and Offrampr keeps `soft`, both already distinct.

**Note on two of these:** `sepa-mint` and `offrampr` already exist in
`data/pages.json` with earlier copy. Their prompts replace that entry rather than
adding a new one.

---

## Reviewing them side by side

The index at `/` lists every brand. From any brand page, the review switcher
bottom left jumps straight to another one. Keys: `[` previous, `]` next, `b`
index. It renders only while a page is `noindex`, so it disappears at launch.

## Prompt 0, orientation. Once per session.

```
The attached folder is the repo root. Every path below is relative to it.

Read, and write nothing yet:
CLAUDE.md
content/brand-homepages.md
data/brand-book.json
data/pages.json, two existing entries in full
assets/themes.css

CLAUDE.md is binding. Its three rules especially: never hand-edit brands/,
structure is shared and style is a theme and brand is an accent, and licence
language follows the brand book.

Then run:
  python3 scripts/build.py
  bash scripts/check.sh
  git remote -v

Report:
0. Whether origin points at https://github.com/knivef/payment-brand-wireframes
   and whether the working tree is clean. If there is no git repository or no
   origin yet, say so. Do not fix it, scripts/sync.sh wires it on first push.
1. The styles available in assets/themes.css and which brands already use each.
2. Which of the six brands in content/brand-homepages.md already have an entry in
   data/pages.json, and confirm the review switcher on an existing page lists
   every brand currently in data/pages.json.
3. The check.sh output.
4. Section 7 of content/brand-homepages.md lists nine open items. Tell me which
   of them block a build and which can ship as bracketed placeholders.

Stop and wait.
```

---

## 1. Swipe Wire Pay

```
Build the Swipe Wire Pay homepage.

Content source: content/brand-homepages.md, section 1. Read sections 0 and 7 as
well, they carry the shared conversion rules and the open items.
Read CLAUDE.md first. Read two existing entries in data/pages.json in full.

Style: ledger
Accent: #38bdf8, accent-fg #06121c, accent-soft rgba(56,189,248,0.13)
Slug: swipe-wire-pay

Skip the comparison table in the content file. Do not build that section.

Rules specific to this build:
- Swipe Wire Pay sells the bundle, not either half. The page argues that cards
  get the volume and the offramp gets the money out. If a section reads as
  equally true of Card Payz, rewrite it.
- Use the pricing table from the content file verbatim. Those numbers are from
  the price list. Do not round, restate or invent any of them.
- Card rates are blank in the price list. The page says "quoted per vertical
  after underwriting" and nothing more specific.
- Licence is None. No copy may state or imply one. Footer uses the "through
  licensed acquiring and payment partners" wording from the content file.
- Every [CONFIRM] in the content file stays as [CONFIRM: ...] in the page.
- No em dashes.

Build an estimator only for the offramp leg, since 2.5 percent all-in is a single
honest number. Do not estimate card cost, because the rate does not exist yet.

Add the entry to data/pages.json, then:
  python3 scripts/build.py swipe-wire-pay
  bash scripts/check.sh

Then push. This is not optional and not deferred to the end of the session:
  ./scripts/sync.sh "Add Swipe Wire Pay homepage"

Report every [CONFIRM] you left and what each one needs, confirm the push
succeeded and give me the repo URL it reported. Then start the preview server
detached and give me the local URL.
```

## 2. Card Payz

```
Build the Card Payz homepage.

Content source: content/brand-homepages.md, section 2. Read sections 0 and 7 too.
Read CLAUDE.md first. Read two existing entries in data/pages.json in full.

Style: stamp
Accent: #c6f24e, accent-fg #14110f, accent-soft rgba(198,242,78,0.16)
Slug: card-payz

There is no comparison table in this section and you should not add one.

Rules specific to this build:
- Cards only. The page must never mention crypto, stablecoins, offramp, wallets
  or crypto settlement, with one exception: FAQ item 6 in the content file, which
  answers the question and points elsewhere. Keep that answer short and leave the
  cross-link target as [CONFIRM].
- The four programmes (Level A, B, C, US) are the spine of the page. Use the
  published setup fees and the $149 monthly. Rates are blank in the price list,
  so the page says "quoted after underwriting".
- Render the four programmes as the pricing section using the published price
  table, not as generic cards.
- "What you need to apply" is a real conversion section in this vertical. Build
  it as its own block, using the compliance section keys.
- Licence is None. Footer uses the "connects merchants with licensed acquiring
  banks and payment institutions" wording from the content file.
- The stamp style sets uppercase H1 and H2. Check the H1 still reads at 375px and
  shorten it if it wraps to more than four lines.
- No em dashes.

No estimator. A programme ladder with no published rate cannot produce an honest
number, and a fake one would undercut the whole page.

Add the entry to data/pages.json, then:
  python3 scripts/build.py card-payz
  bash scripts/check.sh

Then push:
  ./scripts/sync.sh "Add Card Payz homepage"

Report every [CONFIRM] you left, confirm the push succeeded, and give me the repo
URL it reported. Then start the preview server detached and give me the local
URL.
```

## 3. Fiat Pay

```
Build the Fiat Pay homepage.

Content source: content/brand-homepages.md, section 3. Read sections 0 and 7 too.
Read CLAUDE.md first. Read two existing entries in data/pages.json in full.

Style: warm
Accent: #c2410c, accent-fg #ffffff, accent-soft rgba(194,65,12,0.09)
Slug: fiat-pay

No comparison table.

Rules specific to this build:
- The buyer is one person running a small Shopify or WooCommerce store, not a
  payments team. Short sentences, concrete nouns, no category jargon. If a line
  would need explaining to a store owner, rewrite it.
- The warm style runs an 18px body and a narrower container on purpose. Do not
  fight it with dense multi-column sections. Two columns maximum anywhere.
- Lead with "you can take cards again". The crypto-to-fiat part is the second
  beat, not the first.
- Use the pricing table from the content file. Crypto settlement is $0 setup,
  $250 monthly, 2.5 percent all-in, $1,000 to $500,000 per transfer. Card setup
  is [CONFIRM programme].
- Section 3 of the content file flags the RUO stance as unresolved. Build the
  "what we accept and what we do not" section with that whole paragraph as a
  [CONFIRM] block. Do not write a policy.
- Licence is None. Footer uses the "through licensed payment partners" wording.
- Keyword separation matters here. Fiat Pay targets "small store, get paid"
  terms. Pure Labs already owns the vetting and pre-screening terms. Do not use
  pre-screening, vetting or approvability language anywhere on this page.
- No em dashes.

Include an estimator for the crypto-to-fiat leg at 2.5 percent with the $250
monthly. At this buyer's volume the monthly fee dominates, and showing that
honestly is more persuasive than hiding it.

Add the entry to data/pages.json, then:
  python3 scripts/build.py fiat-pay
  bash scripts/check.sh

Then push:
  ./scripts/sync.sh "Add Fiat Pay homepage"

Report every [CONFIRM] you left, confirm the push succeeded, and give me the repo
URL it reported. Then start the preview server detached and give me the local
URL.
```

## 4. Sepa Mint, replaces the existing page

```
Rebuild the Sepa Mint homepage from the new content.

Content source: content/brand-homepages.md, section 4. Read sections 0 and 7 too.
Read CLAUDE.md first.

Sepa Mint already has an entry in data/pages.json. Replace it. Keep the slug
sepa-mint, keep style swiss, keep accent #d7263d. Everything else comes from the
new content file.

No comparison table.

Rules specific to this build:
- The new content is sharper than what is on the page now, especially the three
  EU problems: exchanges will not pay out EUR, banks bounce the transfer, MiCA
  added paperwork not solutions. Use that framing.
- Build the "For iGaming operators" section. It is the SBC play and it is the
  reason this brand exists. The CTA is "Book a meeting at SBC" with the event and
  link as [CONFIRM].
- Pricing: $0 setup, $250 monthly, 2.5 percent all-in either direction, broken
  down as crypto deposit 2 percent plus SEPA payout 0.5 percent. Show that
  breakdown, because the component view is what makes the headline credible.
- FAQ item 4 asks whether Sepa Mint is MiCA compliant. Do not answer it. Leave
  the whole answer as a [CONFIRM with legal] block. This is the highest risk line
  on any page in the repo.
- Licence is None. Footer uses the content file wording, including "Sepa Mint is
  not a bank".
- No em dashes.

Keep the estimator, updated to the breakdown above.

Update the entry in data/pages.json, then:
  python3 scripts/build.py sepa-mint
  bash scripts/check.sh

Then push:
  ./scripts/sync.sh "Rebuild Sepa Mint homepage from new content"

Show me a short diff summary of what changed from the previous version, report
every [CONFIRM], and confirm the push succeeded. Then start the preview server
and give me the local URL.
```

## 5. Offrampr, replaces the existing page

```
Rebuild the Offrampr homepage from the new content.

Content source: content/brand-homepages.md, section 5. Read sections 0 and 7 too.
Read CLAUDE.md first.

Offrampr already has an entry in data/pages.json. Replace it. Keep the slug
offrampr, keep style soft, keep accent #4f46e5.

No comparison table.

Rules specific to this build:
- Lead with who you pay, not how the rail works. The use case table in the
  content file, affiliates, players, traders, creators, suppliers, is the spine
  of the page. Build it as the segments section.
- Pricing comes from the content file and is more detailed than what is on the
  page now: $500 setup, $250 monthly, 1 percent or $30 per payout whichever is
  higher, SEPA payout 0.5 percent, crypto top-up 2 percent, crypto withdrawal
  0.5 percent, FX 0.15 percent plus bank FX, payout size $25 to $200,000. Show
  every line.
- Open item 3 in section 7 is a real pricing problem, not a copy problem: a $25
  payout costs $30, and top-up at 2 percent plus payout at 1 percent is about 3
  percent effective. Do not paper over it. In the estimator, show the effective
  rate including the top-up, and in the FAQ answer the cost question with the
  floor stated plainly. Then flag the problem to me in your report.
- Licence is None. Footer uses the content file wording.
- No em dashes.

Estimator: let me set both monthly payout volume and average payout size, so the
$30 floor becomes visible at small tickets. That is the most useful calculator on
any of these six pages.

Update the entry in data/pages.json, then:
  python3 scripts/build.py offrampr
  bash scripts/check.sh

Then push:
  ./scripts/sync.sh "Rebuild Offrampr homepage from new content"

Show me a short diff summary against the previous version, report every
[CONFIRM], give me your read on the pricing floor problem, and confirm the push
succeeded. Then start the preview server and give me the local URL.
```

## 6. Onrampr

```
Build the Onrampr homepage.

Content source: content/brand-homepages.md, section 6. Read sections 0 and 7 too.
Read CLAUDE.md first. Read two existing entries in data/pages.json in full.

Style: wire
Accent: #0f766e, accent-fg #ffffff, accent-soft rgba(15,118,110,0.09)
Slug: onrampr

No comparison table.

Rules specific to this build:
- This is the only brand of the six running fiat in, crypto out. Do not let the
  copy drift into offramp language. The buyer is a business buying stablecoins
  for treasury, suppliers or trading float.
- Two tiers, Standard and Large tickets, from the content file pricing table.
  Both carry a [CONFIRM] on the tier names and on whether the offramp "either
  direction" rates apply, per open item 4 in section 7. Put that [CONFIRM]
  visibly in the pricing note, not buried.
- The three problems are specific and good: banks block exchange transfers, OTC
  desks want six figures, retail onramps cap you. Keep that framing.
- Build the four use cases: pay suppliers in USDT, fund trading and float, hold a
  stablecoin treasury, fund payouts.
- Licence is None. Footer uses the content file wording, including "Onrampr is
  not a bank or investment adviser" and the volatility line.
- No em dashes.

Estimator with the two tiers as modes, 1.5 percent and 2.5 percent, and the $250
monthly on Standard only. The tier crossover point is the single most useful
thing this page can show a treasury buyer.

One more thing. Before you build, search the web for Onramper.com, an established
third-party fiat-to-crypto onramp aggregator. Our brand is Onrampr, one letter
off. Tell me in three sentences whether that is a trademark and SERP problem.
Do not soften it. Then build anyway, because the page is still worth having, but
I want the finding in writing.

Add the entry to data/pages.json, then:
  python3 scripts/build.py onrampr
  bash scripts/check.sh

Then push:
  ./scripts/sync.sh "Add Onrampr homepage"

Report every [CONFIRM], the Onramper finding, the tier crossover volume, and
confirm the push succeeded. Then start the preview server detached and give me
the local URL.
```

---

## After all six

```
All six homepages are built. Run a portfolio pass.

Read content/brand-homepages.md section 0 and section 7, and every entry in
data/pages.json.

1. Cannibalisation. Section 0 assigns each brand a distinct buyer and keyword
   set. Check the built pages against it. Flag any two pages whose H1, primary
   keyword or trust bar overlap enough that they would compete in search.
   Specifically check Swipe Wire Pay against Card Payz, and Fiat Pay against
   Pure Labs.

2. Clone risk. Open all six side by side at 1440 and 375. They share one
   stylesheet. Tell me honestly whether they read as six companies or as one
   template in six colours. If any two feel like siblings, say which and what
   would fix it.

3. Placeholder register. List every [CONFIRM] across all six, grouped by the
   nine open items in section 7, so I can see which single answer unblocks the
   most pages.

4. Licence sweep. All six have Licence None. Confirm no page states or implies
   one, and that every footer uses partner framing.

5. Navigation. Open the index at / and confirm all six appear with the right
   status, style and accent. Then open one brand page and step through the whole
   set with the ] key to confirm every switcher entry resolves.

Then run bash scripts/check.sh and give me the full output.

If anything changed as a result of this pass, push it:
  ./scripts/sync.sh "Portfolio pass across the six homepages"

Finish by confirming that https://github.com/knivef/payment-brand-wireframes is
up to date with everything built in this session, and list the commits made.
```
