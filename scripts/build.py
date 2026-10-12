#!/usr/bin/env python3
"""
Render every brand page and the index from data/.

  python3 scripts/build.py           # build all
  python3 scripts/build.py zepapay   # build one

Inputs
  data/brand-book.json  Brands, price lists and pitches lifted from the xlsx.
  data/pages.json       Page content per brand, keyed by slug.

Output
  brands/<slug>/index.html   generated, committed, served statically
  brands/<slug>/brand.css    accent tokens only
  index.html                 the hub, with its registry block rewritten

The generated HTML is what Vercel serves. There is no build step at deploy
time. This script exists so that 25 brands stay in sync, not to add tooling.
"""

import hashlib
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = {
    "terminal": "Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600;700",
    "swiss":    "Inter:wght@400;500;600;700&family=Archivo:wght@600;700;800",
    "brutal":   "Space+Grotesk:wght@400;500;600;700",
    "soft":     "DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700",
    "midnight": "Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1",
    "clinical": "Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600",
    "mono":     "Archivo:wght@400;500;600;800;900",
    "ledger":   "Inter+Tight:wght@400;500;600;700&family=Roboto+Mono:wght@400;500;600",
    "stamp":    "Inter:wght@400;500;600;700&family=Oswald:wght@400;500;600;700",
    "warm":     "Nunito:wght@400;600;700;800",
    "wire":     "IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600",
    "frame":    "Inter:wght@400;500;600",
}


def e(s):
    """Escape for HTML text and attributes."""
    if s is None:
        return ""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


def pct(v):
    """0.025 -> 2.50%  |  '1% or USD 30 >' -> passed through."""
    if v is None or v == "":
        return None
    s = str(v).strip()
    try:
        f = float(s)
    except ValueError:
        return s.replace(" >", " minimum")
    if f == 0:
        return "None"
    if f < 1:
        return "{:.2f}%".format(f * 100).replace(".00%", "%")
    return s


def money(v):
    if v is None or v == "":
        return None
    s = str(v).strip()
    if s in ("0.0", "0", "-"):
        return "None"
    return s


# ---------------------------------------------------------------- sections

def sec_announce(b):
    a = b.get("announce")
    if not a:
        return ""
    timer = ""
    if a.get("countdown_hours"):
        timer = ('<span class="announce__timer" data-countdown data-key="{k}" '
                 'data-hours="{h}">00:00:00</span>').format(k=b["slug"], h=a["countdown_hours"])
    return """
<div class="announce" data-announce data-key="{slug}-v1">
  <span>{text}</span>{timer}
  <a href="#apply" data-cta="announce">{cta}</a>
  <button class="announce__close" data-announce-close aria-label="Dismiss">&times;</button>
</div>""".format(slug=b["slug"], text=e(a["text"]), timer=timer, cta=e(a["cta"]))


def sec_nav(b):
    # A nav item points at a section by "id", or anywhere by "href".
    links = "".join('<a href="{0}">{1}</a>'.format(
        e(l["href"]) if l.get("href") else "#" + e(l["id"]), e(l["label"])) for l in b["nav"])
    second = ""
    if b.get("nav_secondary"):
        # e.g. a "Log In" button in place of the Telegram button
        ns = b["nav_secondary"]
        second = ('<a class="btn btn--ghost" href="{href}" data-cta="nav-secondary">{label}</a>'
                  .format(href=e(ns.get("href", "#")), label=e(ns["label"])))
    elif b.get("telegram_cta"):
        second = ('<a class="btn btn--tg" href="{href}" data-cta="nav-telegram">{label}</a>'
                  .format(href=e(b.get("telegram_url", "#apply")), label=e(b["telegram_cta"])))
    return """
<nav class="nav" data-nav>
  <div class="container nav__inner{center}">
    {brand}
    <div class="nav__links">{links}</div>
    <div class="nav__actions">
      {second}
      <a class="btn btn--primary" href="#apply" data-cta="nav-primary">{cta}</a>
    </div>
  </div>
</nav>""".format(links=links, second=second, cta=e(b["cta_primary"]),
                 center=" nav__inner--center" if b.get("nav_layout") == "center" else "",
                 brand=('<a class="nav__brand nav__brand--wordmark" href="./">{0}</a>'.format(e(b["name"]))
                        if b.get("wordmark") else
                        '<a class="nav__brand" href="./"><span class="nav__mark">{0}</span> {1}</a>'
                        .format(e(b["mark"]), e(b["name"]))))


def _reversal(items):
    if not items:
        return ""
    return '<div class="reversal">' + "".join(
        "<span>{0}</span>".format(e(i)) for i in items) + "</div>"


