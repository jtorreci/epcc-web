/* Three-plane scroll parallax (grid 0.2x, drawings 0.5x, content 1x).
   One mechanism for every browser: a passive scroll listener + rAF writes
   custom properties that site.css consumes. Each drawing is anchored to a
   section transition (first one to the hero) and draws in as it reaches
   the viewport centre, undrawing as it leaves. Reduced motion: drawings
   are placed once, fully drawn, and nothing moves with scroll. */
(function () {
  'use strict';
  var root = document.documentElement;
  if (/[?&]tema=claro\b/.test(location.search)) root.setAttribute('data-theme', 'light');

  var layers = document.querySelector('.layers');
  var scenes = layers ? [].slice.call(layers.querySelectorAll('.scene')) : [];
  var sections = [].slice.call(document.querySelectorAll('main > section'));
  if (!scenes.length || !sections.length) return;

  var GRID = 0.2, ART = 0.5, CELL = 120;
  var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  var still = false, vh = 0, anchors = [], queued = false;

  function docTop(el) { return el.getBoundingClientRect().top + window.pageYOffset; }

  // Anchor = document Y that sits at the viewport centre when its drawing is centred.
  function anchorFor(i) {
    if (i === 0) return vh / 2;
    var prev = sections[i - 1], cur = sections[i];
    return (docTop(prev) + prev.offsetHeight + docTop(cur)) / 2;
  }

  function layout() {
    still = !!(mq && mq.matches);
    vh = window.innerHeight;
    var speed = still ? 1 : ART;
    var maxY = Math.max(0, root.scrollHeight - vh);
    anchors = scenes.map(function (svg, i) {
      if (!sections[i]) { svg.style.display = 'none'; return null; }
      var a = Math.min(anchorFor(i), maxY + vh / 2);
      var h = svg.getBoundingClientRect().width * 0.75;
      // Screen top = top - speed * scrollY; centred when scrollY = a - vh/2.
      svg.style.top = (speed * a + (1 - speed) * vh / 2 - h / 2) + 'px';
      return a;
    });
    update();
  }

  function update() {
    queued = false;
    var y = window.pageYOffset;
    layers.style.setProperty('--gy', still ? 0 : ((y * GRID) % CELL).toFixed(1));
    layers.style.setProperty('--ay', still ? 0 : (y * (1 - ART)).toFixed(1));
    scenes.forEach(function (svg, i) {
      var a = anchors[i];
      if (a == null) return;
      if (still) { svg.style.setProperty('--p', 0); svg.style.setProperty('--o', 1); return; }
      // t: drawing centre offset from viewport centre, in viewport heights.
      var t = ART * (a - vh / 2 - y) / vh, d = Math.abs(t);
      var draw = Math.min(1, Math.max(0, (d - 0.1) / 0.35));
      var fade = Math.min(1, Math.max(0, (d - 0.3) / 0.3));
      svg.style.setProperty('--p', (t < 0 ? -draw : draw).toFixed(3));
      svg.style.setProperty('--o', (1 - fade).toFixed(3));
    });
  }

  function request() {
    if (!queued) { queued = true; window.requestAnimationFrame(update); }
  }

  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', layout, { passive: true });
  window.addEventListener('load', layout);
  if (window.ResizeObserver) new ResizeObserver(function () { layout(); }).observe(document.body);
  if (mq && mq.addEventListener) mq.addEventListener('change', layout);
  layout();
})();
