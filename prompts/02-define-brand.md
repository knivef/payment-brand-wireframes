# Prompt 02 - Define a brand that has an empty book row

For the brands that exist as a name and a domain and nothing else. Produces the
missing fields, which then go into the brand book and into prompt 01.

Competitor comparison is out of scope. This is about deciding what the brand is,
not about benchmarking it.

---

```
Define BRAND_NAME well enough to build a page for it.

Read CLAUDE.md and data/brand-book.json first. Find the row for BRAND_NAME and
every row near it, because the portfolio is the constraint here.

## Stage A, what is already taken

List, from the book, every brand that already sells into the same space. For each,
give its Sells line, its target industries and its price list. Then tell me plainly
which positions are occupied and cannot be reused.

Specifically check: is this brand a duplicate of one that already exists with a
different name? If it is, say so. Not every row in the book needs a page.

## Stage B, three options

Give me exactly three definitions for BRAND_NAME. For each:
- Sells, one line, in the style of the existing Sells column
- Target industries, from the Lists tab values where possible
- Which existing price list it would use, and why that one fits
- The pitch line, one sentence
- Who the buyer is, specific enough that I could name three companies
- What makes it not a duplicate of its nearest sibling
- Why the other two options are worse

Use the existing price lists rather than inventing a new one. A brand that needs a
price list the book does not have is a different conversation, and you should say
so rather than make one up.

## Stage C, the honest answer

After the three options, tell me in two sentences whether you think this brand
should exist at all, given what is already in the book. A burnable brand with no
distinct buyer is a domain renewal, not a business. Say that if it is true.

Stop there. I choose, then we run prompts/01-add-brand.md.
```

---

## After I choose

Update the row in `data/brand-book.json` with the chosen Sells, industries, price
list and pitch, then run prompt 01. Keep the xlsx and the JSON in step: the xlsx
is still the thing kvn edits, the JSON is what the build reads.

To re-extract after editing the workbook:

```bash
python3 scripts/import-book.py path/to/Brand_Book.xlsx
```
