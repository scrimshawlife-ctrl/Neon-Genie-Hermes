/* Neon Genie site — cmdk, copy, reveal, type-in */
(function () {
  "use strict";

  const INSTALL =
    "hermes skills install scrimshawlife-ctrl/Neon-Genie-Hermes/skills/neon-genie";

  /* —— Reveal —— */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length) {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      revealEls.forEach((el) => el.classList.add("is-in"));
    } else {
      const io = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-in");
              io.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
      );
      revealEls.forEach((el) => io.observe(el));
    }
  }

  /* —— Type-in (once) —— */
  const typeTarget = document.getElementById("type-cmd");
  if (typeTarget) {
    const full = typeTarget.dataset.full || INSTALL;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      typeTarget.textContent = full;
    } else {
      let i = 0;
      typeTarget.textContent = "";
      const tick = () => {
        i += 1;
        typeTarget.textContent = full.slice(0, i);
        if (i < full.length) {
          window.setTimeout(tick, 18 + Math.random() * 22);
        } else {
          const cursor = document.getElementById("type-cursor");
          if (cursor) cursor.hidden = true;
        }
      };
      window.setTimeout(tick, 400);
    }
  }

  /* —— Copy install —— */
  function copyInstall(btn) {
    if (!btn || btn.disabled) return;
    const done = () => {
      const prev = btn.textContent;
      btn.dataset.state = "success";
      btn.textContent = "Copied";
      window.setTimeout(() => {
        btn.dataset.state = "";
        btn.textContent = prev;
      }, 1600);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(INSTALL).then(done).catch(() => fallbackCopy(done));
    } else {
      fallbackCopy(done);
    }
  }

  function fallbackCopy(done) {
    const ta = document.createElement("textarea");
    ta.value = INSTALL;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.left = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand("copy");
      done();
    } finally {
      document.body.removeChild(ta);
    }
  }

  document.querySelectorAll("[data-copy-install]").forEach((btn) => {
    btn.addEventListener("click", () => copyInstall(btn));
  });

  /* —— Command palette —— */
  const cmdk = document.getElementById("cmdk");
  const cmdkInput = document.getElementById("cmdk-input");
  const cmdkItems = () => Array.from(document.querySelectorAll(".cmdk__item:not([hidden])"));
  let active = 0;
  let lastFocus = null;

  function openCmdk() {
    if (!cmdk) return;
    lastFocus = document.activeElement;
    cmdk.classList.add("is-open");
    cmdk.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    filterCmdk("");
    if (cmdkInput) {
      cmdkInput.value = "";
      window.setTimeout(() => cmdkInput.focus({ preventScroll: true }), 10);
    }
  }

  function closeCmdk() {
    if (!cmdk) return;
    cmdk.classList.remove("is-open");
    cmdk.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (lastFocus && typeof lastFocus.focus === "function") {
      lastFocus.focus({ preventScroll: true });
    }
  }

  function setActive(i) {
    const items = cmdkItems();
    if (!items.length) return;
    active = (i + items.length) % items.length;
    items.forEach((el, idx) => el.classList.toggle("is-active", idx === active));
    items[active].scrollIntoView({ block: "nearest" });
  }

  function runActive() {
    const items = cmdkItems();
    if (!items.length) return;
    const el = items[active];
    const href = el.getAttribute("data-href");
    const action = el.getAttribute("data-action");
    closeCmdk();
    if (action === "copy-install") {
      const btn = document.querySelector("[data-copy-install]");
      copyInstall(btn);
      return;
    }
    if (href) {
      if (href.startsWith("#")) {
        const t = document.querySelector(href);
        if (t) t.scrollIntoView({ behavior: "smooth" });
        else window.location.hash = href;
      } else {
        window.open(href, el.getAttribute("data-target") || "_self");
      }
    }
  }

  function filterCmdk(q) {
    const query = (q || "").trim().toLowerCase();
    document.querySelectorAll(".cmdk__item").forEach((el) => {
      const hay = (el.getAttribute("data-search") || el.textContent || "").toLowerCase();
      el.hidden = query ? !hay.includes(query) : false;
    });
    document.querySelectorAll(".cmdk__group").forEach((g) => {
      let n = g.nextElementSibling;
      let any = false;
      while (n && !n.classList.contains("cmdk__group")) {
        if (n.classList.contains("cmdk__item") && !n.hidden) any = true;
        n = n.nextElementSibling;
      }
      g.hidden = !any;
    });
    setActive(0);
  }

  document.querySelectorAll("[data-open-cmdk]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      openCmdk();
    });
  });

  if (cmdk) {
    cmdk.querySelectorAll("[data-close]").forEach((el) => {
      el.addEventListener("click", closeCmdk);
    });
    cmdk.querySelectorAll(".cmdk__item").forEach((el) => {
      el.addEventListener("click", () => {
        document.querySelectorAll(".cmdk__item").forEach((x) => x.classList.remove("is-active"));
        el.classList.add("is-active");
        active = cmdkItems().indexOf(el);
        runActive();
      });
      el.addEventListener("mouseenter", () => {
        const items = cmdkItems();
        active = items.indexOf(el);
        items.forEach((x, idx) => x.classList.toggle("is-active", idx === active));
      });
    });
  }

  if (cmdkInput) {
    cmdkInput.addEventListener("input", () => filterCmdk(cmdkInput.value));
  }

  document.addEventListener("keydown", (e) => {
    const metaK = (e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K");
    if (metaK) {
      e.preventDefault();
      if (cmdk && cmdk.classList.contains("is-open")) closeCmdk();
      else openCmdk();
      return;
    }
    if (!cmdk || !cmdk.classList.contains("is-open")) return;
    if (e.key === "Escape") {
      e.preventDefault();
      closeCmdk();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(active + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(active - 1);
    } else if (e.key === "Enter") {
      e.preventDefault();
      runActive();
    }
  });
})();
