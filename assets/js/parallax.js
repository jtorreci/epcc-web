/* Scroll fallback for browsers without CSS scroll-driven animations.
   Mirrors the keyframes in site.css; does nothing when native support
   exists or the user prefers reduced motion. */
(function () {
  'use strict';
  var root = document.documentElement;
  var native = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (native || reduce) return;

  var grid = document.querySelector('.layer-grid');
  var art = document.querySelector('.layer-art');
  var scenes = Array.prototype.slice.call(document.querySelectorAll('.scene'));
  if (!art || !scenes.length) return;

  var ranges = scenes.map(function (el) {
    var cs = getComputedStyle(el);
    var from = parseFloat(cs.getPropertyValue('--from')) || 0;
    var to = parseFloat(cs.getPropertyValue('--to')) || 100;
    return [from / 100, to / 100];
  });

  // Returns [opacity, dashoffset] for local progress t within a scene range.
  function state(t, first, last) {
    if (first) t = Math.max(t, 0.35);
    if (last) t = Math.min(t, 0.65);
    if (t <= 0) return [0, 1];
    if (t >= 1) return [0, -1];
    if (t < 0.35) return [t / 0.35, 1 - t / 0.35];
    if (t <= 0.65) return [1, 0];
    var k = (t - 0.65) / 0.35;
    return [1 - k, -k];
  }

  var queued = false;
  function update() {
    queued = false;
    var max = root.scrollHeight - window.innerHeight;
    var p = max > 0 ? Math.min(Math.max(window.scrollY / max, 0), 1) : 0;
    if (grid) grid.style.transform = 'translate3d(0,' + (-12 * p) + 'vh,0)';
    art.style.transform = 'translate3d(0,' + (4 - 20 * p) + 'vh,0)';
    scenes.forEach(function (el, i) {
      var r = ranges[i];
      var s = state((p - r[0]) / (r[1] - r[0]), i === 0, i === scenes.length - 1);
      el.style.opacity = s[0].toFixed(3);
      el.style.strokeDashoffset = s[1].toFixed(3);
    });
  }

  function request() {
    if (!queued) { queued = true; window.requestAnimationFrame(update); }
  }

  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request, { passive: true });
  update();
})();
