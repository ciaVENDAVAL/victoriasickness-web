/* Sage smoke: a soft puff with a tiny ember rises from every tap / click.
   Canvas overlay, no pointer events, runs only while smoke is on screen.
   Off with prefers-reduced-motion or the accessibility "stop animations" option. */
(() => {
  const root = document.documentElement;
  const still = () => matchMedia('(prefers-reduced-motion: reduce)').matches || root.classList.contains('a11y-motion');
  const cv = document.createElement('canvas');
  cv.className = 'smoke'; cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);
  const ctx = cv.getContext('2d');
  let W = 0, H = 0, dpr = 1, parts = [], embers = [], running = false, last = 0;

  const size = () => {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth; H = innerHeight;
    cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  };
  size(); addEventListener('resize', size);

  // pick the smoke colour from the background under the tap: pale sage on dark, deeper sage on light
  const SAGE_ON_DARK = [205, 216, 196], SAGE_ON_LIGHT = [92, 112, 84];
  const bgIsLight = (x, y) => {
    let el = document.elementFromPoint(x, y);
    while (el && el !== document.documentElement) {
      const c = getComputedStyle(el).backgroundColor.match(/[\d.]+/g);
      if (c && (c.length < 4 || +c[3] > .5)) return (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) > 150;
      el = el.parentElement;
    }
    return root.classList.contains('a11y-light');
  };

  // an emitter releases a thin stream for ~0.7 s, like a smouldering sage bundle
  let emitters = [];
  const wisp = (x, y, k, light) => ({
    c: light ? SAGE_ON_LIGHT : SAGE_ON_DARK, boost: light ? 1.9 : 1,
    x: x + (Math.random() - .5) * 3, y,
    vx: (Math.random() - .5) * 6, vy: -(48 + Math.random() * 34),
    r: 1.8 + Math.random() * 2.4, grow: 12 + Math.random() * 18,
    life: 0, max: 2.6 + Math.random() * 1.8,
    wob: k * 5 + Math.random() * .8, wobS: 2.2 + Math.random() * .8, wobA: 4 + Math.random() * 6,
    a: .06 + Math.random() * .06,
  });
  const puff = (x, y) => {
    if (still()) return;
    emitters.push({ x, y, t: 0, dur: .7, acc: 0, light: bgIsLight(x, y) });
    embers.push({ x, y, life: 0, max: .5 });
    if (!running) { running = true; last = performance.now(); requestAnimationFrame(tick); }
  };

  const tick = now => {
    const dt = Math.min(.05, (now - last) / 1000); last = now;
    ctx.clearRect(0, 0, W, H);
    emitters = emitters.filter(em => {
      em.t += dt; em.acc += dt * 60;                       // ~60 wisps per second
      while (em.acc >= 1) { em.acc--; parts.push(wisp(em.x, em.y, em.t, em.light)); }
      return em.t < em.dur;
    });
    ctx.globalCompositeOperation = 'source-over';
    parts = parts.filter(p => {
      p.life += dt; if (p.life >= p.max) return false;
      const k = p.life / p.max;
      // curl grows with height, so the ribbon starts straight and twists as it rises
      p.x += (p.vx + Math.sin(p.wob + p.life * p.wobS) * p.wobA * (1 + p.life * 2.4)) * dt;
      p.y += p.vy * dt; p.vy *= .995; p.vx *= .99;
      const rad = p.r + p.grow * k;
      const [r, g, b] = p.c;
      const alpha = p.a * p.boost * Math.sin(Math.PI * Math.min(1, k * 1.15));          // fade in, then out
      const gr = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, rad);
      gr.addColorStop(0, `rgba(${r},${g},${b},${alpha})`);
      gr.addColorStop(.55, `rgba(${r},${g},${b},${alpha * .45})`);
      gr.addColorStop(1, `rgba(${r},${g},${b},0)`);
      ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(p.x, p.y, rad, 0, 6.2832); ctx.fill();
      return true;
    });
    ctx.globalCompositeOperation = 'lighter';
    embers = embers.filter(e => {
      e.life += dt; if (e.life >= e.max) return false;
      const k = 1 - e.life / e.max, rad = 2 + 5 * k;
      const gr = ctx.createRadialGradient(e.x, e.y, 0, e.x, e.y, rad * 2.2);
      gr.addColorStop(0, `rgba(255,190,120,${.85 * k})`);
      gr.addColorStop(.4, `rgba(232,80,40,${.45 * k})`);
      gr.addColorStop(1, 'rgba(232,0,79,0)');
      ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(e.x, e.y, rad * 2.2, 0, 6.2832); ctx.fill();
      return true;
    });
    if (parts.length || embers.length || emitters.length) requestAnimationFrame(tick);
    else { running = false; ctx.clearRect(0, 0, W, H); }
  };

  // pointerdown covers mouse clicks and touches; ignore secondary buttons and extra fingers
  addEventListener('pointerdown', e => {
    if (e.button > 0 || !e.isPrimary) return;
    puff(e.clientX, e.clientY);
  }, { passive: true });
})();
