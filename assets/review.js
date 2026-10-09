/* ==========================================================================
   Review switcher. Jump between brand pages while reviewing them.

   Renders ONLY while the page still carries its wireframe noindex tag. The
   moment a brand is prepared for launch and that tag comes off, this widget
   disappears on its own. It cannot ship to a live site by accident.

   Reads the brand list from the inline JSON block that scripts/build.py
   writes into every page, so it works offline and needs no fetch.

   Keys: [ and ] step through brands, b opens the index, / toggles the panel.
   ========================================================================== */
(function () {
  "use strict";

  var robots = document.querySelector('meta[name="robots"]');
  if (!robots || robots.content.indexOf("noindex") === -1) { return; }

  var src = document.getElementById("brand-nav");
  if (!src) { return; }

  var brands = [];
  try { brands = JSON.parse(src.textContent); } catch (e) { return; }
  if (!brands.length) { return; }

  var here = (location.pathname.replace(/\/+$/, "").split("/").pop()) || "";
  var index = brands.findIndex(function (b) { return b.slug === here; });
  var current = index > -1 ? brands[index] : null;

  var esc = function (s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  };

  var wrap = document.createElement("div");
  wrap.className = "switcher";
  wrap.setAttribute("data-switcher", "");

  var items = brands.map(function (b) {
    return '<a class="switcher__item" href="/brands/' + esc(b.slug) + '/"' +
      (b.slug === here ? ' aria-current="page"' : "") + '>' +
      '<span class="switcher__dot" style="background:' + esc(b.accent) + '"></span>' +
      '<span class="switcher__name">' + esc(b.name) +
      '<small>' + esc(b.style) + (b.status ? " &middot; " + esc(b.status) : "") + '</small></span>' +
      (b.licence && b.licence !== "None"
        ? '<span class="switcher__badge">' + esc(b.licence) + "</span>" : "") +
      "</a>";
  }).join("");

  wrap.innerHTML =
    '<div class="switcher__panel" role="dialog" aria-label="Switch brand">' +
      '<div class="switcher__head"><span>Brand pages</span>' +
        '<span>' + brands.length + "</span></div>" +
      '<div class="switcher__list">' + items + "</div>" +
      '<div class="switcher__foot">' +
        '<a href="/">All brands</a>' +
        '<button type="button" data-sw-prev>Prev</button>' +
        '<button type="button" data-sw-next>Next</button>' +
      "</div>" +
      '<p class="switcher__hint">Keys: [ prev &middot; ] next &middot; b index</p>' +
    "</div>" +
    '<button class="switcher__toggle" type="button" aria-expanded="false">' +
      '<span class="switcher__dot" style="background:' +
        esc(current ? current.accent : "#888") + '"></span>' +
      esc(current ? current.name : "Brands") +
      '<span class="switcher__count">' +
        (index > -1 ? (index + 1) + "/" + brands.length : brands.length) +
      "</span>" +
    "</button>";

  document.body.appendChild(wrap);

  // Keep the current brand visible without having to hunt for it.
  var list = wrap.querySelector(".switcher__list");
  var scrollToCurrent = function () {
    var cur = list.querySelector('[aria-current="page"]');
    if (!cur) { return; }
    var top = cur.offsetTop - list.clientHeight / 2 + cur.offsetHeight / 2;
    list.scrollTop = Math.max(0, top);
  };

  var toggle = wrap.querySelector(".switcher__toggle");
  var open = function (state) {
    wrap.classList.toggle("is-open", state);
    toggle.setAttribute("aria-expanded", String(state));
    if (state) { scrollToCurrent(); }
  };
  toggle.addEventListener("click", function (e) {
    e.stopPropagation();
    var next = !wrap.classList.contains("is-open");
    open(next);
    if (next) { scrollToCurrent(); }
  });
  document.addEventListener("click", function (e) {
    if (!wrap.contains(e.target)) { open(false); }
  });

  var go = function (step) {
    if (!brands.length) { return; }
    var from = index > -1 ? index : 0;
    var to = (from + step + brands.length) % brands.length;
    location.href = "/brands/" + brands[to].slug + "/";
  };
  wrap.querySelector("[data-sw-prev]").addEventListener("click", function () { go(-1); });
  wrap.querySelector("[data-sw-next]").addEventListener("click", function () { go(1); });

  document.addEventListener("keydown", function (e) {
    var t = e.target;
    if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.tagName === "SELECT")) { return; }
    if (e.metaKey || e.ctrlKey || e.altKey) { return; }
    if (e.key === "[") { go(-1); }
    else if (e.key === "]") { go(1); }
    else if (e.key === "b") { location.href = "/"; }
    else if (e.key === "/") { e.preventDefault(); open(!wrap.classList.contains("is-open")); }
    else if (e.key === "Escape") { open(false); }
  });
})();
