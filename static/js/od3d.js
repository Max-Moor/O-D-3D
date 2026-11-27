// O&D Impression 3D — interactions (menu, nuage de points 3D, filtres, visionneuse photo, vidéo)
document.documentElement.classList.remove('no-js');

const mb = document.querySelector('.menu-btn');
if (mb) mb.addEventListener('click', () => {
  const o = document.body.classList.toggle('open');
  mb.setAttribute('aria-expanded', o);
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') document.body.classList.remove('open'); });

document.querySelectorAll('[data-year]').forEach(e => e.textContent = new Date().getFullYear());

// Nuages de points : pièces "numérisées" en 3D, rotation auto + rotation à la souris / au doigt
const SHAPES = {
  flange() { const P = [], R1 = 1, R0 = .42, H = .34;
    for (let i = 0; i < 2600; i++) { const a = Math.random() * 6.283, r = R0 + Math.random() * (R1 - R0);
      if ([...Array(6)].some((_, k) => { const ha = k * Math.PI / 3; return Math.hypot(Math.cos(a) * r - Math.cos(ha) * .72, Math.sin(a) * r - Math.sin(ha) * .72) < .11; })) continue;
      P.push([Math.cos(a) * r, (Math.random() < .5 ? 1 : -1) * H * .25, Math.sin(a) * r]); }
    for (let i = 0; i < 900; i++) { const a = Math.random() * 6.283; P.push([Math.cos(a) * R1, (Math.random() - .5) * H * .5, Math.sin(a) * R1]); }
    for (let i = 0; i < 1200; i++) { const a = Math.random() * 6.283; P.push([Math.cos(a) * R0, -Math.random() * H * 1.6, Math.sin(a) * R0]); }
    for (let i = 0; i < 500; i++) { const a = Math.random() * 6.283, r = .25 + Math.random() * .17; P.push([Math.cos(a) * r, -H * 1.6, Math.sin(a) * r]); }
    return P; },
  gear() { const P = [], N = 18, Ri = .72, Ro = .95, Rh = .26, T = .14;
    const prof = a => { const u = ((a / 6.2832 * N) % 1 + 1) % 1; return u < .18 || u > .82 ? Ri : (u > .32 && u < .68 ? Ro : Ri + (Ro - Ri) * (u < .5 ? (u - .18) / .14 : (.82 - u) / .14)); };
    for (let i = 0; i < 3400; i++) { const a = Math.random() * 6.283, rm = prof(a), r = Rh + Math.sqrt(Math.random()) * (rm - Rh);
      if (r > .4 && r < .6 && [...Array(5)].some((_, k) => { const ha = k * 1.2566; return Math.hypot(Math.cos(a) * r - Math.cos(ha) * .5, Math.sin(a) * r - Math.sin(ha) * .5) < .09; })) continue;
      P.push([Math.cos(a) * r, (Math.random() < .5 ? 1 : -1) * T, Math.sin(a) * r]); }
    for (let i = 0; i < 1800; i++) { const a = Math.random() * 6.283, r = prof(a); P.push([Math.cos(a) * r, (Math.random() - .5) * 2 * T, Math.sin(a) * r]); }
    for (let i = 0; i < 500; i++) { const a = Math.random() * 6.283; P.push([Math.cos(a) * Rh, (Math.random() - .5) * 2 * T, Math.sin(a) * Rh]); }
    return P; },
  impeller() { const P = [], B = 8;
    for (let i = 0; i < 1100; i++) { const h = Math.random(), r = .34 - h * .22, a = Math.random() * 6.283; P.push([Math.cos(a) * r, .6 - h * 1.25, Math.sin(a) * r]); }
    for (let i = 0; i < 700; i++) { const a = Math.random() * 6.283, r = .9; P.push([Math.cos(a) * r, .6, Math.sin(a) * r]); }
    for (let i = 0; i < 500; i++) { const a = Math.random() * 6.283, r = Math.sqrt(Math.random()) * .9; P.push([Math.cos(a) * r, .62, Math.sin(a) * r]); }
    for (let b = 0; b < B; b++) for (let i = 0; i < 520; i++) { const h = Math.random(), s = Math.random(), rh = .34 - h * .22, rmax = .9 - h * .62, r = rh + s * (rmax - rh);
      const a = b * 6.283 / B + h * 1.3 + s * s * .9; P.push([Math.cos(a) * r, .6 - h * 1.25, Math.sin(a) * r]); }
    for (let b = 0; b < B; b++) for (let i = 0; i < 160; i++) { const h = Math.random(), rmax = .9 - h * .62, a = b * 6.283 / B + h * 1.3 + .9; P.push([Math.cos(a) * rmax, .6 - h * 1.25, Math.sin(a) * rmax]); }
    return P; },
  lattice() { const P = [], N = 3, L = .56, c = 2 * L / N, seg = (p, q, n) => { for (let i = 0; i < n; i++) { const t = Math.random(), j = .008; P.push([p[0] + (q[0] - p[0]) * t + (Math.random() - .5) * j, p[1] + (q[1] - p[1]) * t + (Math.random() - .5) * j, p[2] + (q[2] - p[2]) * t + (Math.random() - .5) * j]); } };
    for (let i = 0; i < N; i++) for (let k = 0; k < N; k++) for (let m = 0; m < N; m++) {
      const o = [-L + i * c, -L + k * c, -L + m * c], ctr = [o[0] + c / 2, o[1] + c / 2, o[2] + c / 2];
      for (let dx = 0; dx < 2; dx++) for (let dy = 0; dy < 2; dy++) for (let dz = 0; dz < 2; dz++) seg(ctr, [o[0] + dx * c, o[1] + dy * c, o[2] + dz * c], 35);
    }
    for (let a = 0; a <= N; a++) for (let b2 = 0; b2 <= N; b2++) { const u = -L + a * c, v = -L + b2 * c; seg([u, v, -L], [u, v, L], 45); seg([u, -L, v], [u, L, v], 45); seg([-L, u, v], [L, u, v], 45); }
    return P; },
  bracket() { const P = [], hole = (u, v, cu, cv, r) => Math.hypot(u - cu, v - cv) < r;
    for (let i = 0; i < 2600; i++) { const u = Math.random() * 1.6 - .8, v = Math.random() * 1 - .5; if (hole(u, v, -.45, 0, .12) || hole(u, v, .2, 0, .12)) continue; P.push([u, -.5 + (Math.random() < .5 ? 0 : .12), v]); }
    for (let i = 0; i < 2200; i++) { const u = Math.random() * 1.1, v = Math.random() * 1 - .5; if (hole(u, v, .65, 0, .13)) continue; P.push([.8 - (Math.random() < .5 ? 0 : .12), -.5 + u, v]); }
    for (let i = 0; i < 900; i++) { const t = Math.random(), s = Math.random() * t; P.push([.68 - t * .5, -.38 + s * .5, (Math.random() < .5 ? -.06 : .06)]); }
    for (let i = 0; i < 700; i++) { const u = Math.random() * 1.6 - .8; P.push([u, -.5 + Math.random() * .12, Math.random() < .5 ? -.5 : .5]); }
    return P; },
  ring() { const P = [], R = .58, r = .09;
    for (let i = 0; i < 3000; i++) { const a = Math.random() * 6.283, b = Math.random() * 6.283; P.push([(R + r * Math.cos(b)) * Math.cos(a), (R + r * Math.cos(b)) * Math.sin(a) + .18, r * Math.sin(b) * 1.8]); }
    for (let i = 0; i < 1500; i++) { const u = Math.random() * 6.283, v = Math.acos(2 * Math.random() - 1), rs = .2; P.push([rs * Math.sin(v) * Math.cos(u), -.68 + rs * Math.cos(v) * .75, rs * Math.sin(v) * Math.sin(u)]); }
    for (let k = 0; k < 6; k++) for (let i = 0; i < 140; i++) { const a = k * 1.047 + .52, h = Math.random(); P.push([Math.cos(a) * (.13 + h * .09), -.42 - h * .3, Math.sin(a) * (.13 + h * .09)]); }
    return P; }
};
function hexA(h, a) { const n = parseInt(h.slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; }
document.querySelectorAll('canvas[data-shape]').forEach(cv => {
  const ctx = cv.getContext('2d'), pts = (SHAPES[cv.dataset.shape] || SHAPES.flange)(), dc = cv.dataset.color;
  const getCol = () => (!dc || dc === 'ink') ? (getComputedStyle(cv).getPropertyValue('--pt').trim() || '#BFEFFA') : dc;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let t = Math.random() * 10, W, Hh, dpr, ry = 0, rx = -.95, vy = .0064, drag = null, live = false, raf = 0;
  const tilt = cv.dataset.tilt ? +cv.dataset.tilt : -.95; rx = tilt;
  const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; Hh = cv.clientHeight; cv.width = W * dpr; cv.height = Hh * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  size(); addEventListener('resize', () => { size(); frame(); });
  cv.style.touchAction = 'pan-y'; cv.style.cursor = 'grab';
  cv.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, ry, rx }; cv.setPointerCapture(e.pointerId); cv.style.cursor = 'grabbing'; });
  cv.addEventListener('pointermove', e => { if (!drag) return; const nry = drag.ry + (e.clientX - drag.x) * .012; vy = (nry - ry) * .6; ry = nry; rx = Math.max(-1.5, Math.min(.4, drag.rx + (e.clientY - drag.y) * .008)); if (!live) frame(); });
  const up = () => { drag = null; cv.style.cursor = 'grab'; };
  cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
  function frame() {
    t += .004;
    if (!drag && !reduce) { vy += (.0064 - vy) * .02; ry += vy; rx += (tilt + Math.sin(t * .7) * .1 - rx) * .02; }
    ctx.clearRect(0, 0, W, Hh);
    const s = Math.min(W, Hh) * .34, cx = W / 2, cy = Hh / 2, cyr = Math.cos(ry), syr = Math.sin(ry), cxr = Math.cos(rx), sxr = Math.sin(rx);
    for (const p of pts) {
      let x = p[0] * cyr - p[2] * syr, z = p[0] * syr + p[2] * cyr, y = p[1];
      const y2 = y * cxr - z * sxr; z = y * sxr + z * cxr;
      const f = 2.6 / (2.6 + z), X = cx + x * s * f, Y = cy + y2 * s * f;
      ctx.fillStyle = hexA(getCol(), (.22 + (1 - (z + 1) / 2) * .7).toFixed(2));
      const r = 1.2 * f; ctx.fillRect(X, Y, r, r);
    }
    if (live && !reduce) raf = requestAnimationFrame(frame);
  }
  new IntersectionObserver(es => es.forEach(e => { live = e.isIntersecting; cancelAnimationFrame(raf); if (live) frame(); }), { rootMargin: '100px' }).observe(cv);
  frame();
});