def _hero_visual(h):
    kind = h.get("visual", {}).get("type")
    v = h.get("visual", {})
    if kind == "mock":
        rows = "".join("""
      <div class="mock__row">
        <span class="mock__label">{label}<span class="mock__sub">{sub}</span></span>
        <span class="mock__amt{cls}">{amt}</span>
      </div>""".format(label=e(r["label"]), sub=e(r["sub"]), amt=e(r["amount"]),
                       cls=" yes" if r.get("good") else "") for r in v["rows"])
        return """
    <div class="hero__visual reveal">
      <div class="mock__head"><span>{title}</span><span>{status}</span></div>{rows}
    </div>""".format(title=e(v["title"]), status=e(v["status"]), rows=rows)
    if kind == "stats":
        cells = "".join("""
      <div class="stat"><div class="stat__num">{n}</div><div class="stat__label">{l}</div></div>
        """.format(n=e(s["value"]), l=e(s["label"])) for s in v["items"])
        return '<div class="stats reveal">{0}</div>'.format(cells)
    if kind == "form":
        return _form_markup(v["form"], compact=True)
    if kind == "stack":
        # Product mockup built in HTML: cards stacked with a slight offset.
        # Values are typed in pages.json and are not live data.
        def row(r):
            mark = ""
            if r.get("status") == "dot":
                mark = '<i class="stack__dot" aria-hidden="true"></i>'
            elif r.get("status") == "check":
                mark = ('<svg class="stack__check" width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">'
                        '<path d="M2.5 7.5 5.5 10.5 11.5 3.5" stroke="currentColor" stroke-width="1.6" '
                        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
            return ('<div class="stack__row"><span class="stack__label">{l}</span>'
                    '<span class="stack__value{mono}">{m}{v}</span></div>').format(
                        l=e(r["label"]), v=e(r["value"]), m=mark,
                        mono=" mono" if r.get("mono") else "")
        cards = "".join(
            '<div class="stack__card"><div class="stack__title">{t}</div>{rows}</div>'.format(
                t=e(c["title"]), rows="".join(row(r) for r in c["rows"]))
            for c in v["cards"])
        note = ("\n    <!-- {0} -->".format(e(v["note"])) if v.get("note") else "")
        return """{note}
    <div class="hero__stack reveal"><div class="stack">{cards}</div></div>""".format(note=note, cards=cards)
    return ""


def sec_hero(b):
    h = b["hero"]
    layout = h.get("layout", "split")
    ctas = ('<a class="btn btn--primary btn--lg" href="#apply" data-cta="hero-primary">{0}</a>'
            .format(e(h["cta"])))
    if h.get("cta_secondary") and h.get("cta_secondary_style") == "link":
        ctas += ('<a class="link-cta" href="#{anchor}" data-cta="hero-secondary">'
                 '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" aria-hidden="true">'
                 '<circle cx="9" cy="9" r="8" stroke="currentColor"/>'
                 '<path d="M7.5 5.5 11 9l-3.5 3.5" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/>'
                 '</svg>{0}</a>'
                 .format(e(h["cta_secondary"]), anchor=e(h.get("cta_secondary_anchor", "how"))))
    elif h.get("cta_secondary"):
        ctas += ('<a class="btn btn--ghost btn--lg" href="#{anchor}" data-cta="hero-secondary">{0}</a>'
                 .format(e(h["cta_secondary"]), anchor=e(h.get("cta_secondary_anchor", "how"))))

    copy = """
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="lede">{sub}</p>
      <div class="cta-row">{ctas}</div>
      {rev}
    </div>""".format(eyebrow=e(h["eyebrow"]), h1=e(h["h1"]), sub=e(h["sub"]),
                     ctas=ctas, rev=_reversal(h.get("reversal")))

    if layout == "center":
        return """
<header class="hero hero--center" data-stickybar-after>
  <div class="container">{copy}</div>
</header>""".format(copy=copy)

    cls = "split--form" if h.get("visual", {}).get("type") == "form" else "split"
    return """
<header class="hero" data-stickybar-after>
  <div class="container {cls}">{copy}{visual}</div>
</header>""".format(cls=cls, copy=copy, visual=_hero_visual(h))


def sec_trustbar(b):
    t = b.get("trustbar")
    if not t:
        return ""
    chips = "".join('<span class="chip">{0}</span>'.format(e(c)) for c in t["chips"])
    return """
<section class="trustbar"{id}>
  <div class="container trustbar__inner">
    <span class="trustbar__label">{label}</span>{chips}
  </div>
</section>""".format(label=e(t["label"]), chips=chips,
                     id=' id="{0}"'.format(e(t["id"])) if t.get("id") else "")


def _cards(items, numbered=False, accent_index=None):
    out = []
    for i, c in enumerate(items):
        icon = ""
        if numbered:
            icon = '<div class="card__icon">{0}</div>'.format(i + 1)
        elif c.get("icon"):
            icon = '<div class="card__icon">{0}</div>'.format(e(c["icon"]))
        ticks = ""
        if c.get("points"):
            ticks = '<ul class="ticklist">' + "".join(
                "<li>{0}</li>".format(e(p)) for p in c["points"]) + "</ul>"
        cls = "card card--accent" if accent_index == i else "card"
        out.append('<div class="{cls}">{icon}<h3>{t}</h3><p>{b}</p>{ticks}</div>'
                   .format(cls=cls, icon=icon, t=e(c["title"]), b=e(c["body"]), ticks=ticks))
    return "".join(out)


def sec_block(b, key, grid, tint=False, numbered=False):
    s = b.get(key)
    if not s:
        return ""
    # A page may override the grid, e.g. "grid-1" for a style that runs a
    # large body and a narrow container, or "grid-3" for five short cards.
    grid = s.get("grid", grid)
    head = '<p class="eyebrow">{0}</p>'.format(e(s["eyebrow"])) if s.get("eyebrow") else ""
    lede = '<p class="lede">{0}</p>'.format(e(s["lede"])) if s.get("lede") else ""
    cta = ""
    if s.get("cta"):
        cta = ('<div class="cta-row reveal" style="margin-top:28px">'
               '<a class="btn btn--primary" href="#apply" data-cta="{k}">{c}</a></div>'
               .format(k=key, c=e(s["cta"])))
    return """
<section class="section{tint}" id="{id}">
  <div class="container">
    <div class="section-head reveal">{head}<h2>{h2}</h2>{lede}</div>
    {grid_html}
    {foot}{cta}
  </div>
</section>""".format(tint=" section--tint" if tint else "", id=s.get("id", key),
                     head=head, h2=e(s["h2"]), lede=lede,
                     grid_html=('<div class="grid {0} reveal">{1}</div>'.format(
                         grid, _cards(s["cards"], numbered=numbered,
                                      accent_index=s.get("accent_index")))
                         if s.get("cards") else ""),
                     foot=('<p class="muted reveal" style="margin-top:22px">{0}</p>'
                           .format(e(s["foot"])) if s.get("foot") else ""),
                     cta=cta)


def sec_how(b):
    s = b.get("how")
    if not s:
        return ""
    steps = "".join("""
      <div><div class="step__num">{n}</div><h3>{t}</h3><p class="muted">{b}</p></div>
    """.format(n=i + 1, t=e(c["title"]), b=e(c["body"])) for i, c in enumerate(s["cards"]))
    return """
<section class="section" id="how">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div>
    <div class="steps{stack} reveal">{steps}</div>
  </div>
</section>""".format(eyebrow=e(s.get("eyebrow", "Process")), h2=e(s["h2"]), steps=steps,
                     stack=" steps--stack" if s.get("layout") == "stack" else "")


def sec_pricing(b, price_lists):
    p = b.get("pricing")
    if not p:
        return ""
    if p.get("columns"):
        return _pricing_multi(p)
    pl = next((x for x in price_lists if x["name"] == p["price_list"]), None)
    rows = []

    def row(label, value, note=None, hi=False):
        if value in (None, ""):
            return
        rows.append('<tr{hi}><td>{l}{n}</td><td class="rate">{v}</td></tr>'.format(
            hi=' class="is-highlight"' if hi else "",
            l=e(label),
            n='<br><span class="muted" style="font-size:.82em">{0}</span>'.format(e(note)) if note else "",
            v=e(value)))

    if pl:
        row("Setup, one time", money(pl.get("setup")))
        row("Monthly maintenance", money(pl.get("monthly")))
        for label, key, hi in p.get("show", []):
            val = pl.get(key)
            row(label, pct(val) if key not in ("min_ticket", "max_ticket", "setup", "monthly", "exchange", "reserve", "limit_rule") else (money(val) if "ticket" in key else val), hi=hi)
        row("FX on conversion", pl.get("exchange"))
        row("Rolling reserve", pl.get("reserve") and str(pl["reserve"]).replace("/", " percent held, released in ") + " days")
        row("Minimum ticket", money(pl.get("min_ticket")))
        row("Maximum ticket", money(pl.get("max_ticket")))

    for extra in p.get("extra_rows", []):
        row(extra["label"], extra["value"], extra.get("note"), extra.get("highlight"))

    not_charged = ""
    if p.get("not_charged"):
        not_charged = ('<ul class="ticklist crosslist" style="margin-top:22px">' +
                       "".join("<li>{0}</li>".format(e(x)) for x in p["not_charged"]) + "</ul>")

    return """
<section class="section section--tint" id="pricing">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{eyebrow}</p><h2>{h2}</h2><p class="lede">{lede}</p>
    </div>
    <div class="price-wrap reveal">
      <table class="pricetable">
        <thead><tr><th scope="col">Line</th><th scope="col">Rate</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    {not_charged}
    <p class="cta-note reveal">{note}</p>
  </div>
</section>""".format(eyebrow=e(p.get("eyebrow", "Pricing")), h2=e(p["h2"]),
                     lede=e(p.get("lede", "")), rows="".join(rows),
                     not_charged=not_charged, note=e(p.get("note", "")))


def _pricing_multi(p):
    """Pricing for a brand that sells more than one rail: one column per rail.

    Values are typed in data/pages.json rather than read from a price list,
    because one row can span two lists. Each must still come from the book.
    """
    head = "".join('<th scope="col">{0}</th>'.format(e(c)) for c in p["columns"])
    rows = "".join(
        '<tr{hi}><td>{l}</td>{cells}</tr>'.format(
            hi=' class="is-highlight"' if r.get("highlight") else "",
            l=e(r["label"]),
            cells="".join('<td class="rate" data-label="{c}">{v}</td>'.format(c=e(c), v=e(v))
                          for c, v in zip(p["columns"], r["values"])))
        for r in p["rows"])
    cta = ""
    if p.get("cta"):
        cta = ('<div class="cta-row reveal" style="margin-top:22px">'
               '<a class="btn btn--primary" href="#apply" data-cta="pricing">{0}</a></div>'
               .format(e(p["cta"])))
    return """
<section class="section section--tint" id="pricing">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">{eyebrow}</p><h2>{h2}</h2><p class="lede">{lede}</p>
    </div>
    <div class="price-wrap reveal">
      <table class="pricetable pricetable--multi">
        <thead><tr><th scope="col"><span class="sr-only">Line</span></th>{head}</tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
    <p class="cta-note reveal">{note}</p>{cta}
  </div>
</section>""".format(eyebrow=e(p.get("eyebrow", "Pricing")), h2=e(p["h2"]),
                     lede=e(p.get("lede", "")), head=head, rows=rows,
                     note=e(p.get("note", "")), cta=cta)


def sec_estimator(b):
    s = b.get("estimator")
    if not s:
        return ""
    for m in s["modes"]:
        # Optional component view, e.g. crypto deposit 2% + SEPA payout 0.5%.
        # The parts must add up to the headline rate or the page contradicts itself.
        if m.get("parts"):
            total = round(sum(x["pct"] for x in m["parts"]), 6)
            if total != round(m["pct"], 6):
                sys.exit("estimator parts for {0}/{1} add up to {2}, not {3}".format(
                    b["slug"], m["key"], total, m["pct"]))
    modes = "".join('<button type="button" data-est-mode="{k}" data-pct="{p}"{parts}{floor}>{l}</button>'
                    .format(k=m["key"], p=m["pct"], l=e(m["label"]),
                            parts=(' data-parts="{0}"'.format(e(json.dumps(m["parts"])))
                                   if m.get("parts") else ""),
                            floor=(' data-floor="{0}"'.format(m["floor"]) if m.get("floor") else "")
                                  + (' data-monthly="{0}"'.format(m["monthly"]) if "monthly" in m else ""))
                    for m in s["modes"])
    # Optional second slider: average payout size. With it, a per-payout
    # minimum ("1% or $30, whichever is higher") is charged per payout, so the
    # floor shows up at small tickets instead of hiding inside a percentage.
    avg = ""
    if s.get("avg_values"):
        vals = s["avg_values"]
        idx = vals.index(s.get("avg_default", vals[0]))
        avg = """
        <div>
          <div class="range-head"><span>{label}</span><b data-est-avg-label>$0</b></div>
          <input type="range" data-est-avg data-values="{vals}" min="0" max="{mx}" step="1" value="{idx}" aria-label="{label}">
        </div>""".format(label=e(s.get("avg_label", "Average payout")), vals=e(json.dumps(vals)),
                         mx=len(vals) - 1, idx=idx)
    topup = ' data-topup="{0}" data-topup-label="{1}"'.format(
        s["topup_pct"], e(s.get("topup_label", "Top-up"))) if s.get("topup_pct") else ""
    return """
<section class="section" id="estimate">
  <div class="container">
    <div class="section-head reveal"><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2><p class="lede">{lede}</p></div>
    <div class="estimator reveal" data-estimator data-setup="{setup}" data-monthly="{monthly}"{topup}>
      <div class="estimator__controls">
        <div class="seg">{modes}</div>
        <div>
          <div class="range-head"><span>Monthly volume</span><b data-est-volume-label>$0</b></div>
          <input type="range" data-est-volume min="{min}" max="{max}" step="{step}" value="{val}" aria-label="Monthly volume">
        </div>{avg}
        <p class="form-note">{disclaimer}</p>
      </div>
      <div class="estimator__out">
        <p class="muted" style="margin:0 0 4px;font-size:.85rem">{out_label}</p>
        <div class="estimator__big" data-est-total>$0</div>
        <div data-est-lines style="margin-top:16px"></div>
        <a class="btn btn--primary btn--block" href="#apply" style="margin-top:18px" data-cta="estimator">{cta}</a>
      </div>
    </div>
  </div>
</section>""".format(eyebrow=e(s.get("eyebrow", "Cost")), h2=e(s["h2"]), lede=e(s.get("lede", "")),
                     setup=s.get("setup", 0), monthly=s.get("monthly", 0), modes=modes,
                     min=s.get("min", 10000), max=s.get("max", 1000000),
                     step=s.get("step", 10000), val=s.get("default", 100000),
                     disclaimer=e(s.get("disclaimer", "")), out_label=e(s.get("out_label", "Estimated monthly cost")),
                     cta=e(s.get("cta", "Get a written quote")), avg=avg, topup=topup)


def _form_markup(f, compact=False):
    """Single step or multi step lead form."""
    multistep = len(f["steps"]) > 1
    bar = ""
    if multistep:
        bar = '<div class="steps-bar">' + "".join("<i></i>" for _ in f["steps"]) + "</div>"

    def field(fl):
        if fl["type"] == "select":
            opts = '<option value="">Select</option>' + "".join(
                "<option>{0}</option>".format(e(o)) for o in fl["options"])
            inner = '<select name="{n}"{req}>{o}</select>'.format(
                n=e(fl["name"]), req=" required" if fl.get("required") else "", o=opts)
        elif fl["type"] == "textarea":
            inner = '<textarea name="{n}" rows="3" placeholder="{p}"></textarea>'.format(
                n=e(fl["name"]), p=e(fl.get("placeholder", "")))
        else:
            inner = '<input type="{t}" name="{n}" placeholder="{p}"{req}>'.format(
                t=e(fl["type"]), n=e(fl["name"]), p=e(fl.get("placeholder", "")),
                req=" required" if fl.get("required") else "")
        return "<label>{0} {1}</label>".format(e(fl["label"]), inner)

    steps_html = []
    for i, st in enumerate(f["steps"]):
        pairs, single = [], []
        for fl in st:
            (pairs if fl.get("half") else single).append(fl)
        body = ""
        while pairs:
            chunk, pairs = pairs[:2], pairs[2:]
            body += '<div class="form-grid">' + "".join(field(x) for x in chunk) + "</div>"
        body += "".join(field(x) for x in single)
        last = i == len(f["steps"]) - 1
        if multistep:
            nav = '<div class="cta-row">'
            if i > 0:
                nav += '<button type="button" class="btn btn--ghost" data-back>Back</button>'
            nav += ('<button type="submit" class="btn btn--primary" style="flex:1" data-cta="form-submit">{0}</button>'
                    .format(e(f["submit"])) if last else
                    '<button type="button" class="btn btn--primary" style="flex:1" data-next>Continue</button>')
            nav += "</div>"
        else:
            nav = ('<button type="submit" class="btn btn--primary btn--block btn--lg" data-cta="form-submit">{0}</button>'
                   .format(e(f["submit"])))
        steps_html.append('<div class="fstep">{0}{1}</div>'.format(body, nav))

    head = ""
    if f.get("title"):
        head = '<div class="form__head"><h3>{0}</h3><p class="muted" style="font-size:.88rem;margin:0">{1}</p></div>'.format(
            e(f["title"]), e(f.get("sub", "")))

    return """
    <form class="card form reveal" data-lead-form{multi}{free} data-endpoint="" data-success="{success}">
      <input class="hp" type="text" name="company_website_hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      {head}{bar}{steps}
      <p class="form-note" data-form-status>{note}</p>
    </form>""".format(multi=" data-multistep" if multistep else "",
                      free=" data-block-free-email" if f.get("block_free_email") else "",
                      success=e(f.get("success", "Got it. We come back within one business day.")),
                      head=head, bar=bar, steps="".join(steps_html), note=e(f.get("note", "")))


def sec_form(b):
    s = b.get("apply")
    if not s:
        return ""
    ticks = ""
    if s.get("points"):
        ticks = '<ul class="ticklist">' + "".join(
            "<li>{0}</li>".format(e(p)) for p in s["points"]) + "</ul>"
    tg = ""
    if b.get("telegram_cta"):
        tg = ('<div class="cta-row" style="margin-top:24px">'
              '<a class="btn btn--tg" href="{h}" data-cta="apply-telegram">{l}</a>'
              '<span class="muted" style="font-size:.85rem">{n}</span></div>'
              .format(h=e(b.get("telegram_url", "#")), l=e(b["telegram_cta"]),
                      n=e(s.get("telegram_note", ""))))
    return """
<section class="section" id="apply">
  <div class="container split--form">
    <div class="reveal">
      <p class="eyebrow">{eyebrow}</p><h2>{h2}</h2><p class="lede">{lede}</p>{ticks}{tg}
    </div>
    {form}
  </div>
</section>""".format(eyebrow=e(s.get("eyebrow", "Apply")), h2=e(s["h2"]),
                     lede=e(s.get("lede", "")), ticks=ticks, tg=tg,
                     form=_form_markup(s["form"]))


def sec_faq(b):
    s = b.get("faq")
    if not s:
        return ""
    items = "".join(
        '<details{o}><summary>{q}</summary><div>{a}</div></details>'.format(
            o=" open" if i == 0 else "", q=e(x["q"]), a=e(x["a"]))
        for i, x in enumerate(s["items"]))
    return """
<section class="section section--tint" id="faq">
  <div class="container">
    <div class="section-head center reveal"><h2>{h2}</h2><p class="lede">{lede}</p></div>
    <div class="faq reveal">{items}</div>
  </div>
</section>""".format(h2=e(s.get("h2", "Questions")), lede=e(s.get("lede", "")), items=items)


def sec_final(b):
    s = b.get("final")
    if not s:
        return ""
    second = ""
    if b.get("telegram_cta"):
        second = ('<a class="btn btn--ghost btn--lg" href="{h}" data-cta="final-telegram">{l}</a>'
                  .format(h=e(b.get("telegram_url", "#")), l=e(b["telegram_cta"])))
    return """
<section class="section section--flush">
  <div class="container">
    <div class="final-cta reveal">
      <h2>{h2}</h2><p class="lede center">{body}</p>
      <div class="cta-row" style="justify-content:center">
        <a class="btn btn--primary btn--lg" href="#apply" data-cta="final-primary">{cta}</a>{second}
      </div>
    </div>
  </div>
</section>""".format(h2=e(s["h2"]), body=e(s["body"]), cta=e(s["cta"]), second=second)


def sec_footer(b):
    cols = "".join(
        '<div><h4>{t}</h4><ul>{li}</ul></div>'.format(
            t=e(c["title"]),
            li="".join('<li><a href="{h}">{l}</a></li>'.format(
                h=e(x.get("href", "#")), l=e(x["label"])) for x in c["links"]))
        for c in b["footer"]["columns"])
    return """
<footer class="footer">
  <div class="container">
    <div class="footer__cols{narrow}">
      <div>
        <div class="nav__brand" style="margin-bottom:10px"><span class="nav__mark">{mark}</span> {name}</div>
        <p class="muted" style="font-size:.86rem">{tagline}</p>
      </div>
      {cols}
    </div>
    <div class="footer__legal">{legal}<br>&copy; <span id="yr"></span> {name}. All rights reserved.</div>
  </div>
</footer>""".format(mark=e(b["mark"]), name=e(b["name"]), tagline=e(b["tagline"]),
                    cols=cols, legal=e(b["footer"]["legal"]),
                    narrow=" footer__cols--two" if len(b["footer"]["columns"]) == 1 else "")


def sec_sticky(b):
    s = b.get("sticky")
    if not s:
        return ""
    return """
<div class="stickybar" data-stickybar>
  <div class="stickybar__copy"><strong>{t}</strong><span class="muted">{s}</span></div>
  <a class="btn btn--primary" href="#apply" data-cta="sticky">{c}</a>
</div>
<div class="railcta" data-railcta>
  <span>{t}</span>
  <a class="btn btn--primary" href="#apply" data-cta="rail">{c}</a>
</div>""".format(t=e(s["title"]), s=e(s["sub"]), c=e(s["cta"]))


def sec_exit(b):
    s = b.get("exit_modal")
    if not s:
        return ""
    return """
<div class="modal" id="exit-modal" data-modal data-exit-intent data-key="{slug}-v1"
     aria-hidden="true" role="dialog" aria-modal="true" aria-label="{h}">
  <div class="modal__panel">
    <button class="modal__close" data-modal-close aria-label="Close">&times;</button>
    <p class="eyebrow">{eyebrow}</p>
    <h3>{h}</h3>
    <p class="muted">{body}</p>
    <form class="form" data-lead-form data-endpoint="" data-success="{success}">
      <input class="hp" type="text" name="company_website_hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label>Work email <input type="email" name="email" required placeholder="you@company.com"></label>
      <button class="btn btn--primary btn--block" type="submit" data-cta="exit-modal">{cta}</button>
      <p class="form-note" data-form-status>{note}</p>
    </form>
  </div>
</div>""".format(slug=b["slug"], eyebrow=e(s.get("eyebrow", "Before you go")), h=e(s["h"]),
                 body=e(s["body"]), cta=e(s["cta"]), note=e(s.get("note", "")),
                 success=e(s.get("success", "On its way.")))


# ---------------------------------------------------------------- page

def faq_schema(b):
    s = b.get("faq")
    if not s:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": x["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": x["a"]}}
                       for x in s["items"]],
    }
    return '<script type="application/ld+json">{0}</script>'.format(json.dumps(data))


