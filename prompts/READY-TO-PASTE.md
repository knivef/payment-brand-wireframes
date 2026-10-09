# Ready to paste

Every prompt below is filled in. Attach the repo folder, paste, run.

**Everything lands in https://github.com/knivef/payment-brand-wireframes.**
Every prompt that changes a file ends with `./scripts/sync.sh "<message>"`, which
runs the health check and refuses to push if it fails. Work that is not in that
repo is not done.

Run **Prompt 0** once at the start of a session. Then pick the brand you want.

Three groups, because they are not the same job:

- **Group A, Payments.** The existing template fits. 11 brands.
- **Group B, Provider Matching.** Directory and matching pages. The template does
  not cover these. 3 brands.
- **Group C, News and Media.** Content and review sites. Different page type
  entirely. 7 brands.

---

## Moving between pages

The index at `/` lists every brand. On any brand page the review switcher sits
bottom left: all brands, current one marked, prev and next. Keys: `[` previous,
`]` next, `b` index. It only renders while a page is `noindex`.

## Prompt 0, orientation. Once per session.

```
The attached folder is the repo root. Every path below is relative to it.

Read these, and do not write anything yet:
CLAUDE.md
README.md
prompts/01-add-brand.md
prompts/02-define-brand.md
data/brand-book.json
data/pages.json
assets/themes.css

CLAUDE.md is binding for this session. Its three rules especially: never
hand-edit brands/, structure is shared and style is a theme and brand is an
accent, and licence language follows the brand book.

Then run from the repo root:
  python3 scripts/build.py
  bash scripts/check.sh
  git remote -v

Report back:
0. Whether origin points at https://github.com/knivef/payment-brand-wireframes
   and whether the working tree is clean. If there is no repository or no origin
   yet, say so. Do not fix it, scripts/sync.sh wires it on first push.
1. The seven brands with pages, their style, licence and Burnable or Permanent.
2. Which brands in data/brand-book.json have no page yet, split into ones with a
   defined Sells and ones with an empty row.
3. The check.sh output including the open placeholder count per brand.
4. Anything in the setup that will break at twenty brands. Include whether the
   review switcher and the index page still work at that count, since both list
   every brand without pagination.

Then stop and wait.
```

---

# Group A, Payments

## A1. NexFlow

The only one here that is already defined, Live, and holds a licence.

```
Add a page for NexFlow to this repo.

Read CLAUDE.md, then the NexFlow row in data/brand-book.json, then two existing
entries in data/pages.json in full, then assets/themes.css.

NexFlow is different from the other seven in one important way: it sells to other
PSPs and acquirers, not to merchants. The buyer is a partnerships or BD lead at a
payment company, not a merchant owner. Do not reuse merchant-facing copy patterns.

It holds a Canadian MSB licence, which it may state. It is the only brand in the
book with that licence, so it is a differentiator, not a footnote.

Stage A. Report the book row, and tell me what is missing. NexFlow has no price
list and no pitch in the book. Ask me for what you need rather than inventing it.

Stage B. Propose a style and an accent. It must not read as a sibling of the
seven existing pages. Give me both WCAG contrast ratios. NexFlow is Permanent, so
this one is worth doing properly.

Stage C. Write the seven-beat arc for a PSP-to-PSP audience: hook, problem, why
the existing options fail, the shift, the mechanism, proof, the ask. The ask for
this audience is a partnership conversation, not a signup. Show me the arc and
wait.

Stage D. Build it into data/pages.json. No invented rates. The Canadian MSB
licence may be stated. No em dashes. No competitor comparison section. Then:
  python3 scripts/build.py nexflow
  bash scripts/check.sh
  ./scripts/sync.sh "Add NexFlow page"

Stage E. Report both contrast ratios, every [CONFIRM: ...] you left, anything in
the book row that contradicts what you wrote, and confirmation that the push
succeeded. Then start the preview server detached and give me the local URL.
```

## A2 to A11. The ten empty Payments rows

These have a name and a domain and nothing else. Define before building.

Run this one first, once, before any of the ten:

