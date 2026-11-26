/* raddgames.com: a few small niceties, no libraries, no tracking.
   1. The menu button on phones.
   1b. Email links on computers: a small chooser (Gmail in the browser, the computer's mail app,
       or copy the address), because a bare mailto link does nothing where no mail app is set up.
       Phones open their mail app directly, which works.
   2. Screenshot carousels: arrows, dots and "1–4 of 8", always inside the page.
   3. Raddy's eyes follow the pointer (and wander on touch screens).
   4. Things rise into place as they scroll into view. */
(function () {
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var calm = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // 1. Menu
  var head = document.querySelector(".site-head");
  var menu = head && head.querySelector(".menu-btn");
  if (menu) {
    menu.addEventListener("click", function () {
      var open = head.classList.toggle("open");
      menu.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && head.classList.contains("open")) { head.classList.remove("open"); menu.setAttribute("aria-expanded", "false"); menu.focus(); }
    });
  }

  // 1b. Email chooser (computers only)
  var fine = window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (fine) {
    var pop = null, opener = null;
    var enc = encodeURIComponent;
    function parseMail(href) {
      var rest = href.slice(7), i = rest.indexOf("?");
      var q = new URLSearchParams(i < 0 ? "" : rest.slice(i + 1));
      return { to: decodeURIComponent(i < 0 ? rest : rest.slice(0, i)), su: q.get("subject") || "", body: q.get("body") || "" };
    }
    function closeMenu(back) {
      if (!pop) return;
      pop.parentNode.removeChild(pop); pop = null;
      if (back && opener) opener.focus();
    }
    function copyText(text, done) {
      function fallback() {
        var t = document.createElement("textarea");
        t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
        document.body.appendChild(t); t.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(t); done();
      }
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback); else fallback();
    }
    function item(tag, label, note) {
      var el = document.createElement(tag);
      el.className = "mm-item";
      el.innerHTML = "<span></span><small></small>";
      el.firstChild.textContent = label; el.lastChild.textContent = note || "";
      return el;
    }
    function openMenu(a) {
      closeMenu(false);
      opener = a;
      var m = parseMail(a.getAttribute("href"));
      var gmail = "https://mail.google.com/mail/?view=cm&fs=1&to=" + enc(m.to) + (m.su ? "&su=" + enc(m.su) : "") + (m.body ? "&body=" + enc(m.body) : "");
      pop = document.createElement("div");
      pop.className = "mailmenu";
      pop.setAttribute("role", "dialog");
      pop.setAttribute("aria-label", "Email " + m.to);
      var to = document.createElement("p"); to.className = "mm-to"; to.textContent = m.to; pop.appendChild(to);
      var g = item("a", "Write in Gmail", "opens a new tab"); g.href = gmail; g.target = "_blank"; g.rel = "noopener";
      var app = item("a", "Use my email app", "Outlook, Mail…"); app.href = a.getAttribute("href");
      var cp = item("button", "Copy the address", ""); cp.type = "button";
      cp.addEventListener("click", function () {
        copyText(m.to, function () { cp.firstChild.textContent = "Copied ✓"; setTimeout(function () { closeMenu(true); }, 900); });
      });
      [g, app].forEach(function (x) { x.addEventListener("click", function () { setTimeout(function () { closeMenu(false); }, 0); }); });
      pop.appendChild(g); pop.appendChild(app); pop.appendChild(cp);
      document.body.appendChild(pop);
      var r = a.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight;
      var left = Math.min(Math.max(12, r.left + r.width / 2 - w / 2), document.documentElement.clientWidth - w - 12);
      var top = r.bottom + 8;
      if (top + h > window.innerHeight - 8 && r.top - h - 8 > 8) top = r.top - h - 8;
      pop.style.left = (left + window.scrollX) + "px";
      pop.style.top = (top + window.scrollY) + "px";
      g.focus();
    }
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[href^="mailto:"]');
      if (a && !a.closest(".mailmenu")) { e.preventDefault(); openMenu(a); return; }
      if (pop && !pop.contains(e.target)) closeMenu(false);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && pop) closeMenu(true); });
    window.addEventListener("resize", function () { closeMenu(false); });
  }

  // 2. Carousels
  [].slice.call(document.querySelectorAll("[data-carousel]")).forEach(function (box) {
    var track = box.querySelector(".track");
    var prev = box.querySelector(".arrow.prev");
    var next = box.querySelector(".arrow.next");
    var dots = box.nextElementSibling && box.nextElementSibling.classList.contains("dots") ? box.nextElementSibling : null;
    var count = box.parentNode.querySelector(".count");
    var figs = [].slice.call(track.children);
    var total = figs.length;
    var built = -1;

    function step() { return figs.length > 1 ? figs[1].offsetLeft - figs[0].offsetLeft : track.clientWidth; }
    function perView() { return Math.max(1, Math.round(track.clientWidth / step())); }
    function first() { return Math.min(total - 1, Math.max(0, Math.round(track.scrollLeft / step()))); }
    function pages() { return Math.max(1, Math.ceil((total - perView()) / perView()) + 1); }

    function go(index) {
      index = Math.max(0, Math.min(total - 1, index));
      track.scrollTo({ left: figs[index].offsetLeft - figs[0].offsetLeft, behavior: calm ? "auto" : "smooth" });
    }

    function buildDots() {
      if (!dots) return;
      var n = pages();
      if (n === built) return;
      built = n;
      dots.innerHTML = "";
      for (var i = 0; i < n; i++) {
        var b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", "Pictures, page " + (i + 1) + " of " + n);
        (function (p) { b.addEventListener("click", function () { go(p * perView()); }); })(i);
        dots.appendChild(b);
      }
    }

    function update() {
      var pv = perView();
      var f = first();
      var atEnd = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
      var fits = track.scrollWidth <= track.clientWidth + 4;
      box.classList.toggle("fits", fits);
      prev.disabled = f <= 0 && track.scrollLeft < 4;
      next.disabled = atEnd;
      buildDots();
      if (dots) {
        var page = atEnd ? dots.children.length - 1 : Math.round(f / pv);
        [].forEach.call(dots.children, function (d, i) { d.setAttribute("aria-current", i === page ? "true" : "false"); });
      }
      if (count) {
        var last = atEnd ? total : Math.min(total, f + pv);
        var from = atEnd ? Math.max(1, total - pv + 1) : f + 1;
        count.textContent = fits ? total + " pictures" : (from === last ? from + " of " + total : from + "–" + last + " of " + total);
      }
    }

    prev.addEventListener("click", function () { go(first() - perView()); });
    next.addEventListener("click", function () { go(first() + perView()); });
    track.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); go(first() + 1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(first() - 1); }
    });
    var t = 0;
    track.addEventListener("scroll", function () { cancelAnimationFrame(t); t = requestAnimationFrame(update); }, { passive: true });
    window.addEventListener("resize", function () { built = -1; update(); });
    update();
  });

  // 3. Eyes
  var eyes = [].slice.call(document.querySelectorAll(".raddy .eye"));
  function look(x, y) {
    eyes.forEach(function (eye) {
      var pupil = eye.querySelector(".pupil");
      if (!pupil) return;
      var box = eye.getBoundingClientRect();
      if (!box.width) return;
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

  // 4. Reveal on scroll
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