def render(b, price_lists, nav_json="[]"):
    body = "".join([
        sec_announce(b),
        '<div class="progress" data-progress></div>',
        sec_nav(b),
        sec_hero(b),
        sec_trustbar(b),
        # A page that sells to named payee or buyer types can lead with them.
        (sec_block(b, "segments", "grid-2", tint=True) if b.get("segments_first") else ""),
        sec_block(b, "problem", "grid-3"),
        sec_block(b, "product", "grid-2", tint=True),
        sec_how(b),
        sec_pricing(b, price_lists),
        sec_estimator(b),
        ("" if b.get("segments_first") else sec_block(b, "segments", "grid-2", tint=True)),
        sec_block(b, "compliance", "grid-3"),
        sec_form(b),
        sec_faq(b),
        sec_final(b),
        sec_footer(b),
        sec_sticky(b),
        sec_exit(b),
    ])
    return """<!doctype html>
<html lang="en" data-style="{style}"{framed}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://{domain}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta name="twitter:card" content="summary_large_image">
{robots}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={font}&display=swap">
<link rel="stylesheet" href="/assets/base.css">
<link rel="stylesheet" href="/assets/themes.css">
<link rel="stylesheet" href="brand.css">
<script defer src="/assets/conversion.js"></script>
<!-- Review switcher. Renders only while the noindex tag above is present. -->
<script id="brand-nav" type="application/json">{nav}</script>
<script defer src="/assets/review.js"></script>
</head>
<body>
{body}
{schema}
<script>document.getElementById("yr").textContent=new Date().getFullYear();</script>
</body>
</html>
""".format(style=b["style"], title=e(b["seo"]["title"]), desc=e(b["seo"]["description"]),
           domain=e(b["domain"]), font=FONTS[b["style"]], body=body, schema=faq_schema(b),
           nav=nav_json,
           framed=" data-framed" if b.get("framed") else "",
           robots=("" if b.get("launched")
                   else '<meta name="robots" content="noindex, nofollow">'))


