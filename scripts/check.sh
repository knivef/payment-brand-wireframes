#!/usr/bin/env bash
# Repo health check. Run from the repo root: ./scripts/check.sh
# Exits non-zero if anything fails, so it works as a pre-push hook or CI step.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

FAIL=0
pass() { printf "  ok    %s\n" "$1"; }
fail() { printf "  FAIL  %s\n" "$1"; FAIL=1; }

echo "Payment brand wireframes, health check"
echo

# 1. Em dashes
echo "1. Em dashes"
HITS=$(python3 -I - <<'PY'
import pathlib
bad=[]
for f in pathlib.Path('.').rglob('*'):
    if f.suffix in {'.html','.css','.js','.md','.json','.py','.sh'} and '.git' not in f.parts:
        for i,l in enumerate(f.read_text(errors='ignore').split('\n')):
            if chr(8212) in l: bad.append(f"{f}:{i+1}")
print('\n'.join(bad))
PY
)
if [ -n "$HITS" ]; then fail "em dashes found:"; echo "$HITS" | sed 's/^/        /'; else pass "none found"; fi
echo

# 2. Generated pages are in sync with data/
echo "2. Generated output is current"
TMP=$(mktemp -d)
cp -r brands "$TMP/brands" 2>/dev/null
cp index.html "$TMP/index.html" 2>/dev/null
cp vercel.json "$TMP/vercel.json" 2>/dev/null
python3 -I scripts/build.py >/dev/null 2>&1 || fail "build.py errored"
for t in brands index.html vercel.json; do
  if diff -rq "$TMP/$t" "$t" >/dev/null 2>&1; then
    pass "$t matches data/"
  else
    fail "$t was stale. Regenerated, review and commit the diff."
  fi
done
rm -rf "$TMP"
echo

# 3. Open placeholders, every bracket form
echo "3. Open placeholders"
python3 -I - <<'PY2'
import os, re
# Any bracketed span that reads as an instruction is a placeholder, whatever the
# keyword. The old check looked for CONFIRM, PLACEHOLDER and REAL NUMBER only,
# and missed "[This section needs legal review before launch.]".
PAT = re.compile(r"\[(?:[A-Z][^\]]{3,}|[Tt]his [^\]]{10,})\]")
total = 0
for slug in sorted(os.listdir("brands")):
    path = os.path.join("brands", slug, "index.html")
    if not os.path.isfile(path):
        continue
    html = open(path, encoding="utf-8").read()
    html = re.sub(r'<script id="brand-nav".*?</script>', " ", html, flags=re.S)
    hits = PAT.findall(html)
    total += len(hits)
    if hits:
        print("  note  %s: %d open" % (slug, len(hits)))
        for h in sorted(set(hits)):
            print("          " + h[:100])
    else:
        print("  ok    %s clean" % slug)
print("        %d open across all brands. Each needs a claims-register row." % total)
PY2
echo

# 4. Brand registry
echo "4. Brand registry"
python3 -I - <<'PY'
import json, os, re, sys
src = open("index.html", encoding="utf-8").read()
m = re.search(r'id="brand-registry" type="application/json">(.*?)</script>', src, re.S)
if not m: print("  FAIL  registry block not found"); sys.exit(1)
try: data = json.loads(m.group(1))
except Exception as ex: print(f"  FAIL  invalid JSON: {ex}"); sys.exit(1)
print(f"  ok    valid JSON, {len(data)} brand(s)")
bad = 0
for b in data:
    if not os.path.isdir(os.path.join("brands", b.get("slug",""))):
        print(f"  FAIL  {b.get('slug')} has no folder"); bad = 1
    if not os.path.isfile(os.path.join("assets","themes.css")): continue
    styles = open("assets/themes.css", encoding="utf-8").read()
    if f'[data-style="{b.get("style")}"]' not in styles:
        print(f"  FAIL  {b.get('slug')} uses style '{b.get('style')}' which is not in themes.css"); bad = 1
if not bad: print("  ok    every entry has a folder and a real style")
sys.exit(bad)
PY
[ $? -ne 0 ] && FAIL=1
echo

# 5. Licence discipline, per brand
echo "5. Licence discipline"
python3 -I - <<'PY2'
import json, os, re, sys
book = json.load(open("data/brand-book.json", encoding="utf-8"))
pages = json.load(open("data/pages.json", encoding="utf-8"))["pages"]
lic = {b["brand"].strip().lower(): (b.get("licence") or "None") for b in book["brands"]}

