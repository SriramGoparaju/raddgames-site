/* raddgames.com: two small niceties, no libraries, no tracking.
   1. Raddy's eyes follow the pointer (and wander on touch screens).
   2. Things rise into place as they scroll into view. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. Eyes
  var eyes = [].slice.call(document.querySelectorAll(".raddy .eye"));
  function look(x, y) {
    eyes.forEach(function (eye) {
      var pupil = eye.querySelector(".pupil");
      if (!pupil) return;
      var box = eye.getBoundingClientRect();
      var cx = box.left + box.width / 2, cy = box.top + box.height / 2;
      var dx = x - cx, dy = y - cy;
      var far = Math.sqrt(dx * dx + dy * dy) || 1;
      var reach = Math.min(1, far / 160) * 3.2;            // SVG units: the pupil stays inside the white
      pupil.style.transform = "translate(" + (dx / far * reach).toFixed(2) + "px, " + (dy / far * reach).toFixed(2) + "px)";
    });
  }
  if (eyes.length && !calm) {
    var last = 0;
    window.addEventListener("pointermove", function (e) {
      var now = Date.now();
      if (now - last < 30) return;
      last = now;
      look(e.clientX, e.clientY);
    }, { passive: true });
    if (window.matchMedia && window.matchMedia("(hover: none)").matches) {
      setInterval(function () {
        look(Math.random() * window.innerWidth, Math.random() * window.innerHeight);
      }, 1800);
    }
  }

  // 2. Reveal on scroll
  var items = [].slice.call(document.querySelectorAll("[data-reveal]"));
  if (!items.length) return;
  if (calm || !("IntersectionObserver" in window)) {
    items.forEach(function (el) { el.classList.add("in"); });
    return;
  }
  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add("in"); seen.unobserve(entry.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
  items.forEach(function (el) { seen.observe(el); });
})();
