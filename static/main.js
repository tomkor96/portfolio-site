const root = document.documentElement;

function currentTheme() {
  if (root.dataset.theme) return root.dataset.theme;
  return matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

document.getElementById("theme-toggle").addEventListener("click", () => {
  const next = currentTheme() === "dark" ? "light" : "dark";
  root.dataset.theme = next;
  try {
    localStorage.setItem("theme", next);
  } catch (e) {
    // Not persisted; the choice still applies to this visit.
  }
});

const nav = document.getElementById("nav");
const navToggle = document.getElementById("nav-toggle");

function setNav(open) {
  nav.classList.toggle("is-open", open);
  navToggle.setAttribute("aria-expanded", String(open));
}

navToggle.addEventListener("click", () => setNav(!nav.classList.contains("is-open")));
nav.addEventListener("click", (event) => {
  if (event.target.closest("a")) setNav(false);
});

// Highlight the nav link of the section in view; the hero (#top) has no link and clears it.
const links = new Map([...nav.querySelectorAll("a")].map((a) => [a.hash.slice(1), a]));
const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      links.forEach((a) => a.classList.remove("is-active"));
      links.get(entry.target.id)?.classList.add("is-active");
    }
  },
  { rootMargin: "-45% 0px -50% 0px" },
);
["top", ...links.keys()].forEach((id) => {
  const section = document.getElementById(id);
  if (section) observer.observe(section);
});

// Reveal content as it scrolls in; theme.js adds .js to <html>, so without JS nothing is hidden.
const REVEAL =
  ".section h2, .section__intro, .card, .timeline__item, .skill, .col-title, .plain-list li, .contact .lead, .contact__mail, .links";
const revealTargets = document.querySelectorAll(REVEAL);
const revealObserver = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add("is-visible");
      revealObserver.unobserve(entry.target);
    }
  },
  { rootMargin: "0px 0px -8% 0px" },
);
revealTargets.forEach((el) => {
  // Siblings that enter together appear one after another.
  const index = [...el.parentElement.children].indexOf(el);
  el.style.transitionDelay = `${Math.min(index, 6) * 70}ms`;
  revealObserver.observe(el);
});

// A section reached from the nav gets a short accent on its heading.
function flashSection(id) {
  const heading = document.getElementById(id)?.querySelector("h2");
  if (!heading) return;
  heading.classList.remove("is-flashing");
  void heading.offsetWidth; // restart the animation on repeated clicks
  heading.classList.add("is-flashing");
}
document.querySelectorAll('a[href^="#"]').forEach((a) => {
  a.addEventListener("click", () => flashSection(a.hash.slice(1)));
});

// Lightbox: one shared <dialog>, opened from any project gallery.
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const lightboxCaption = document.getElementById("lightbox-caption");
const lightboxCounter = document.getElementById("lightbox-counter");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
let slides = [];
let current = 0;

function showSlide(index, direction = 0) {
  current = (index + slides.length) % slides.length;
  const slide = slides[current];
  lightboxImg.src = slide.href;
  lightboxImg.alt = slide.querySelector("img")?.alt ?? "";
  lightboxCaption.textContent = slide.dataset.caption ?? "";
  lightboxCounter.textContent = slides.length > 1 ? `${current + 1} / ${slides.length}` : "";
  if (direction && !reducedMotion.matches) {
    lightboxImg.animate(
      [
        { opacity: 0, transform: `translateX(${direction * 48}px) scale(0.98)` },
        { opacity: 1, transform: "none" },
      ],
      { duration: 280, easing: "cubic-bezier(0.22, 1, 0.36, 1)" },
    );
  }
  // Warm the cache so the next arrow press doesn't wait for the network.
  for (const offset of [1, -1]) {
    const neighbour = slides[(current + offset + slides.length) % slides.length];
    if (neighbour) new Image().src = neighbour.href;
  }
}

function openLightbox(link) {
  slides = [...link.closest(".gallery").querySelectorAll("[data-lightbox]")];
  lightbox.classList.toggle("is-single", slides.length < 2);
  showSlide(slides.indexOf(link));
  lightbox.classList.remove("is-closing");
  lightbox.showModal();
}

function closeLightbox() {
  if (!lightbox.open || lightbox.classList.contains("is-closing")) return;
  if (reducedMotion.matches) {
    lightbox.close();
    return;
  }
  lightbox.classList.add("is-closing");
  lightbox.addEventListener(
    "animationend",
    () => {
      lightbox.classList.remove("is-closing");
      lightbox.close();
    },
    { once: true },
  );
}