def render_brand_css(b):
    return """/* {name} - accent tokens only. Layout lives in /assets/base.css.
   Look lives in /assets/themes.css under [data-style="{style}"]. */
:root {{
  --accent:      {accent};
  --accent-fg:   {accent_fg};
  --accent-soft: {accent_soft};
}}
""".format(name=b["name"], style=b["style"], accent=b["accent"],
           accent_fg=b.get("accent_fg", "#ffffff"), accent_soft=b["accent_soft"])


STATE = os.path.join(ROOT, "data", "build-state.json")


def load_state():
    if os.path.isfile(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def stamp(slug, content, state):
    """Return the date this brand last actually changed.

    The registry's `updated` field must not move on every build, or index.html
    shows a diff every day for nothing. Hash the rendered page and only bump the
    date when the hash changes.
    """
    h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    prev = state.get(slug)
    if prev and prev.get("hash") == h:
        return prev["updated"]
    state[slug] = {"hash": h, "updated": date.today().isoformat()}
    return state[slug]["updated"]


def read_styles():
    """Parse assets/themes.css for the style list and its one-line description.

    Single source of truth. The index page and the docs read this rather than
    carrying their own hand-maintained list, which is how they fell out of sync.
    """
    css = open(os.path.join(ROOT, "assets", "themes.css"), encoding="utf-8").read()
    out = []
    for m in re.finditer(
            r"/\* -+ \d+\. (\w+) -+\n(.*?)\*/\s*\[data-style=", css, re.S):
        name, body = m.group(1), m.group(2)
        desc = " ".join(l.strip().rstrip("*").strip() for l in body.strip().split("\n"))
        out.append({"name": name, "description": re.sub(r"\s+", " ", desc).strip()})
    seen = {s["name"] for s in out}
    for m in re.finditer(r'^\[data-style="(\w+)"\] \{', css, re.M):
        if m.group(1) not in seen:
            out.append({"name": m.group(1), "description": ""})
            seen.add(m.group(1))
    return out


def render_vercel(pages):
    """Write vercel.json so noindex is applied per brand, not repo-wide.

    A brand launches by setting "launched": true in data/pages.json. Its page
    then loses both the meta tag and the X-Robots-Tag header, and every other
    brand keeps both. There is no repo-wide switch to get wrong.
    """
    headers = [{
        "source": "/assets/(.*)",
        "headers": [{"key": "Cache-Control", "value": "public, max-age=3600, must-revalidate"}],
    }, {
        "source": "/(.*)",
        "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
        ],
    }]
    # The index is internal and always stays out of search.
    noindex = [{"source": "/", "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}]}]
    for b in pages:
        if not b.get("launched"):
            noindex.append({
                "source": "/brands/{0}/(.*)?".format(b["slug"]),
                "headers": [{"key": "X-Robots-Tag", "value": "noindex, nofollow"}],
            })
    cfg = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "cleanUrls": True,
        "trailingSlash": True,
        "headers": headers + noindex,
    }
    with open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    return sum(1 for b in pages if b.get("launched"))


def render_index(pages, book, stamps):
    by_name = {x["brand"].strip().lower(): x for x in book["brands"]}
    registry = []
    missing = []
    for b in pages:
        key = (b.get("book_key") or b["name"]).strip().lower()
        bk = by_name.get(key, {})
        if not bk:
            missing.append(b["name"])
        registry.append({
            "slug": b["slug"], "name": b["name"], "tagline": b["tagline"],
            "accent": b["accent"], "style": b["style"],
            "status": bk.get("status", "Idea"), "type": bk.get("type", ""),
            "priority": bk.get("priority") or "", "licence": bk.get("licence") or "None",
            "verticals": (bk.get("industries") or [])[:3],
            "category": bk.get("category", "Payments"),
            "launched": bool(b.get("launched")),
            "updated": stamps.get(b["slug"], date.today().isoformat()),
        })
    block = json.dumps(registry, indent=2)

    path = os.path.join(ROOT, "index.html")
    with open(path, encoding="utf-8") as f:
        src = f.read()
    new = re.sub(
        r'(<script id="brand-registry" type="application/json">)(.*?)(</script>)',
        lambda m: m.group(1) + "\n" + block + "\n" + m.group(3),
        src, flags=re.S)

    styles = json.dumps(read_styles(), indent=2)
    new = re.sub(
        r'(<script id="style-catalog" type="application/json">)(.*?)(</script>)',
        lambda m: m.group(1) + "\n" + styles + "\n" + m.group(3),
        new, flags=re.S)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    if missing:
        print("  WARNING: not found in the brand book:", ", ".join(missing))
        print("           set book_key on those pages so status and licence come through")
    return len(registry)


def main():
    book = load("brand-book.json")
    pages = load("pages.json")["pages"]
    only = sys.argv[1] if len(sys.argv) > 1 else None

    # Shared brand list for the review switcher on every page. Always built from
    # the full set, so rebuilding one brand does not shrink the others' menu.
    by_name = {x["brand"].strip().lower(): x for x in book["brands"]}
    nav = []
    for b in pages:
        bk = by_name.get((b.get("book_key") or b["name"]).strip().lower(), {})
        nav.append({"slug": b["slug"], "name": b["name"], "accent": b["accent"],
                    "style": b["style"], "status": bk.get("status", "Idea"),
                    "licence": bk.get("licence") or "None",
                    "priority": bk.get("priority") or ""})
    # Same ordering the index uses, so stepping with ] matches the card order.
    order = {"Live": 0, "Building": 1, "Idea": 2, "Paused": 3, "Burnt": 4, "Retired": 5}
    prio = {"High": 0, "Medium": 1, "Low": 2}
    nav.sort(key=lambda x: (order.get(x["status"], 9),
                            prio.get(x["priority"], 9), x["name"].lower()))
    for x in nav:
        x.pop("priority", None)
    nav_json = json.dumps(nav)

    state = load_state()
    stamps = {}
    built = []
    for b in pages:
        if only and b["slug"] != only:
            stamps[b["slug"]] = state.get(b["slug"], {}).get("updated", date.today().isoformat())
            continue
        d = os.path.join(ROOT, "brands", b["slug"])
        os.makedirs(d, exist_ok=True)
        html = render(b, book["price_lists"], nav_json)
        stamps[b["slug"]] = stamp(b["slug"], html, state)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        with open(os.path.join(d, "brand.css"), "w", encoding="utf-8") as f:
            f.write(render_brand_css(b))
        built.append(b["slug"])
        print("  built brands/{0}/  style={1}{2}".format(
            b["slug"], b["style"], "  LAUNCHED" if b.get("launched") else ""))

    save_state(state)
    n = render_index(pages, book, stamps)
    live = render_vercel(pages)
    print("  index registry: {0} brands, {1} style(s) catalogued".format(n, len(read_styles())))
    print("  vercel.json: {0} launched, {1} noindex".format(live, len(pages) - live))
    print("done:", len(built), "page(s)")


if __name__ == "__main__":
    main()
