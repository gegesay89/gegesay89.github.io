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

  // 2. Mark the section currently in view in the on-page contents.
  var links = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
  if (!links.length || !("IntersectionObserver" in window)) return;

  var byId = {};
  var headings = [];
  links.forEach(function (link) {
    var id = decodeURIComponent(link.hash.slice(1));
    var heading = document.getElementById(id);
    if (heading) {
      byId[id] = link;
      headings.push(heading);
    }
  });
  if (!headings.length) return;

  var visible = [];

  function paint() {
    var id = visible.length
      ? visible[0]
      : (function () {
          // Nothing intersecting: fall back to the last heading scrolled past.
          var above = headings.filter(function (h) {
            return h.getBoundingClientRect().top < 100;
          });
          return above.length ? above[above.length - 1].id : headings[0].id;
        })();

    links.forEach(function (link) {
      link.classList.remove("active");
    });
    if (byId[id]) byId[id].classList.add("active");
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        var id = entry.target.id;
        var at = visible.indexOf(id);
        if (entry.isIntersecting && at === -1) visible.push(id);
        if (!entry.isIntersecting && at !== -1) visible.splice(at, 1);
      });
      visible.sort(function (a, b) {
        return headings.indexOf(document.getElementById(a)) - headings.indexOf(document.getElementById(b));
      });
      paint();
    },
    { rootMargin: "-88px 0px -70% 0px" }
  );

  headings.forEach(function (heading) {
    observer.observe(heading);
  });
  paint();
})();