```
Before I define any more Payments brands, audit the ten empty rows against what
already exists.

Read CLAUDE.md and data/brand-book.json. The ten empty Payments rows are:
Swipe Wire Pay, Fiat Pay, Card Payz, Onrampr, Offramper, Pay Genex, Grey Lane,
Edge Line, High Stake, Stable Payments.

For each, tell me in one line what the name and domain imply it would sell, and
which existing brand in the book already occupies that position.

Then group them: which are genuine gaps, which are duplicates of a brand that
already has a page, and which are domain renewals with no distinct buyer.

Two specific checks:
- Offramper (offramper.io) against Offrampr (offrampr.com), which already has a
  page. Are these two brands or one brand and a defensive domain registration?
- Onrampr (onrampr.com) against Onramper.com, which is an established third-party
  onramp aggregator. Search the web and tell me plainly whether that name is
  viable, including trademark and SERP overlap.

End with a recommended build order for the ones worth building, and a list of the
ones I should leave as parked domains. Do not soften the second list.
```

Then, per brand, substitute the name into this:

```
Define BRAND_NAME (DOMAIN) well enough to build a page for it.

Read CLAUDE.md and data/brand-book.json first. Find the row and every row near it.
The portfolio is the constraint.

Stage A. List every brand in the book that sells into the same space, with its
Sells line, target industries and price list. Say plainly which positions are
occupied and cannot be reused. If this brand is a duplicate of one that already
exists under a different name, say so. Not every row in the book needs a page.

Stage B. Exactly three definitions. For each: Sells in one line in the style of
the existing Sells column; target industries from the Lists tab values; which
existing price list it would use and why; the pitch line in one sentence; who the
buyer is, specific enough that I could name three companies; what makes it not a
duplicate of its nearest sibling; why the other two options are worse.

Use the existing price lists. A brand that needs a list the book does not have is
a different conversation, so say so rather than invent one.

Stage C. Two sentences on whether this brand should exist at all. A burnable brand
with no distinct buyer is a domain renewal, not a business. Say that if it is true.

Stop. I choose, then we run prompts/01-add-brand.md.
```

Brand and domain pairs to substitute:

| Brand | Domain | Priority in book |
|---|---|---|
| Swipe Wire Pay | swipewirepay.com | Medium |
| Fiat Pay | fiatpay.io | Medium |
| Grey Lane | greylanepayments.com | Medium |
| High Stake | highstakepayments.com | Medium |
| Card Payz | cardpayz.com | none set |
| Onrampr | onrampr.com | none set |
| Offramper | offramper.io | none set |
| Pay Genex | paygenex.com | none set |
| Edge Line | edgelinepayments.com | none set |
| Stable Payments | stablepayments.io | none set |

Build the four marked Medium first. The rest are unprioritised in your own book,
which is itself an answer.

---

# Group B, Provider Matching

Ramp Match, Crypto Atlas and Ramp Stack are not product pages. The existing
template does not fit them. Run this before building any of the three.

```
Three brands in data/brand-book.json are category "Provider Matching" and none of
them fit the current page template:

- Ramp Match (rampmatch.com), "Provider matching engine system"
- Crypto Atlas (cryptoatlas.ai), "Crypto On/off ramping providers only"
- Ramp Stack (rampstack.io), "Hosting services for payram"

Read CLAUDE.md, data/brand-book.json and brands/zepapay/index.html.

Stage A. For each of the three, tell me what page type it actually needs. Ramp
Stack looks like a product page and may fit the existing template. The other two
look like directory or comparison products, which need provider rows, filters and
a methodology page, none of which exist in assets/base.css.

Stage B. There is a conflict to resolve. I own Zepapay, Secure Payment Services,
Offrampr, Sepa Mint and AltPay, all of which are offramp or settlement providers.
If Ramp Match or Crypto Atlas ranks or compares providers and any of mine appear,
common ownership has to be disclosed on the page itself, next to the listing.

Tell me how credible fintech comparison sites handle this, quoted, and draft an
ownership disclosure line for me to approve. If the honest answer is that we
cannot credibly rank our own brands on a site we own, say so. Excluding them is a
valid answer.

Stage C. Propose how to add a second template, brands/_template-directory, sharing
the same tokens, the same themes.css and the same conversion.js, rather than
growing the existing template to cover both. Tell me which reusable classes go in
assets/base.css and what scripts/build.py needs to render it.

Do not build anything yet. Show me the plan and stop. Nothing to push on this
one, it is a read-only pass.
```

---

# Group C, News and Media

Seven content and review sites. Wrong product entirely for the current repo.

