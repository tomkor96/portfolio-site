// Runs in <head> before first paint so a saved theme never flashes the other one.
(function () {
  try {
    var saved = localStorage.getItem("theme");
    if (saved === "light" || saved === "dark") document.documentElement.dataset.theme = saved;
  } catch (e) {
    // Storage blocked (private mode): fall back to the system preference.
  }
})();
