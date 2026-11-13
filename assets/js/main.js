/* cia. Victoria Sickness — interactions
   - hero video pause/play (+ reduced motion)
   - lite YouTube embeds (no third-party load until click)
   - custom cursor; long press = hand getting a manicure (mouse + touch)
*/
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch {} },
  };

  /* ---------- hero video ---------- */
  const video = document.querySelector('.hero__video');
  const toggle = document.querySelector('.hero__toggle');
  if (video && toggle) {
    const label = toggle.querySelector('.sr');
    const sync = () => {
      const paused = video.paused;
      toggle.setAttribute('aria-pressed', String(paused));
      label.textContent = paused ? toggle.dataset.play : toggle.dataset.pause;
    };
    if (reduce || document.documentElement.classList.contains('a11y-motion')) video.removeAttribute('autoplay'), video.pause();
    toggle.addEventListener('click', () => { video.paused ? video.play() : video.pause(); });
    video.addEventListener('play', sync); video.addEventListener('pause', sync); sync();
  }

  /* ---------- header hides on scroll down ---------- */
  const header = document.querySelector('.site-header');
  let lastY = scrollY;
  addEventListener('scroll', () => {
    const y = scrollY;
    header.classList.toggle('is-hidden', y > lastY && y > 400);
    lastY = y;
  }, { passive: true });
  header.addEventListener('focusin', () => header.classList.remove('is-hidden'));

  /* ---------- lite YouTube ---------- */
  document.querySelectorAll('.yt').forEach(btn => btn.addEventListener('click', () => {
    const f = document.createElement('iframe');
    f.className = 'yt-frame';
    f.src = `https://www.youtube-nocookie.com/embed/${btn.dataset.yt}?autoplay=1&rel=0`;
    f.title = btn.dataset.title;
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    btn.replaceWith(f);
    f.focus();
  }));

  /* ---------- language menu: close on outside click / Escape ---------- */
  const lang = document.querySelector('.lang');
  if (lang) {
    document.addEventListener('click', e => { if (lang.open && !lang.contains(e.target)) lang.open = false; });
    lang.addEventListener('keydown', e => { if (e.key === 'Escape') { lang.open = false; lang.querySelector('summary').focus(); } });
  }

  /* ---------- lightbox ---------- */
  const lb = document.querySelector('.lightbox');
  if (lb && lb.showModal) {
    const lbImg = lb.querySelector('.lightbox__img');
    const lbCap = lb.querySelector('.lightbox__cap');
    let items = [], idx = 0, opener = null;
    const show = i => {
      idx = (i + items.length) % items.length;
      const a = items[idx];
      lbImg.style.animation = 'none'; void lbImg.offsetWidth; lbImg.style.animation = '';
      lbImg.src = a.href;
      lbImg.alt = a.querySelector('img').alt;
      lbCap.textContent = a.dataset.caption || '';
      // preload neighbour
      const n = items[(idx + 1) % items.length]; if (n) new Image().src = n.href;
    };
    document.querySelectorAll('[data-gallery]').forEach(g => {
      const links = [...g.querySelectorAll('a')];
      links.forEach((a, i) => a.addEventListener('click', e => {
        e.preventDefault();
        items = links; opener = a; show(i); lb.showModal();
        const cur = document.querySelector('.cursor'); if (cur) lb.append(cur);
        document.documentElement.style.overflow = 'hidden';
      }));
    });
    lb.querySelector('.lightbox__prev').addEventListener('click', () => show(idx - 1));
    lb.querySelector('.lightbox__next').addEventListener('click', () => show(idx + 1));
    lb.querySelector('.lightbox__close').addEventListener('click', () => lb.close());
    lb.addEventListener('click', e => { if (e.target === lb) lb.close(); });
    lb.addEventListener('close', () => { document.documentElement.style.overflow = '';
      const cur = document.querySelector('.cursor'); if (cur) document.body.append(cur); opener && opener.focus(); });
    lb.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
    let sx = null;
    lb.addEventListener('touchstart', e => { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (sx === null) return;
      const dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    });
  }


  /* ---------- menu (upper right) ---------- */
  const menuBtn = document.querySelector('.menu-btn');
  const menu = document.getElementById('menu');
  if (menuBtn && menu) {
    const lbl = menuBtn.querySelector('.sr');
    const setMenu = open => {
      menuBtn.setAttribute('aria-expanded', String(open));
      lbl.textContent = open ? lbl.dataset.close : lbl.dataset.open;
      document.documentElement.classList.toggle('is-menu-open', open);
      document.documentElement.style.overflow = open ? 'hidden' : '';
      if (open) { menu.hidden = false; requestAnimationFrame(() => menu.classList.add('is-open')); menu.querySelector('a').focus({ preventScroll: true }); }
      else { menu.classList.remove('is-open'); setTimeout(() => { if (!menu.classList.contains('is-open')) menu.hidden = true; }, 700); }
    };
    menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
    menu.addEventListener('click', e => { if (e.target.closest('a[href^="#"]')) setMenu(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menuBtn.getAttribute('aria-expanded') === 'true') { setMenu(false); menuBtn.focus(); } });
  }

  /* ---------- accessibility panel ---------- */
  const A11Y_KEY = 'vs-a11y';
  const root = document.documentElement;
  const prefs = (() => { try { return JSON.parse(localStorage.getItem(A11Y_KEY) || '{}'); } catch { return {}; } })();
  const save = () => { try { localStorage.setItem(A11Y_KEY, JSON.stringify(prefs)); } catch {} };
  const a11yBtn = document.querySelector('.a11y-btn');
  const panel = document.getElementById('a11y-panel');
  const sizeOut = panel && panel.querySelector('.a11y-size__val');
  const TOGGLES = ['motion', 'contrast', 'links', 'spacing', 'cursor'];
  const apply = () => {
    TOGGLES.forEach(k => root.classList.toggle('a11y-' + k, !!prefs[k]));
    root.classList.toggle('a11y-light', !!prefs.light);
    root.style.setProperty('--fs', prefs.size || 1);
    if (!panel) return;
    panel.querySelectorAll('[data-a]').forEach(b => {
      const k = b.dataset.a;
      if (TOGGLES.includes(k)) b.setAttribute('aria-pressed', String(!!prefs[k]));
      if (k === 'light') b.setAttribute('aria-pressed', String(!!prefs.light));
      if (k === 'dark') b.setAttribute('aria-pressed', String(!prefs.light));
    });
    sizeOut.textContent = Math.round((prefs.size || 1) * 100) + '%';
    // motion: pause the hero video too
    if (prefs.motion && video && !video.paused) video.pause();
    // cursor: fall back to the normal pointer
    root.classList.toggle('has-cursor', finePointerA && !prefs.cursor);
  };
  const finePointerA = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (a11yBtn && panel) {
    a11yBtn.addEventListener('click', () => {
      const open = a11yBtn.getAttribute('aria-expanded') !== 'true';
      a11yBtn.setAttribute('aria-expanded', String(open)); panel.hidden = !open;
      if (open) panel.querySelector('button').focus();
    });
    panel.addEventListener('click', e => {
      const b = e.target.closest('[data-a]'); if (!b) return;
      const k = b.dataset.a;
      if (TOGGLES.includes(k)) prefs[k] = !prefs[k];
      else if (k === 'light') prefs.light = true;
      else if (k === 'dark') prefs.light = false;
      else if (k === 'bigger') prefs.size = Math.min(1.6, Math.round(((prefs.size || 1) + .1) * 10) / 10);
      else if (k === 'smaller') prefs.size = Math.max(.8, Math.round(((prefs.size || 1) - .1) * 10) / 10);
      else if (k === 'reset') Object.keys(prefs).forEach(x => delete prefs[x]);
      save(); apply();
    });
    document.addEventListener('click', e => { if (!panel.hidden && !e.target.closest('.a11y')) { panel.hidden = true; a11yBtn.setAttribute('aria-expanded', 'false'); } });
    panel.addEventListener('keydown', e => { if (e.key === 'Escape') { panel.hidden = true; a11yBtn.setAttribute('aria-expanded', 'false'); a11yBtn.focus(); } });
  }

  /* ---------- cursor + manicure ---------- */
  const cursor = document.querySelector('.cursor');
  const hint = document.querySelector('.cursor-hint');
  if (!cursor) return;

  const finePointer = finePointerA;
  const customOn = () => !root.classList.contains('a11y-cursor');
  apply();

  const HOLD = 450;                                // ms before the hand appears (mouse)
  const HOLD_TOUCH = 320;                          // shorter on touch: beat the browser's own long-press (~500 ms)
  const STEP = reduce ? 120 : 280;                 // ms per nail
  const POLISH = ['#e8004f', '#ff4fb0', '#8a5cff', '#120d11', '#d6b04c', '#2fd1c5', '#c9c2d6'];
  // brush tip positions (svg units) for nails 0..4 = pinky, ring, middle, index, thumb
  const NAILS = [[89.3,  42.7],  [72.5,  25.5],  [53.0,  18.7],  [34.1,  27.9],  [10.0,  83.7]];
  const paints = [...cursor.querySelectorAll('.nail-paint')].sort((a, b) => a.dataset.nail - b.dataset.nail);
  const brush = cursor.querySelector('.brush');
  cursor.style.setProperty('--hold', HOLD + 'ms');
  if (!finePointer) cursor.style.setProperty('--hold', HOLD_TOUCH + 'ms');

  let x = innerWidth / 2, y = innerHeight / 2, raf = 0;
  let holdTimer = 0, stepTimers = [], handOn = false, startX = 0, startY = 0, swallowClick = false;
  let colorIdx = Number(store.get('vs-polish')) || 0;

  const place = () => { raf = 0; cursor.style.transform = `translate3d(${x}px, ${y}px, 0)`; };
  const move = (nx, ny) => { x = nx; y = ny; if (!raf) raf = requestAnimationFrame(place); };

  if (finePointer) {
    addEventListener('pointermove', e => {
      if (e.pointerType !== 'mouse') return;
      move(e.clientX, e.clientY);
      cursor.classList.add('is-visible');
      cursor.classList.toggle('is-link', !!e.target.closest('a, button, [tabindex="0"]'));
    }, { passive: true });
    document.addEventListener('mouseleave', () => cursor.classList.remove('is-visible'));
  }

  const brushTo = i => { const [bx, by] = NAILS[i]; brush.style.transform = `translate(${bx}px, ${by}px)`; };

  const startManicure = () => {
    handOn = true;
    const color = POLISH[colorIdx % POLISH.length];
    colorIdx++; store.set('vs-polish', colorIdx);
    cursor.style.setProperty('--polish', color);
    cursor.classList.add('is-hand', 'is-painting');
    brushTo(0);
    paints.forEach((p, i) => {
      stepTimers.push(setTimeout(() => {
        brushTo(i);
        p.classList.add('painted');
        if (navigator.vibrate && cursor.classList.contains('is-touch')) navigator.vibrate(8);
      }, 120 + i * STEP));
    });
    stepTimers.push(setTimeout(() => {
      cursor.classList.remove('is-painting');
      cursor.classList.add('is-done');
    }, 120 + paints.length * STEP));
    if (hint) { hint.classList.remove('is-shown'); store.set('vs-hint', '1'); }
  };

  const beginHold = (cx, cy) => {
    startX = cx; startY = cy; swallowClick = false;
    clearTimeout(holdTimer);
    cursor.classList.remove('is-pressing'); void cursor.offsetWidth; cursor.classList.add('is-pressing');
    document.documentElement.classList.add('is-holding');
    holdTimer = setTimeout(startManicure, cursor.classList.contains('is-touch') ? HOLD_TOUCH : HOLD);
  };

  const reset = () => {
    clearTimeout(holdTimer); stepTimers.forEach(clearTimeout); stepTimers = [];
    cursor.classList.remove('is-pressing', 'is-hand', 'is-painting', 'is-done');
    document.documentElement.classList.remove('is-holding');
    if (handOn) swallowClick = true;
    handOn = false;
    setTimeout(() => { if (!handOn) paints.forEach(p => p.classList.remove('painted')); }, 300);
    if (cursor.classList.contains('is-touch')) setTimeout(() => { if (!handOn) cursor.classList.remove('is-touch'); }, 250);
  };

  // ---- mouse: pointer events ----
  addEventListener('pointerdown', e => {
    if (e.pointerType !== 'mouse' || e.button !== 0) return;   // touch is handled below
    if (!finePointer || !customOn()) return;
    if (e.target.closest('iframe, input, textarea, select, video, .a11y, .lightbox')) return;
    beginHold(e.clientX, e.clientY);
  });
  addEventListener('pointerup', e => { if (e.pointerType === 'mouse') reset(); });
  addEventListener('blur', reset);

  // ---- touch: touch events (iOS fires pointercancel on long press, which would kill the hand) ----
  let touchId = null, autoHide = 0;
  addEventListener('touchstart', e => {
    if (e.touches.length > 1 || !customOn()) { if (touchId !== null) reset(); return; }
    if (e.target.closest('iframe, input, textarea, select, video, .a11y, .lightbox, .menu')) return;
    const t = e.changedTouches[0]; touchId = t.identifier;
    clearTimeout(autoHide);
    cursor.classList.add('is-touch'); move(t.clientX, t.clientY); place();
    beginHold(t.clientX, t.clientY);
  }, { passive: true });
  addEventListener('touchmove', e => {
    const t = [...e.changedTouches].find(x => x.identifier === touchId); if (!t) return;
    if (!handOn && Math.hypot(t.clientX - startX, t.clientY - startY) > 12) { touchId = null; reset(); return; }
    if (handOn) { e.preventDefault(); move(t.clientX, t.clientY); }      // keep the page still while painting
  }, { passive: false });
  addEventListener('touchend', e => {
    if ([...e.changedTouches].some(x => x.identifier === touchId)) { touchId = null; reset(); }
  });
  addEventListener('touchcancel', () => {
    touchId = null;
    if (!handOn) return reset();
    // the browser took over the gesture: finish the manicure, then fade out on its own
    autoHide = setTimeout(reset, 120 + paints.length * STEP + 900);
  });

  // a long press shouldn't also "click" the link underneath, nor open the context menu
  addEventListener('click', e => { if (swallowClick) { e.preventDefault(); e.stopPropagation(); swallowClick = false; } }, true);
  addEventListener('contextmenu', e => { if (handOn || cursor.classList.contains('is-pressing')) e.preventDefault(); });

  // first-visit hint
  if (hint && !store.get('vs-hint')) {
    setTimeout(() => hint.classList.add('is-shown'), 2500);
    setTimeout(() => hint.classList.remove('is-shown'), 9000);
  }
})();
