# Prompt 01 - Research and content

Produces `brands/<slug>/brief.md`. Nothing gets built until this exists.

Paste the block below into Claude Code from the repo root, with the variables
filled in.

---

```
Research and write the content brief for a payment brand called BRAND_NAME.

Brand variables:
BRAND_NAME = ...
BRAND_SLUG = ...
DOMAIN = ...
ONE_LINER = ...
VERTICALS = ...
GEOGRAPHIES = ...
PRIMARY_BUYER = ...
KNOWN_COMPETITORS = ...
URGENCY_HOOK = ...

Read brands/_template/brief.md first. That file is the exact output structure.
Copy it to brands/BRAND_SLUG/brief.md and fill every field.

## Stage A - Competitor teardown

Identify five to eight direct competitors. Start from KNOWN_COMPETITORS and find
the rest by searching the way the buyer would search, not the way a marketer
would. Use the buyer's problem language: "processor that accepts X",
"X merchant account approval", "alternative to Y", "Y shut down my account".

For each competitor, fetch the homepage and record:
- The literal H1 and subhead, quoted
- The primary CTA verb and where it sits
- Section order, top to bottom, as a numbered list
- Whether pricing is shown, hidden behind a form, or absent
- Which social proof they use: logos, counts, testimonials, certifications
- Which urgency or scarcity devices they run, if any
- The single best line on the page, quoted, and why it works
- The single weakest thing about the page

Then find what buyers actually say. Search Reddit, Trustpilot, G2, industry
forums and Telegram-adjacent public sources for complaints about these
competitors and about the category. Quote real objections verbatim. These become
the FAQ and the objection handlers next to the form. Do not paraphrase them into
marketing language. The raw phrasing is the value.

## Stage B - Positioning

From the teardown, produce:

1. The table stakes list. Everything every competitor claims. These belong on
   the page but never in the H1, because they differentiate nothing.
2. The white space. What nobody in the category claims, that is true and
   provable for BRAND_NAME.
3. The wedge. One sentence we can say that competitors cannot. Then the
   mechanism sentence that makes the wedge believable. A wedge with no mechanism
   is a slogan and will not survive a sales call.
4. The enemy. The status quo, the incumbent, or the specific failure mode we are
   positioning against. Name it plainly.
5. A positioning statement in this form:
   For [buyer] who [situation], BRAND_NAME is the [category] that
   [differentiator]. Unlike [primary alternative], we [proof].

Pressure-test the wedge before you continue. If a competitor could put the same
sentence on their homepage tomorrow and it would be true, it is not a wedge.
Go back and find a sharper one.

## Stage C - Narrative

Write the seven-beat arc in section 4 of the brief: hook, problem, why existing
options fail, the shift, the mechanism, proof, the ask. Each beat must follow
from the one before it. If a reader can skip a beat and lose nothing, cut it.

## Stage D - Copy

Write every copy block in section 5 of the brief. Rules:

- Write for a buyer who has been burned before and is scanning for the catch.
- Concrete over abstract. "Reserve released on a six month lag" beats
  "transparent reserve terms".
- No em dashes. Use a full stop or a comma.
- No AI register: no "seamless", "robust", "unlock", "empower", "in today's
  landscape", "we understand that", "it's not just X, it's Y".
- The H1 states an outcome in under twelve words. Not a feature, not a category.
- Every claim is either verifiable or a bracketed placeholder. Nothing in
  between.
- The comparison table must include at least one row where we honestly lose or
  tie. A sweep reads as fiction and buyers discount the whole table.
- FAQ questions are phrased the way buyers search, not the way we would like
  them phrased.

## Stage E - Conversion layer

Fill section 6. For each conversion element, write the actual copy and state the
trigger. For urgency specifically: use URGENCY_HOOK if it is real. If it is not
real, write "none" and remove the countdown from the build. A fake deadline that
resets on refresh is the fastest way to lose a high-value buyer.

## Stage F - Claims register

Fill section 8. Every factual claim on the page gets a row with its source and
who verified it. List every bracketed placeholder still open. This is the
handover artefact, so be exhaustive rather than tidy.

## Output

Write brands/BRAND_SLUG/brief.md. Then show me, in chat, only these:
- The competitor table
- The wedge and its mechanism sentence
- The seven-beat narrative
- The list of open placeholders

Wait for my approval before touching any HTML.
```

---

## Notes

The teardown stage is the one worth spending tokens on. A brief built from three
competitors produces a page that sounds like those three competitors. Eight
competitors plus real buyer complaints produces a page that sounds like it was
written by someone who has sat in the deals.

If a vertical is one where public buyer complaints are thin, say so in the brief
rather than filling the section with inference presented as research.
