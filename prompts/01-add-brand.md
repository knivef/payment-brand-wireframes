# Prompt 01 - Add a brand

The brand book now carries the positioning, the price list and the pitch, so most
of what the old research chain produced already exists. This prompt fills the gap
between a row in the book and a page.

Competitor comparison is deliberately out of scope.

---

```
Add a page for BRAND_NAME to this repo.

Read first, in this order:
1. CLAUDE.md
2. data/brand-book.json, and find the row for BRAND_NAME
3. data/pages.json, and read two existing entries in full
4. assets/themes.css

Do not write anything yet.

## Stage A, read the book row and report

From data/brand-book.json tell me, for BRAND_NAME:
- Sells, target industries, channels
- Which price list or lists it uses, and the actual numbers on them
- Which pitch it uses, and the pitch line
- Licence held, status, type (Burnable or Permanent), priority

Then say what is missing. A row with no Sells and no pitch needs those from me
before you build anything. Ask for them in one short list rather than inventing
them.

## Stage B, pick a style and justify it

Propose one style from assets/themes.css and say why in two sentences, including
which brands already use it and why that is or is not a problem. Then propose an
accent that works on that style's background and passes WCAG AA for both
accent-on-background and accent-fg-on-accent. Give me the two contrast ratios.

If the brand is Burnable, say so and keep the build light. A burnable brand gets
one page and no content backlog.

## Stage C, narrative

Write the seven-beat arc before any copy: hook, problem, why the existing options
fail, the shift, the mechanism, proof, the ask. Ground it in the pitch line from
the book and the real numbers from the price list. Show me the arc and wait.

## Stage D, build

Add one entry to data/pages.json following the shape of the existing entries.
Rules:

- Every price figure comes from the price list in data/brand-book.json. Do not
  type a rate that is not in the book.
- If the brand holds no licence, no copy may state or imply one. Partner framing
  is allowed, and the partner entity stays as [CONFIRM: ...].
- No em dashes.
- Include an estimator only if there is a single headline percentage that makes
  the arithmetic honest. A tiered or floor-based price list usually does not.
- Set a telegram_cta if the book lists TG as a channel.
- Section keys are optional. Omit a section rather than fill it with filler.

Then run:
  python3 scripts/build.py BRAND_SLUG
  ./scripts/check.sh

## Stage E, report

Tell me:
- The two contrast ratios
- Every [CONFIRM: ...] you left, and what each one needs
- Which price list figures you used and where each one came from
- Anything in the book row that contradicts what you wrote

Then start the preview server detached and give me the URL.
```

---

## When the book row is empty

Several brands in the book have no Sells, no target and no pitch: Onrampr,
Offramper, Card Payz, Swipe Wire Pay, Fiat Pay, Pay Genex, Grey Lane, Edge Line,
High Stake, Stable Payments.

Those need a definition before a page. Use `prompts/02-define-brand.md`.