```
Seven brands in data/brand-book.json are category "News & Media":

- Wire 2 Casino (wire2casino.com), wire solutions for casinos
- Wire 2 Win (wire2win.com), wire solutions for VIP players and casinos
- Wire 2 Bet (wire2bet.com), wire solutions for gambling
- Wire 2 Trade (wire2trade.com), paying for crypto and forex trading
- Pay 4 FX (pay4fx.com), payment solutions and reviews for forex
- Pay 4 Casino (pay4casino.com), top casino games and offers
- Pay 4 Bitcoins (pay4bitcoins.com), buying crypto from non-KYC websites

Read CLAUDE.md and data/brand-book.json.

Stage A. These are content sites, not product pages. Say what each one actually
is: an SEO content play feeding leads to the payment brands, an affiliate site, or
a review directory. Tell me which of the three models each name fits best.

Stage B. There is significant overlap. Wire 2 Casino, Wire 2 Win and Wire 2 Bet
all point at gambling wires. Tell me honestly how many distinct sites this set
supports and which names are redundant.

Stage C. Pay 4 Bitcoins says "non KYC websites". Flag the compliance exposure of
publishing content that helps people avoid KYC, in plain terms, including how it
sits against the licensed brands in the same portfolio. This is the highest risk
item in the whole book and I want it named rather than built around.

Stage D. If any of these are worth building, propose what a content site template
needs that this repo does not have: article listing, article page, author and
disclosure, category pages. Propose it as a third template rather than growing the
existing one.

Do not build anything. Show me the analysis and stop. Nothing to push on this
one, it is a read-only pass.
```

---

# Maintenance

## After editing the workbook

```
I have updated Brand_Book.xlsx. Re-extract and rebuild.

  python3 scripts/import-book.py <path to the xlsx>
  python3 scripts/build.py
  bash scripts/check.sh

Report every rate that changed and which brand pages it affected. If a licence
value changed for any brand, tell me which pages need their copy reviewed before
the next deploy.

Then push, with the rate changes named in the message:
  ./scripts/sync.sh "Update rates from the brand book: <what changed>"
```

## A/B a design style

```
I want to test BRAND_NAME in a second style.

Copy its entry in data/pages.json. On the copy set slug to BRAND_SLUG-alt and
style to STYLE_NAME. Change nothing else, because the point is to isolate the
design variable.

Check the accent still clears WCAG AA on the new style's background. If it does
not, propose a shifted accent and give me both ratios before you build.

Rebuild, run the check, then push:
  ./scripts/sync.sh "Add BRAND_SLUG-alt in the STYLE_NAME style for an A/B"

Give me both local URLs side by side and confirm the push succeeded.
```

Styles available: `terminal`, `swiss`, `brutal`, `soft`, `midnight`, `clinical`,
`mono`.

## Clear placeholders before a brand goes public

```
BRAND_NAME is going public. Walk me through every [CONFIRM: ...] on its page.

For each: what it says now, what it needs, and who signs it off. Do not write a
replacement for a licensing line. Draft the question for legal instead.

Then tell me what else has to change for launch: the noindex meta tag on the page,
the X-Robots-Tag header in vercel.json, and whether the published pricing on this
page is cleared for public display. Do not remove noindex repo-wide, only for this
brand.

Do not change anything yet. When I approve the list, make the changes and push:
  ./scripts/sync.sh "Prepare BRAND_NAME for launch"
```

## Push and deploy

```
Push everything to https://github.com/knivef/payment-brand-wireframes.

  ./scripts/sync.sh "<imperative, one line, no em dashes>"

The script runs scripts/check.sh first and refuses to push if it fails. It wires
origin on the first run, so a fresh folder needs no setup. Do not push with raw
git commands, because that skips the check.

If the push is rejected because the remote has moved ahead, pull with rebase,
rerun the check, and push again. Do not force push.

If the push fails for any other reason, tell me what the error was and stop. Do
not carry on with the next task with unpushed work sitting locally.

When it succeeds, give me the repo URL and the commit message you used.
```

## Session close

```
Before we finish, confirm the repo is clean and current.

  git status --short
  git log --oneline -10
  git remote -v

Tell me:
- Whether anything is uncommitted or unpushed. If there is, run
  ./scripts/sync.sh with a message that describes it.
- The commits made this session.
- That origin is https://github.com/knivef/payment-brand-wireframes.

If the working tree is clean and everything is pushed, say so in one line.
```
