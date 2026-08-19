/* Two progressive enhancements. The site is fully usable without this file. */
(function () {
  "use strict";

  // 1. Collapsible section navigation on narrow screens.
  var sidebar = document.querySelector(".sidebar");
  var groups = sidebar && sidebar.querySelector(".nav-groups");
  if (sidebar && groups) {
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "nav-toggle";
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-controls", "section-nav");
    groups.id = "section-nav";

    var current = sidebar.querySelector('a[aria-current="page"]');
    toggle.textContent = current ? current.textContent : "Sections";

    toggle.addEventListener("click", function () {
      var open = sidebar.getAttribute("data-open") === "true";
      sidebar.setAttribute("data-open", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
    });

    sidebar.insertBefore(toggle, groups);
  }

  // 2. Mark the section currently being read in the on-page contents.
  //
  // Driven by scroll position rather than intersection: these sections are far
  // taller than the viewport, so an observer-only approach leaves the highlight
  // frozen for long stretches where no heading enters or leaves the detection
  // band. Reading position is simply the last heading scrolled past.
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (!links.length) return;

  var entries = [];
  links.forEach(function (link) {
    var heading = document.getElementById(decodeURIComponent(link.hash.slice(1)));
    if (heading) entries.push({ link: link, heading: heading });
  });
  if (!entries.length) return;

  var active = null;

  function paint() {
    // A heading counts as current once its top passes just below the header.
    var line = 96;
    var found = entries[0];

    for (var i = 0; i < entries.length; i++) {
      if (entries[i].heading.getBoundingClientRect().top <= line) {
        found = entries[i];
      } else {
        break;
      }
    }

    // At the very bottom, prefer the last section: its heading may sit above
    // the line while the page can scroll no further.
    var atBottom = window.innerHeight + window.scrollY >= document.body.scrollHeight - 2;
    if (atBottom) found = entries[entries.length - 1];

    if (found.link === active) return;
    if (active) active.classList.remove("active");
    found.link.classList.add("active");
    active = found.link;
  }

  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(function () {
      queued = false;
      paint();
    });
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  window.addEventListener("hashchange", onScroll);
  paint();
})();
