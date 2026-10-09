# Prompt 00 - Orchestrator

Run this one prompt in Claude Code from the repo root to execute the whole
chain for a single brand. It calls the other four prompts in order and stops at
each gate for your approval.

If you prefer manual control, skip this and run `01` through `04` yourself.

---

## Variables

Fill these in before pasting. Everything downstream reads from here.

```
BRAND_NAME      = [e.g. Swipe Wire Pay]
BRAND_SLUG      = [e.g. swipe-wire-pay, lowercase, hyphens, no spaces]
DOMAIN          = [e.g. swipewirepay.com, or "not registered yet"]
ONE_LINER       = [one sentence on what the brand does]
VERTICALS       = [e.g. iGaming, adult, peptides, nutra]
GEOGRAPHIES     = [e.g. EU, UK, LATAM]
PRIMARY_BUYER   = [role and company type]
ACCENT_COLOUR   = [#hex, or "pick one and justify it"]
KNOWN_COMPETITORS = [3 to 8 URLs, or "find them"]
URGENCY_HOOK    = [what is genuinely time-bound, or "none, drop the countdown"]
```

---

## The prompt

```
You are building a conversion wireframe for a payment brand in this repo.

Brand variables:
BRAND_NAME = ...
BRAND_SLUG = ...
DOMAIN = ...
ONE_LINER = ...
VERTICALS = ...
GEOGRAPHIES = ...
PRIMARY_BUYER = ...
ACCENT_COLOUR = ...
KNOWN_COMPETITORS = ...
URGENCY_HOOK = ...

Read these files before you start, in this order:
1. README.md
2. prompts/01-research.md
3. prompts/02-seo.md
4. prompts/03-wireframe.md
5. prompts/04-qa-deploy.md
6. brands/_template/index.html
7. brands/_template/brief.md
8. assets/base.css

House rules that override anything else:
- No em dashes anywhere. Not in copy, not in comments, not in commit messages.
- Never invent a number, a merchant count, a volume figure, a testimonial or a
  certification. Anything unverified stays as a literal [BRACKETED PLACEHOLDER]
  and gets logged in the claims register in brief.md.
- Structural CSS lives only in assets/base.css. A brand folder may contain token
  overrides in brand.css and nothing else.
- Every page is plain HTML and CSS. No build step, no framework, no bundler.

Execute in four stages. Stop and wait for my approval between each one.

STAGE 1 - Research. Follow prompts/01-research.md. Write the output to
brands/BRAND_SLUG/brief.md. Show me sections 2, 3 and 4 of the brief and wait.

STAGE 2 - SEO. Follow prompts/02-seo.md. Fill section 7 of the brief. Show me
the keyword table and the title and meta and wait.

STAGE 3 - Build. Follow prompts/03-wireframe.md. Create
brands/BRAND_SLUG/index.html and brands/BRAND_SLUG/brand.css from the template,
filling every bracket from the brief. Register the brand in the JSON block in
index.html at the repo root. Then start a local server and tell me the URL.

STAGE 4 - QA and ship. Follow prompts/04-qa-deploy.md. Run every check, report
the results, then commit and push.

Start with Stage 1.
```

---

## Gates, and why they exist

| Gate | What you are checking |
|---|---|
| After research | Is the wedge real, or did it invent a differentiator we cannot back? |
| After SEO | Does the primary keyword match how buyers actually search, and can we rank for it? |
| After build | Does the page read as one argument, or as a list of sections? |
| After QA | Are any placeholders still live, and is the claims register complete? |

Skipping a gate costs more time than it saves. The research gate in particular
is where a wrong wedge gets caught, and a wrong wedge means rewriting the whole
page.