# Safe on any unlicensed brand.
SHARED = (
    "[confirm",
    "partnership with licensed", "through licensed", "licensed payment partner",
    "licensed payment institution", "licensed partner", "licensed acquiring",
    "licensed issuer", "licensed technology", "licensed partners",
    "does not hold a licence", "a licence of its own", "not a payment processor",
    "not a bank",
    # the merchant's licence, not ours
    "licence jurisdiction", "licence where", "licence position", "your licence",
    "regulated brokers", "need a licence", "require one",
)
# Per-brand exceptions. Each needs a reason. Adding one is a decision, not a fix.
PER_BRAND = {
    # "slug": [("phrase", "why this is allowed on this brand")],
}

CLAIMS = re.compile(r"\b(licensed|licence|license|authorised|authorized|regulated)\b", re.I)
bad = 0
for p in pages:
    key = (p.get("book_key") or p["name"]).strip().lower()
    held = lic.get(key, "None")
    path = os.path.join("brands", p["slug"], "index.html")
    if not os.path.isfile(path):
        continue
    if held != "None":
        print("  ok    %s holds %s" % (p["slug"], held))
        continue

    html = open(path, encoding="utf-8").read()
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)

    allowed = tuple(SHARED) + tuple(x[0].lower() for x in PER_BRAND.get(p["slug"], []))
    findings = []
    # Sentences, not lines, so a claim split across a line break is still caught.
    for sent in re.split(r"(?<=[.!?]) ", text):
        if not CLAIMS.search(sent):
            continue
        # An FAQ question is not a claim. "Are you licensed in the EU?" is the
        # question; what matters is whether the answer is bracketed, and the
        # answer is its own sentence and gets checked on its own.
        if sent.rstrip().endswith("?"):
            continue
        low = sent.lower()
        if any(a in low for a in allowed):
            continue
        findings.append(sent.strip())
    if findings:
        print("  FAIL  %s holds no licence but makes licence claims:" % p["slug"])
        for f in findings[:4]:
            print("          " + f[:130])
        bad = 1
    else:
        print("  ok    %s (no licence) every claim bracketed or partner framed" % p["slug"])
sys.exit(bad)
PY2
[ $? -ne 0 ] && FAIL=1
echo

# 6. Shared asset links and brand.css hygiene
echo "6. Assets and brand.css"
for dir in brands/*/; do
  slug=$(basename "$dir")
  [ -f "$dir/index.html" ] || continue
  for a in /assets/base.css /assets/themes.css /assets/conversion.js /assets/review.js; do
    grep -q "$a" "$dir/index.html" || fail "$slug does not link $a"
  done
  STRAY=$(grep -nE '^[^/ \t}].*\{' "$dir/brand.css" 2>/dev/null | grep -vE ':root|\[data-theme' || true)
  if [ -n "$STRAY" ]; then fail "$slug/brand.css has non-token rules"; else pass "$slug ok"; fi
done
echo

# 7. Review switcher
echo "7. Review switcher"
python3 -I - <<'PY2'
import json, os, re, sys
slugs = sorted(d for d in os.listdir("brands") if os.path.isdir(os.path.join("brands", d)))
bad = 0
for slug in slugs:
    path = os.path.join("brands", slug, "index.html")
    if not os.path.isfile(path): continue
    html = open(path, encoding="utf-8").read()
    m = re.search(r'id="brand-nav" type="application/json">(.*?)</script>', html, re.S)
    if not m:
        print(f"  FAIL  {slug} has no brand-nav block"); bad = 1; continue
    try: nav = json.loads(m.group(1))
    except Exception as ex:
        print(f"  FAIL  {slug} brand-nav is invalid JSON: {ex}"); bad = 1; continue
    if sorted(x["slug"] for x in nav) != slugs:
        print(f"  FAIL  {slug} switcher lists {len(nav)} of {len(slugs)} brands, rebuild all"); bad = 1
    elif "noindex" not in html:
        print(f"  note  {slug} has no noindex, switcher will not render (expected at launch)")
    else:
        print(f"  ok    {slug} switcher lists all {len(nav)}")
sys.exit(bad)
PY2
[ $? -ne 0 ] && FAIL=1
echo

if [ $FAIL -eq 0 ]; then echo "All checks passed."; else echo "Checks failed. Fix the items above before pushing."; fi
exit $FAIL
