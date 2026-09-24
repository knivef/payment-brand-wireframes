/* ==========================================================================
   Shared conversion behaviours. Zero dependencies. Loaded with `defer`.
   Everything is opt-in via data attributes so a brand page only gets what
   it declares in its markup.
   ========================================================================== */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var store = {
    get: function (k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { window.localStorage.setItem(k, v); } catch (e) { /* no-op */ } }
  };

  /* ---- 1. Sticky nav shadow on scroll ---------------------------------- */
  var nav = document.querySelector("[data-nav]");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("is-stuck", window.scrollY > 32); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---- 2. Scroll reveal ------------------------------------------------ */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && !reduced && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---- 3. Countdown timer ---------------------------------------------- */
  /* <span data-countdown data-deadline="2026-12-31T23:59:59Z"></span>
     Falls back to a rolling 72h window per visitor if no deadline is set,
     which keeps urgency honest-looking without a fake fixed date. */
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var deadline = el.getAttribute("data-deadline");
    var end;
    if (deadline) {
      end = new Date(deadline).getTime();
    } else {
      var key = "cdw:" + (el.getAttribute("data-key") || "default");
      var saved = store.get(key);
      var hours = parseInt(el.getAttribute("data-hours") || "72", 10);
      end = saved ? parseInt(saved, 10) : Date.now() + hours * 3600000;
      if (!saved) { store.set(key, String(end)); }
    }
    var pad = function (n) { return n < 10 ? "0" + n : String(n); };
    var tick = function () {
      var left = end - Date.now();
      if (left <= 0) { el.textContent = "00:00:00"; return; }
      var d = Math.floor(left / 86400000);
      var h = Math.floor((left % 86400000) / 3600000);
      var m = Math.floor((left % 3600000) / 60000);
      var s = Math.floor((left % 60000) / 1000);
      el.textContent = (d > 0 ? d + "d " : "") + pad(h) + ":" + pad(m) + ":" + pad(s);
      window.setTimeout(tick, 1000);
    };
    tick();
  });

  /* ---- 4. Dismissible announcement bar ---------------------------------- */
  var announce = document.querySelector("[data-announce]");
  if (announce) {
    var aKey = "announce-dismissed:" + (announce.getAttribute("data-key") || "v1");
    if (store.get(aKey) === "1") {
      announce.remove();
    } else {
      var closeBtn = announce.querySelector("[data-announce-close]");
      if (closeBtn) {
        closeBtn.addEventListener("click", function () {
          announce.remove();
          store.set(aKey, "1");
        });
      }
    }
  }

  /* ---- 5. Sticky bottom CTA bar, appears past the hero ------------------ */
  var sticky = document.querySelector("[data-stickybar]");
  if (sticky) {
    var trigger = document.querySelector("[data-stickybar-after]") || document.querySelector(".hero");
    if (trigger && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        sticky.classList.toggle("is-visible", !entries[0].isIntersecting);
      }, { threshold: 0 }).observe(trigger);
    } else {
      sticky.classList.add("is-visible");
    }
  }

  /* ---- 6. Modal open / close ------------------------------------------- */
  var openModal = function (modal) {
    if (!modal || modal.classList.contains("is-open")) { return; }
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    var focusable = modal.querySelector("input, button, select, textarea, a[href]");
    if (focusable) { focusable.focus(); }
  };
  var closeModal = function (modal) {
    if (!modal) { return; }
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
  };

  document.querySelectorAll("[data-modal-open]").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      openModal(document.getElementById(btn.getAttribute("data-modal-open")));
    });
  });
  document.querySelectorAll("[data-modal]").forEach(function (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === modal || e.target.hasAttribute("data-modal-close")) { closeModal(modal); }
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { document.querySelectorAll(".modal.is-open").forEach(closeModal); }
  });

  /* ---- 7. Exit intent, once per visitor --------------------------------- */
  var exitModal = document.querySelector("[data-exit-intent]");
  if (exitModal) {
    var eKey = "exit-shown:" + (exitModal.getAttribute("data-key") || "v1");
    if (store.get(eKey) !== "1") {
      var fired = false;
      var fire = function () {
        if (fired) { return; }
        fired = true;
        openModal(exitModal);
        store.set(eKey, "1");
        document.removeEventListener("mouseout", desktopHandler);
        window.removeEventListener("scroll", mobileHandler);
      };
      var desktopHandler = function (e) {
        if (!e.relatedTarget && e.clientY <= 0) { fire(); }
      };
      document.addEventListener("mouseout", desktopHandler);
      // Mobile has no exit intent, so use dwell plus scroll depth instead.
      var armed = false;
      window.setTimeout(function () { armed = true; }, 25000);
      var mobileHandler = function () {
        if (!armed || window.innerWidth > 820) { return; }
        var depth = (window.scrollY + window.innerHeight) / document.body.scrollHeight;
        if (depth > 0.55) { fire(); }
      };
      window.addEventListener("scroll", mobileHandler, { passive: true });
    }
  }

  /* ---- 8. FAQ accordion, single open at a time -------------------------- */
  var faqItems = document.querySelectorAll(".faq details");
  faqItems.forEach(function (item) {
    item.addEventListener("toggle", function () {
      if (!item.open) { return; }
      faqItems.forEach(function (other) { if (other !== item) { other.open = false; } });
    });
  });

  /* ---- 9. Lead form, inline success, honeypot, free-email block ---------- */
  var FREE_EMAIL = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "proton.me", "protonmail.com", "aol.com", "mail.com", "yandex.com"];

  document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
    var startedAt = Date.now();
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector("[data-form-status]");
      var say = function (msg, ok) {
        if (!status) { return; }
        status.textContent = msg;
        status.style.color = ok ? "var(--positive)" : "var(--negative)";
      };

      if (form.querySelector(".hp") && form.querySelector(".hp").value) { return; }
      if (Date.now() - startedAt < 2000) { say("Take a moment and try again.", false); return; }

      var emailField = form.querySelector("input[type=email]");
      if (emailField && form.hasAttribute("data-block-free-email")) {
        var domain = (emailField.value.split("@")[1] || "").toLowerCase();
        if (FREE_EMAIL.indexOf(domain) !== -1) {
          say("Please use your work email so we can verify the business.", false);
          emailField.focus();
          return;
        }
      }

      var endpoint = form.getAttribute("data-endpoint");
      var payload = Object.fromEntries(new FormData(form).entries());
      delete payload.company_website_hp;

      var done = function () {
        form.querySelectorAll("input, select, textarea, button").forEach(function (f) { f.disabled = true; });
        say(form.getAttribute("data-success") || "Got it. We will come back to you within 48 hours.", true);
      };

      if (!endpoint) { done(); return; }
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      }).then(done).catch(function () { say("Something went wrong. Email us instead.", false); });
    });
  });

  /* ---- 10. CTA click tracking hook -------------------------------------- */
  /* Fires a window event any analytics script can listen for without this
     file knowing which analytics vendor the brand uses. */
  document.querySelectorAll("[data-cta]").forEach(function (el) {
    el.addEventListener("click", function () {
      window.dispatchEvent(new CustomEvent("wf:cta", {
        detail: { label: el.getAttribute("data-cta"), path: window.location.pathname }
      }));
    });
  });
})();
