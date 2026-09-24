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

# 1. Em dashes anywhere in tracked source
echo "1. Em dashes"
HITS=$(grep -rn $'—' --include="*.html" --include="*.css" --include="*.js" --include="*.md" --include="*.json" . 2>/dev/null || true)
if [ -n "$HITS" ]; then
  fail "em dashes found:"
  echo "$HITS" | sed 's/^/        /'
else
  pass "none found"
fi
echo

# 2. Unfilled placeholders outside the template
echo "2. Open placeholders in shipped brands"
for dir in brands/*/; do
  slug=$(basename "$dir")
  [ "$slug" = "_template" ] && continue
  [ -f "$dir/index.html" ] || continue
  N=$(grep -c "\[[A-Z0-9][A-Z0-9 ,.'\/-]*\]" "$dir/index.html" 2>/dev/null || echo 0)
  if [ "$N" -gt 0 ]; then
    fail "$slug has $N open placeholder(s)"
  else
    pass "$slug clean"
  fi
done
echo

# 3. Brand registry is valid JSON and every slug has a folder
echo "3. Brand registry"
python3 - <<'PY'
import json, os, re, sys
src = open("index.html", encoding="utf-8").read()
m = re.search(r'id="brand-registry" type="application/json">(.*?)</script>', src, re.S)
if not m:
    print("  FAIL  registry block not found"); sys.exit(1)
try:
    data = json.loads(m.group(1))
except Exception as e:
    print(f"  FAIL  registry is not valid JSON: {e}"); sys.exit(1)
print(f"  ok    valid JSON, {len(data)} brand(s)")
bad = 0
required = {"slug", "name", "tagline", "accent", "verticals", "status", "updated"}
for b in data:
    missing = required - set(b)
    if missing:
        print(f"  FAIL  {b.get('slug','?')} missing keys: {sorted(missing)}"); bad = 1
    if not os.path.isdir(os.path.join("brands", b.get("slug", ""))):
        print(f"  FAIL  {b.get('slug')} has no folder under brands/"); bad = 1
    if b.get("status") not in ("live", "draft", "planned"):
        print(f"  FAIL  {b.get('slug')} has invalid status {b.get('status')!r}"); bad = 1
if not bad:
    print("  ok    every entry well formed and has a folder")
sys.exit(bad)
PY
[ $? -ne 0 ] && FAIL=1
echo

# 4. Required files per brand
echo "4. Brand folder contents"
for dir in brands/*/; do
  slug=$(basename "$dir")
  for f in index.html brand.css brief.md; do
    if [ -f "$dir$f" ]; then pass "$slug/$f"; else fail "$slug/$f missing"; fi
  done
done
echo

# 5. Shared asset links intact
echo "5. Shared asset links"
for dir in brands/*/; do
  slug=$(basename "$dir")
  [ -f "$dir/index.html" ] || continue
  grep -q '/assets/base.css' "$dir/index.html" && pass "$slug links base.css" || fail "$slug does not link base.css"
  grep -q '/assets/conversion.js' "$dir/index.html" && pass "$slug links conversion.js" || fail "$slug does not link conversion.js"
done
echo

# 6. No brand-local layout CSS
echo "6. brand.css contains tokens only"
for dir in brands/*/; do
  slug=$(basename "$dir")
  [ -f "$dir/brand.css" ] || continue
  # any selector other than :root or [data-theme=...] is a layout rule
  STRAY=$(grep -nE '^[^/ \t}].*\{' "$dir/brand.css" | grep -vE ':root|\[data-theme' || true)
  if [ -n "$STRAY" ]; then
    fail "$slug/brand.css has non-token rules:"
    echo "$STRAY" | sed 's/^/        /'
  else
    pass "$slug/brand.css tokens only"
  fi
done
echo

if [ $FAIL -eq 0 ]; then
  echo "All checks passed."
else
  echo "Checks failed. Fix the items above before pushing."
fi
exit $FAIL
