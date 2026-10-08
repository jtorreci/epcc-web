/* Minimal carousel: one image visible at a time, prev/next buttons,
   clickable dots, auto-advance every 6s that pauses on hover and
   when the carousel is offscreen (IntersectionObserver). Respects
   prefers-reduced-motion: no auto-advance, no transition. */
(function () {
  'use strict';

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var galleries = document.querySelectorAll('.gallery');
  galleries.forEach(function (root) {
    var track = root.querySelector('.gallery-track');
    if (!track) return;
    var images = track.querySelectorAll('img');
    if (images.length < 2) return;
    var prevBtn = root.querySelector('.gallery-btn-prev');
    var nextBtn = root.querySelector('.gallery-btn-next');
    var dotsContainer = root.querySelector('.gallery-dots');
    // Generate dots dynamically so HTML stays minimal.
    if (dotsContainer && !dotsContainer.children.length) {
      images.forEach(function (_, idx) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('aria-label', 'Foto ' + (idx + 1));
        dotsContainer.appendChild(b);
      });
    }
    var dots = dotsContainer ? dotsContainer.querySelectorAll('button') : [];
    var current = 0;
    var timer = null;

    function show(i) {
      current = (i + images.length) % images.length;
      images.forEach(function (img, idx) {
        img.classList.toggle('is-active', idx === current);
      });
      dots.forEach(function (dot, idx) {
        dot.setAttribute('aria-current', idx === current ? 'true' : 'false');
      });
    }
    function next() { show(current + 1); }
    function prev() { show(current - 1); }

    show(0);
    if (prevBtn) prevBtn.addEventListener('click', function () { prev(); restart(); });
    if (nextBtn) nextBtn.addEventListener('click', function () { next(); restart(); });
    dots.forEach(function (dot, idx) {
      dot.addEventListener('click', function () { show(idx); restart(); });
    });

    function start() {
      if (reduce) return;
      if (timer) return;
      timer = setInterval(next, 6000);
    }
    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
    }
    function restart() { stop(); start(); }

    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', start);

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) start(); else stop();
        });
      }, { threshold: 0.25 });
      io.observe(root);
    } else {
      start();
    }
  });
})();