document.querySelectorAll("[data-lightbox]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    openLightbox(link);
  });
});

document.getElementById("lightbox-close").addEventListener("click", closeLightbox);
document.getElementById("lightbox-prev").addEventListener("click", () => showSlide(current - 1, -1));
document.getElementById("lightbox-next").addEventListener("click", () => showSlide(current + 1, 1));

// A click on the backdrop lands on the <dialog> itself (or the empty frame around the image).
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox || event.target.classList.contains("lightbox__frame")) {
    closeLightbox();
  }
});

// Esc goes through the closing animation instead of the instant native close.
lightbox.addEventListener("cancel", (event) => {
  event.preventDefault();
  closeLightbox();
});

lightbox.addEventListener("keydown", (event) => {
  if (slides.length < 2) return;
  if (event.key === "ArrowRight") showSlide(current + 1, 1);
  if (event.key === "ArrowLeft") showSlide(current - 1, -1);
});

let touchStartX = null;
lightbox.addEventListener("touchstart", (event) => {
  touchStartX = event.touches[0].clientX;
}, { passive: true });
lightbox.addEventListener("touchend", (event) => {
  if (touchStartX === null || slides.length < 2) return;
  const dx = event.changedTouches[0].clientX - touchStartX;
  touchStartX = null;
  if (Math.abs(dx) > 50) showSlide(current + (dx < 0 ? 1 : -1), dx < 0 ? 1 : -1);
});

// Spotlight: cards and skill tiles track the cursor through --x/--y (CSSOM, so the CSP allows it).
if (matchMedia("(hover: hover)").matches && !reducedMotion.matches) {
  document.querySelectorAll(".card, .skill").forEach((el) => {
    el.addEventListener("pointermove", (event) => {
      const box = el.getBoundingClientRect();
      el.style.setProperty("--x", `${event.clientX - box.left}px`);
      el.style.setProperty("--y", `${event.clientY - box.top}px`);
    });
  });
}
// Live status and the latest newsletter issue, from /live/live.json (cron on the server, every
// 5 minutes). No file, a failed request or stale data leaves everything hidden: never a false "live".
const STALE_AFTER_MS = 30 * 60 * 1000;
const LIVE_TEXTS = {
  pl: { down: "niedostępna", checked: "sprawdzono", now: "przed chwilą", ago: (m) => `${m} min temu` },
  en: { down: "down", checked: "checked", now: "just now", ago: (m) => `${m} min ago` },
};
const liveText = LIVE_TEXTS[document.documentElement.lang] ?? LIVE_TEXTS.pl;

function minutesAgo(date) {
  const minutes = Math.max(0, Math.round((Date.now() - date) / 60000));
  return minutes === 0 ? liveText.now : liveText.ago(minutes);
}

function showStatus(badge, check, checkedAt) {
  const label = badge.querySelector("[data-live-label]");
  badge.classList.add(check.up ? "badge--live" : "badge--down");
  label.textContent = check.up ? "live" : liveText.down;
  badge.title = `${liveText.checked} ${minutesAgo(checkedAt)}${check.up ? ` · ${check.ms} ms` : ""}`;
  badge.hidden = false;
}

function showLatestIssue(issue) {
  document.querySelectorAll("[data-latest-issue]").forEach((el) => {
    const link = el.matches("a") ? el : el.querySelector("a");
    link.href = issue.url;
    link.title = issue.title;
    el.querySelectorAll("[data-latest-number]").forEach((n) => {
      n.textContent = issue.number ? `#${issue.number}` : "";
    });
    el.querySelectorAll("[data-latest-title]").forEach((t) => (t.textContent = issue.title));
    el.querySelectorAll("[data-latest-date]").forEach((d) => {
      d.textContent = issue.date ? ` · ${issue.date}` : "";
    });
    el.hidden = false;
  });
}

fetch("/live/live.json", { cache: "no-store" })
  .then((response) => (response.ok ? response.json() : Promise.reject(response.status)))
  .then((live) => {
    const checkedAt = new Date(live.checked_at);
    if (!(Date.now() - checkedAt < STALE_AFTER_MS)) return;
    document.querySelectorAll("[data-live-url]").forEach((badge) => {
      const check = live.projects?.[badge.dataset.liveUrl];
      if (check) showStatus(badge, check, checkedAt);
    });
    const newsletter = Object.values(live.projects ?? {}).find((p) => p.latest_issue);
    if (newsletter) showLatestIssue(newsletter.latest_issue);
  })
  .catch(() => {
    // No status file (local preview, CI) or a network error: badges simply stay hidden.
  });
