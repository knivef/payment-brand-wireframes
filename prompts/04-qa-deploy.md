# Prompt 04 - QA, commit and deploy

Run after the build. Nothing ships without this.

---

```
QA and ship the BRAND_SLUG wireframe.

## Stage A - Automated checks

Run scripts/check.sh and report the output. It checks for em dashes, unfilled
brackets outside the template folder, broken asset paths, registry JSON
validity and missing brand files.

If scripts/check.sh does not exist, run these directly from the repo root:

python3 -c "import pathlib,sys; hits=[(str(f),i+1,l) for f in pathlib.Path('.').rglob('*') if f.suffix in {'.html','.css','.js','.md','.json'} for i,l in enumerate(f.read_text(errors='ignore').split(chr(10))) if chr(8212) in l]; print(hits or 'no em dashes')"
grep -n "\[[A-Z][A-Z ]*\]" brands/BRAND_SLUG/index.html || echo "no open brackets"
python3 -c "import json,re,io; s=open('index.html').read(); m=re.search(r'id=\"brand-registry\" type=\"application/json\">(.*?)</script>', s, re.S); json.loads(m.group(1)); print('registry ok')"

## Stage B - Visual and behavioural QA

Serve the site and open the brand page in a browser. Check at 375px, 768px,
1280px and 1440px:

Layout
- No horizontal scroll at any width
- Comparison table switches to stacked cards below 820px and shows the same data
- Hero visual does not overflow or squash on mobile
- Footer columns reflow to two on tablet

Conversion mechanics
- Announcement bar shows, countdown runs, close button dismisses it and it stays
  dismissed on reload
- Nav gets its border after 32px of scroll
- Sticky bottom bar appears after the hero leaves the viewport, on mobile widths
  only
- Exit modal fires on a mouse-out at the top of the viewport, fires once, and
  closes on Escape, on the backdrop and on the close button
- FAQ accordion opens one item at a time
- Lead form: honeypot is hidden, a free email address is rejected with a visible
  message, a valid submit shows the inline success state and does not navigate
- Every reveal element becomes visible on scroll and is visible immediately with
  reduced motion on

Accessibility
- Exactly one h1
- Heading order runs h1, h2, h3 with no skips
- Full keyboard path through the page, every interactive element reachable, and
  a visible focus ring on each
- Accent on background and accent-fg on accent both clear WCAG AA
- Modal has role, aria-modal and an accessible label
- Decorative icons are aria-hidden

Content
- Every claim on the page has a row in the claims register in brief.md
- No invented figures, no testimonials without written consent, no
  certifications we do not hold
- The legal footer line matches the actual operating and licensing structure
- Title and meta lengths are within range

Report every failure with the file and line. Fix the ones that are clearly bugs.
Ask me about anything that is a copy or claims decision.

## Stage C - Index check

Open the root index and confirm the brand card renders with the right accent
swatch, status and tagline, and that clicking it lands on the brand page.

## Stage D - Commit and push

git add -A
git commit -m "Add BRAND_SLUG wireframe"
git push

Commit message rules: imperative mood, no em dashes, one line unless the change
needs a body.

## Stage E - Deploy

If the Vercel project is already linked, the push deploys it. Confirm the
deployment succeeded and print:
- The production URL for the index
- The direct URL for this brand page

If the project is not linked yet, run: vercel link, then vercel --prod, and
report the URLs.

Do not add a custom domain until I confirm the domain is registered and I want
it pointed here.
```

---

## A note on the noindex tag

Every brand page and the index carry `noindex, nofollow`, and `vercel.json`
sends an `X-Robots-Tag` header saying the same thing. That is deliberate while
these are wireframes: a half-finished payments page indexed under a brand name
is a problem that takes months to undo.

Remove both, for one brand at a time, only when that brand is launching on its
own domain.
