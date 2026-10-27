// Runs in <head> before first paint so a saved theme never flashes the other one.
(function () {
  // Lets CSS hide scroll-reveal content only when main.js will be there to show it.
  if ("IntersectionObserver" in window) document.documentElement.classList.add("js");
  try {
    var saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") document.documentElement.dataset.theme = saved;
  } catch (e) {
    // Storage blocked (private mode): fall back to the system preference.
  }
})();
