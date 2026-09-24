# CLAUDE.md

Repo context. Claude Code loads this automatically. Read it before any task here.

## What this repo is

A multi-brand payment wireframe repo. The base URL is an index of every brand.
Each card links to `/brands/<slug>/`, a standalone conversion wireframe.

Plain HTML and CSS. No framework, no bundler, no build step. Vercel serves it
as static output. Do not introduce a build step, a package manager or a
JavaScript framework. If a task seems to need one, stop and ask.

## Layout

```
index.html              Brand index. Renders from the inline JSON block id="brand-registry".
vercel.json             Clean URLs, cache headers, noindex while wireframing.
assets/base.css         ALL structural CSS. Shared by every brand.
assets/conversion.js    Sticky bars, countdown, exit intent, accordion, forms.
brands/_template/       Fork this for a new brand. Never ship it, never edit it casually.
brands/<slug>/          index.html, brand.css, brief.md
prompts/                The four-stage build chain. Read before building.
scripts/check.sh        Health check. Run before every push.
scripts/bootstrap.sh    One-time gh repo create plus vercel link.
```

## The two architectural rules

**1. Structure is shared, brand is tokens.**
`assets/base.css` owns every layout rule. A brand's `brand.css` may set only:
`--accent`, `--accent-fg`, `--accent-soft`, `--bg`, `--surface`, `--surface-2`,
`--radius`, `--radius-sm`, `--radius-lg`, `--font-sans`.

If a brand needs a layout treatment base.css does not have, add a reusable class
to `base.css` and tell the user you did it. Never add a layout rule to a brand
folder. `scripts/check.sh` fails the build if you do.

**2. The brief is the only input to the build.**
`brands/<slug>/brief.md` is the source of truth for copy, claims, positioning
and SEO. If something is not in the brief, it does not go on the page. Copy
decisions get made in the brief, in markdown, where they are reviewable.

## Workflow for a new brand

Run the prompts in order. Stop at each gate.

| Stage | Prompt | Output |
|---|---|---|
| 1 | `prompts/01-research.md` | `brands/<slug>/brief.md` sections 1 to 6 and 8 |
| 2 | `prompts/02-seo.md` | brief section 7 |
| 3 | `prompts/03-wireframe.md` | `brands/<slug>/index.html` and `brand.css`, plus a registry entry |
| 4 | `prompts/04-qa-deploy.md` | QA report, commit, deploy |

`prompts/00-orchestrator.md` runs all four with approval gates.

## House rules

These are non-negotiable. They apply to code, copy, comments and commit messages.

- **No em dashes.** Anywhere. Use a full stop or a comma. `check.sh` enforces it.
- **No invented facts.** Never write a merchant count, a processing volume, a
  testimonial, a certification, a partner name or a compliance claim that has not
  been verified. Unverified content stays as a literal `[BRACKETED PLACEHOLDER]`
  and gets a row in the claims register in `brief.md`.
- **No AI register.** Banned: seamless, robust, unlock, empower, leverage,
  landscape, "in today's", "we understand that", "it's not just X, it's Y",
  "designed to", "tailored to". Write the way someone who has closed these deals
  would write.
- **The comparison table must contain at least one row where the brand honestly
  loses or ties.** A table the brand sweeps reads as fiction and buyers discount
  all of it.
- **Delete the proof section rather than publish placeholder figures.**
- **Drop the countdown rather than invent a deadline.**
- **Every page keeps `noindex` until that specific brand launches** on its own
  domain. Remove it one brand at a time, never repo-wide.

## Conventions

- Section order in a brand page is fixed by the template. Sections may be
  deleted. They may not be reordered, and a new one needs a reason.
- Keep every data attribute the template uses. `conversion.js` binds to
  `data-nav`, `data-announce`, `data-countdown`, `data-stickybar`,
  `data-stickybar-after`, `data-modal`, `data-exit-intent`, `data-lead-form`,
  `data-cta` and silently does nothing if they are missing.
- Give every CTA a distinct `data-cta` label so clicks are attributable.
- Set `data-key` on the announcement bar, countdown and exit modal to the brand
  slug plus a version suffix, so dismissals do not leak between brands sharing a
  preview domain.
- The comparison table renders twice, a real table and a stacked card fallback
  under 820px. Populate both with the same data.
- FAQ copy on the page and FAQ copy in the FAQPage JSON-LD come from one source.
  They must not drift.
- Commit messages: imperative mood, one line, no em dashes.

## Local preview

Pages link `/assets/base.css` with an absolute path, so `file://` will not
render them. They need a server.

```bash
python3 -m http.server 4321
# index:  http://localhost:4321/
# brand:  http://localhost:4321/brands/<slug>/
```

If you are running in Cowork, where each shell call is short-lived, start it
detached and tell the user the URL to open in their own browser:

```bash
cd "<repo root>" && nohup python3 -m http.server 4321 >/dev/null 2>&1 &
```

If that server does not survive, do not fight it. Ask the user to run the
command in their own Terminal, or push the branch and review the Vercel preview
URL instead.

Add `class="wf"` to a brand page's `<body>` to strip colour and shadow and
review structure alone. Remove it before committing.

## Running in Cowork with the folder attached

The attached folder is the repo root. Everything in this file still applies.
Two differences:

- This file is not loaded automatically. Read it first, before anything else.
- Each shell call is a fresh short-lived shell. Do not rely on a previous call's
  working directory or background process. Anchor paths from the repo root every
  time, and split long jobs into steps.

## Before every push

```bash
./scripts/check.sh
```

It checks for em dashes, open placeholders in shipped brands, brand registry
validity, required files per brand, shared asset links, and layout rules leaking
into a brand's `brand.css`.

## Ask, do not assume

Stop and ask the user when:

- A claim needs a number nobody has verified
- The brief and the layout conflict, so copy would have to change
- A task seems to need a framework, a build step or a dependency
- A brand's accent colour fails WCAG AA and the fix changes the brand
- The legal or licensing disclosure line needs to say something specific
