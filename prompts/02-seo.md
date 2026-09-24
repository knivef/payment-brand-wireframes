# Prompt 02 - SEO and keyword layer

Fills section 7 of `brands/<slug>/brief.md`. Run after research, before build.

Requires the Ubersuggest MCP server. If it is not connected, the prompt falls
back to search-based keyword discovery and marks every volume figure as
estimated.

---

```
Fill the SEO section of brands/BRAND_SLUG/brief.md.

Read brands/BRAND_SLUG/brief.md first. The positioning and the buyer language in
sections 2 and 3 are your seed set. Do not invent seed keywords from the brand
name alone.

## Stage A - Seed set

Build the seed list from three sources:
1. The buyer's problem language quoted in section 2 of the brief.
2. The category terms competitors rank for.
3. The objection phrasings from the forum research.

For each named competitor domain, run domain_overview and domain_keywords. Pull
their top thirty organic keywords. This is the highest-signal input you have,
because it is what already works in this category.

## Stage B - Expansion and metrics

For each seed, run keyword_suggestions and keyword_overview. Capture volume,
SEO difficulty, paid difficulty and CPC. CPC matters here: in payments, a high
CPC on a low-volume term usually means the term converts, which makes it a
better page target than a high-volume informational term.

Run serp_analysis on the top three candidates. Record who ranks, what page type
ranks (homepage, product page, listicle, forum thread) and the domain authority
spread. If the first page is all DR 70+ publishers, the term is a blog target,
not a homepage target. Say so and pick again.

## Stage C - Selection

Choose:
- One primary keyword. Commercial intent, realistic difficulty for a new domain,
  and it must describe what the buyer is actually trying to buy. Volume is the
  third consideration, not the first.
- Three to five secondary keywords that can sit naturally in H2s.
- Six to ten question keywords for the FAQ, taken from google_suggestions and
  from People Also Ask patterns in the SERP data.

Justify the primary keyword choice in two sentences, including what you rejected
and why.

## Stage D - On-page assets

Write:
- Title tag, 55 to 60 characters, primary keyword first, brand last.
- Meta description, 150 to 158 characters, containing the primary keyword and
  the CTA verb. Written to earn a click, not to describe the page.
- H1 that contains or closely matches the primary keyword while still passing
  the under-twelve-words outcome test from the research prompt. If the keyword
  and the outcome fight each other, the outcome wins and the keyword moves to
  the H2. Say which you chose.
- Internal link targets: the three to five pages this brand should build next,
  each with its own keyword. These go in the brief as a backlog, not on the page.

## Stage E - Schema

Specify the JSON-LD to emit in the build:
- Organization, with the legal entity name and the actual operating structure.
- FAQPage, generated from the same FAQ copy that renders on the page. The two
  must not drift.
- BreadcrumbList.

## Output

Update section 7 of brands/BRAND_SLUG/brief.md. Show me the keyword table with
volume, difficulty and CPC, plus the title and meta, and wait for approval.

If the Ubersuggest MCP is unavailable, say so explicitly, gather keywords by
search instead, and label every volume figure "estimated, unverified" in the
brief. Do not present an estimate as a measurement.
```

---

## Notes

The trap in this category is chasing high-volume head terms like "payment
gateway". You will not rank and the traffic does not convert. The terms that
build a pipeline are the ones with intent baked in: the vertical plus the
product, or the failure mode plus the fix.

The second trap is a title tag written for the crawler. In payments the SERP is
crowded with near-identical titles, so the differentiator in the meta
description is doing more work than the keyword placement.
