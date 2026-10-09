/* ==========================================================================
   Shared conversion behaviours, v2. Zero dependencies, loaded with `defer`.
   Everything is opt-in via data attributes.
   ========================================================================== */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) {} }
  };
  var track = function (label, extra) {
    window.dispatchEvent(new CustomEvent("wf:event", {
      detail: Object.assign({ label: label, path: location.pathname }, extra || {})
    }));
  };

  /* ---- 1. Sticky nav ---------------------------------------------------- */
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("is-stuck", window.scrollY > 32); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---- 2. Read progress bar --------------------------------------------- */
  var bar = document.querySelector("[data-progress]");
  if (bar) {
    var tickBar = function () {
      var h = document.body.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + "%";
    };
    window.addEventListener("scroll", tickBar, { passive: true });
    tickBar();
  }

  /* ---- 3. Scroll reveal -------------------------------------------------- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && !reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---- 4. Countdown ------------------------------------------------------ */
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var deadline = el.getAttribute("data-deadline"), end;
    if (deadline) {
      end = new Date(deadline).getTime();
    } else {
      var key = "cdw:" + (el.getAttribute("data-key") || "default");
      var saved = store.get(key);
      var hours = parseInt(el.getAttribute("data-hours") || "72", 10);
      end = saved ? parseInt(saved, 10) : Date.now() + hours * 3600000;
      if (!saved) store.set(key, String(end));
    }
    var pad = function (n) { return n < 10 ? "0" + n : String(n); };
    (function tick() {
      var left = end - Date.now();
      if (left <= 0) { el.textContent = "00:00:00"; return; }
      var d = Math.floor(left / 86400000),
          h = Math.floor((left % 86400000) / 3600000),
          m = Math.floor((left % 3600000) / 60000),
          s = Math.floor((left % 60000) / 1000);
      el.textContent = (d > 0 ? d + "d " : "") + pad(h) + ":" + pad(m) + ":" + pad(s);
      setTimeout(tick, 1000);
    })();
  });

  /* ---- 5. Announcement bar ----------------------------------------------- */
  var announce = document.querySelector("[data-announce]");
  if (announce) {
    var aKey = "announce:" + (announce.getAttribute("data-key") || "v1");
    if (store.get(aKey) === "1") {
      announce.remove();
    } else {
      var close = announce.querySelector("[data-announce-close]");
      if (close) close.addEventListener("click", function () { announce.remove(); store.set(aKey, "1"); });
    }
  }

  /* ---- 6. Sticky CTAs, mobile bar and desktop rail ------------------------ */
  var trigger = document.querySelector("[data-stickybar-after]") || document.querySelector(".hero");
  var stickies = document.querySelectorAll("[data-stickybar], [data-railcta]");
  if (stickies.length) {
    if (trigger && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        var show = !entries[0].isIntersecting;
        stickies.forEach(function (s) { s.classList.toggle("is-visible", show); });
      }, { threshold: 0 }).observe(trigger);
    } else {
      stickies.forEach(function (s) { s.classList.add("is-visible"); });
    }
  }

  /* ---- 7. Modals --------------------------------------------------------- */
  var openModal = function (m) {
    if (!m || m.classList.contains("is-open")) return;
    m.classList.add("is-open"); m.setAttribute("aria-hidden", "false");
    var f = m.querySelector("input, button, select, textarea, a[href]");
    if (f) f.focus();
  };
  var closeModal = function (m) {
    if (!m) return;
    m.classList.remove("is-open"); m.setAttribute("aria-hidden", "true");
  };
  document.querySelectorAll("[data-modal-open]").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.preventDefault(); openModal(document.getElementById(b.getAttribute("data-modal-open")));
    });
  });
  document.querySelectorAll("[data-modal]").forEach(function (m) {
    m.addEventListener("click", function (e) {
      if (e.target === m || e.target.hasAttribute("data-modal-close")) closeModal(m);
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.querySelectorAll(".modal.is-open").forEach(closeModal);
  });

  /* ---- 8. Exit intent, once per visitor ----------------------------------- */
  var exitModal = document.querySelector("[data-exit-intent]");
  if (exitModal) {
    var eKey = "exit:" + (exitModal.getAttribute("data-key") || "v1");
    if (store.get(eKey) !== "1") {
      var fired = false;
      var fire = function () {
        if (fired) return;
        fired = true; openModal(exitModal); store.set(eKey, "1"); track("exit-intent");
        document.removeEventListener("mouseout", desktop);
      };
      var desktop = function (e) { if (!e.relatedTarget && e.clientY <= 0) fire(); };
      document.addEventListener("mouseout", desktop);
      var armed = false;
      setTimeout(function () { armed = true; }, 25000);
      window.addEventListener("scroll", function () {
        if (!armed || window.innerWidth > 820) return;
        var depth = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
        if (depth > 0.55) fire();
      }, { passive: true });
    }
  }

  /* ---- 9. FAQ, one open at a time ----------------------------------------- */
  var faqs = document.querySelectorAll(".faq details");
  faqs.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) return;
      faqs.forEach(function (o) { if (o !== item) o.open = false; });
      track("faq-open", { q: (item.querySelector("summary") || {}).textContent });
    });
  });

  /* ---- 10. Fee estimator --------------------------------------------------
     Reads its rates from data attributes so the markup stays the single
     source of truth and the numbers come from the brand's price list.      */
  document.querySelectorAll("[data-estimator]").forEach(function (root) {
    var vol   = root.querySelector("[data-est-volume]");
    var out   = root.querySelector("[data-est-total]");
    var lines = root.querySelector("[data-est-lines]");
    var volLabel = root.querySelector("[data-est-volume-label]");
    var modeBtns = root.querySelectorAll("[data-est-mode]");
    if (!vol || !out) return;

    var fmt = function (n) {
      return "$" + Math.round(n).toLocaleString("en-US");
    };
    var modes = {};
    modeBtns.forEach(function (b) {
      modes[b.getAttribute("data-est-mode")] = {
        pct: parseFloat(b.getAttribute("data-pct") || "0"),
        fixed: parseFloat(b.getAttribute("data-fixed") || "0"),
        label: b.textContent.trim(),
        parts: (function () {
          try { return JSON.parse(b.getAttribute("data-parts") || "null"); }
          catch (e) { return null; }
        })()
      };
    });
    var active = modeBtns.length ? modeBtns[0].getAttribute("data-est-mode") : null;

    var setup   = parseFloat(root.getAttribute("data-setup") || "0");
    var monthly = parseFloat(root.getAttribute("data-monthly") || "0");

    var render = function () {
      var v = parseFloat(vol.value);
      var m = modes[active] || { pct: 0, fixed: 0 };
      var variable = v * (m.pct / 100);
      var total = variable + monthly;
      if (volLabel) volLabel.textContent = fmt(v);
      out.textContent = fmt(total);
      if (lines) {
        var rateLines = m.parts && m.parts.length
          ? m.parts.map(function (p) {
              return '<div class="estimator__line"><span>' + p.label + ' at ' + p.pct + '%</span><span>' + fmt(v * p.pct / 100) + '</span></div>';
            }).join("")
          : '<div class="estimator__line"><span>' + (m.label || "Rate") + ' at ' + m.pct + '%</span><span>' + fmt(variable) + '</span></div>';
        lines.innerHTML =
          rateLines +
          (monthly ? '<div class="estimator__line"><span>Monthly maintenance</span><span>' + fmt(monthly) + '</span></div>' : '') +
          (setup ? '<div class="estimator__line"><span>One-time setup</span><span>' + fmt(setup) + '</span></div>' : '') +
          '<div class="estimator__line"><span>Effective rate on volume</span><span>' + (v ? ((total / v) * 100).toFixed(2) : "0.00") + '%</span></div>';
      }
    };
    vol.addEventListener("input", render);
    modeBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        active = b.getAttribute("data-est-mode");
        modeBtns.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        render(); track("estimator-mode", { mode: active });
      });
    });
    if (modeBtns.length) modeBtns[0].setAttribute("aria-pressed", "true");
    render();
  });

  /* ---- 11. Multi-step form ------------------------------------------------ */
  document.querySelectorAll("[data-multistep]").forEach(function (form) {
    var steps = form.querySelectorAll(".fstep");
    var marks = form.querySelectorAll(".steps-bar i");
    var i = 0;
    var show = function () {
      steps.forEach(function (s, n) { s.hidden = n !== i; });
      marks.forEach(function (m, n) { m.classList.toggle("is-done", n <= i); });
    };
    form.querySelectorAll("[data-next]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cur = steps[i];
        var bad = Array.prototype.slice.call(cur.querySelectorAll("input, select, textarea"))
          .filter(function (f) { return !f.checkValidity(); });
        if (bad.length) { bad[0].reportValidity(); return; }
        i = Math.min(i + 1, steps.length - 1); show(); track("form-step", { step: i + 1 });
      });
    });
    form.querySelectorAll("[data-back]").forEach(function (btn) {
      btn.addEventListener("click", function () { i = Math.max(i - 1, 0); show(); });
    });
    show();
  });

  /* ---- 12. Lead forms ----------------------------------------------------- */
  var FREE_EMAIL = ["gmail.com","yahoo.com","hotmail.com","outlook.com","icloud.com","proton.me","protonmail.com","aol.com","mail.com","yandex.com"];

  document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
    var startedAt = Date.now();
    var touched = false;
    form.addEventListener("input", function () {
      if (!touched) { touched = true; track("form-start"); }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector("[data-form-status]");
      var say = function (msg, ok) {
        if (!status) return;
        status.textContent = msg;
        status.style.color = ok ? "var(--positive)" : "var(--negative)";
      };

      var hp = form.querySelector(".hp");
      if (hp && hp.value) return;
      if (Date.now() - startedAt < 1500) { say("Take a moment and try again.", false); return; }

      var emailField = form.querySelector("input[type=email]");
      if (emailField && form.hasAttribute("data-block-free-email")) {
        var domain = (emailField.value.split("@")[1] || "").toLowerCase();
        if (FREE_EMAIL.indexOf(domain) !== -1) {
          say("Use your work email so we can verify the business.", false);
          emailField.focus();
          return;
        }
      }

      var payload = Object.fromEntries(new FormData(form).entries());
      delete payload.company_website_hp;
      var endpoint = form.getAttribute("data-endpoint");

      var done = function () {
        form.querySelectorAll("input, select, textarea, button").forEach(function (f) { f.disabled = true; });
        say(form.getAttribute("data-success") || "Got it. We come back within one business day.", true);
        track("form-submit");
      };
      if (!endpoint) { done(); return; }
      fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
        .then(done)
        .catch(function () { say("Something went wrong. Message us on Telegram instead.", false); });
    });
  });

  /* ---- 13. CTA tracking ---------------------------------------------------- */
  document.querySelectorAll("[data-cta]").forEach(function (el) {
    el.addEventListener("click", function () { track("cta", { cta: el.getAttribute("data-cta") }); });
  });

  /* ---- 14. Scroll depth ---------------------------------------------------- */
  var hit = {};
  window.addEventListener("scroll", function () {
    var h = document.body.scrollHeight - window.innerHeight;
    if (h <= 0) return;
    var pct = Math.round((window.scrollY / h) * 100);
    [25, 50, 75, 100].forEach(function (mark) {
      if (pct >= mark && !hit[mark]) { hit[mark] = 1; track("scroll-depth", { depth: mark }); }
    });
  }, { passive: true });
})();
