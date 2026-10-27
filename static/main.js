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