// Ruche : zoom sur le logo survolé
const hexes = [...document.querySelectorAll('.hex')];
hexes.forEach(h => {
  h.addEventListener('mouseenter', () => { h.classList.add('on'); hexes.forEach(o => o !== h && o.classList.add('dim')); });
  h.addEventListener('mouseleave', () => hexes.forEach(o => o.classList.remove('on', 'dim')));
});

// Visionneuse photo
document.querySelectorAll('.gal-i').forEach(a => a.addEventListener('click', e => {
  e.preventDefault();
  const lb = document.createElement('div'); lb.className = 'lb';
  lb.innerHTML = '<img alt="" src="' + a.dataset.full + '">';
  lb.addEventListener('click', () => lb.remove());
  document.addEventListener('keydown', function k(ev) { if (ev.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', k); } });
  document.body.appendChild(lb);
}));

// Matériaux (accueil) : filtre par technologie
(function () {
  const root = document.getElementById('mring'); if (!root) return;
  const groups = [...root.querySelectorAll('.mgroup')];
  root.querySelectorAll('.mr-filters button').forEach(b => b.addEventListener('click', () => {
    root.querySelectorAll('.mr-filters button').forEach(x => x.classList.toggle('on', x === b));
    groups.forEach(g => { g.hidden = b.dataset.f !== 'all' && g.dataset.t !== b.dataset.f; });
  }));
})();

// Grilles équilibrées : 4 éléments → 2 + 2, 6 → 3 + 3, 5 → 3 + 2…
document.querySelectorAll('.grid.g3, .grid.g4').forEach(g => {
  const n = g.children.length, c = g.classList.contains('g4') ? 4 : 3;
  if (n <= c) return;
  const rows = Math.ceil(n / c), cols = Math.ceil(n / rows);
  if (cols !== c) { g.dataset.cols = cols; g.style.setProperty('--cols', cols); }
});

// Vidéo de l'atelier (fond de l'accueil) : lecture auto en sourdine, pause / son
(function () {
  const v = document.getElementById('atelierVid'); if (!v) return;
  const f = v.closest('[data-vid]') || v.parentElement, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let userPaused = reduce;
  if (reduce) { v.removeAttribute('autoplay'); v.pause(); }
  const sync = () => f.classList.toggle('paused', v.paused);
  v.addEventListener('play', sync); v.addEventListener('pause', sync); sync();
  new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && !userPaused) v.play().catch(() => {}); else if (!e.isIntersecting) v.pause(); }), { threshold: .2 }).observe(v);
  const pb = f.querySelector('[data-act="play"]'), sb = f.querySelector('[data-act="sound"]');
  if (pb) pb.addEventListener('click', () => { if (v.paused) { userPaused = false; v.play(); } else { userPaused = true; v.pause(); } });
  if (sb) sb.addEventListener('click', () => { v.muted = !v.muted; f.classList.toggle('sound', !v.muted); if (!v.muted && v.paused) { userPaused = false; v.play(); } });
})();

