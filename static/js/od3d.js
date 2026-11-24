// O&D Impression 3D — interactions (menu, apparitions, halo souris, nuage de points 3D)
document.documentElement.classList.remove('no-js');

const mb = document.querySelector('.menu-btn');
if (mb) mb.addEventListener('click', () => {
  const o = document.body.classList.toggle('open');
  mb.setAttribute('aria-expanded', o);
});
document.addEventListener('keydown', e => { if (e.key === 'Escape') document.body.classList.remove('open'); });

const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
}), { threshold: .1 }) : null;
document.querySelectorAll('.rv').forEach(el => io ? io.observe(el) : el.classList.add('in'));

document.querySelectorAll('.spot').forEach(el => el.addEventListener('pointermove', e => {
  const r = el.getBoundingClientRect();
  el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
  el.style.setProperty('--my', (e.clientY - r.top) + 'px');
}));

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
  const ctx = cv.getContext('2d'), pts = (SHAPES[cv.dataset.shape] || SHAPES.flange)(), col = cv.dataset.color || '#00C1EA';
  const host = cv.closest('.scan') || cv.parentElement, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const angEl = host.querySelector('[data-ang]'), ptsEl = host.querySelector('[data-npts]');
  if (ptsEl) ptsEl.textContent = pts.length.toLocaleString('fr-BE');
  let t = Math.random() * 10, W, Hh, dpr, ry = 0, rx = -.95, vy = .0064, drag = null, live = false, raf = 0;
  const tilt = cv.dataset.tilt ? +cv.dataset.tilt : -.95; rx = tilt;
  const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; Hh = cv.clientHeight; cv.width = W * dpr; cv.height = Hh * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  size(); addEventListener('resize', size);
  cv.style.touchAction = 'pan-y'; cv.style.cursor = 'grab';
  cv.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, ry, rx }; cv.setPointerCapture(e.pointerId); cv.style.cursor = 'grabbing'; });
  cv.addEventListener('pointermove', e => { if (!drag) return; const nry = drag.ry + (e.clientX - drag.x) * .012; vy = (nry - ry) * .6; ry = nry; rx = Math.max(-1.5, Math.min(.4, drag.rx + (e.clientY - drag.y) * .008)); if (!live) frame(); });
  const up = () => { drag = null; cv.style.cursor = 'grab'; };
  cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
  function frame() {
    t += .004;
    if (!drag && !reduce) { vy += (.0064 - vy) * .02; ry += vy; rx += (tilt + Math.sin(t * .7) * .1 - rx) * .02; }
    ctx.clearRect(0, 0, W, Hh);
    const s = Math.min(W, Hh) * .34, cx = W / 2, cy = Hh / 2, cyr = Math.cos(ry), syr = Math.sin(ry), cxr = Math.cos(rx), sxr = Math.sin(rx), scanY = Math.sin(t * 2.2) * .7;
    for (const p of pts) {
      let x = p[0] * cyr - p[2] * syr, z = p[0] * syr + p[2] * cyr, y = p[1];
      const y2 = y * cxr - z * sxr; z = y * sxr + z * cxr;
      const f = 2.6 / (2.6 + z), X = cx + x * s * f, Y = cy + y2 * s * f, near = Math.abs(y2 - scanY) < .03;
      ctx.fillStyle = near ? 'rgba(255,255,255,.95)' : hexA(col, (.25 + (1 - (z + 1) / 2) * .6).toFixed(2));
      const r = near ? 1.6 : 1.1 * f; ctx.fillRect(X, Y, r, r);
    }
    const sy = cy + scanY * s, g = ctx.createLinearGradient(0, sy - 18, 0, sy + 18);
    g.addColorStop(0, hexA(col, 0)); g.addColorStop(.5, hexA(col, .18)); g.addColorStop(1, hexA(col, 0));
    ctx.fillStyle = g; ctx.fillRect(cx - s * 1.25, sy - 18, s * 2.5, 36); ctx.fillStyle = hexA(col, .8); ctx.fillRect(cx - s * 1.25, sy, s * 2.5, 1);
    if (angEl) angEl.textContent = ((((ry * 57.3) % 360) + 360) % 360).toFixed(1).padStart(5, '0') + '°';
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

// Anneau 3D des matières (page d'accueil) : glisser, flèches, filtres
(function () {
  const root = document.getElementById('mring'); if (!root) return;
  const stage = root.querySelector('.mr-stage'), rot = root.querySelector('.mr-rot'), all = [...rot.querySelectorAll('.rcard')];
  const nameEl = document.getElementById('mrName'), tagEl = document.getElementById('mrTag'), goEl = document.getElementById('mrGo');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cards = all, R = 600, step = 30, th = 0, v = 0, target = null, drag = null, moved = 0, hover = false, tiltX = -12, tiltT = -12, live = false, front = null;
  function layout() {
    const cw = all[0] ? all[0].offsetWidth : 170;
    step = 360 / cards.length; R = Math.max(cw * 2.2, cards.length * cw * 1.12 / (2 * Math.PI));
    all.forEach(c => c.style.display = cards.includes(c) ? '' : 'none');
    cards.forEach((c, i) => { c.dataset.a = i * step; });
  }
  function render() {
    rot.style.transform = `translateZ(${-R}px) rotateX(${tiltX}deg) rotateY(${th}deg)`;
    let best = -2;
    cards.forEach(c => {
      const a = (+c.dataset.a + th) * Math.PI / 180, k = Math.cos(a), o = .12 + .88 * Math.pow((k + 1) / 2, 1.6);
      c.style.transform = `rotateY(${c.dataset.a}deg) translateZ(${R}px)`;
      c.style.opacity = o.toFixed(3); c.style.pointerEvents = k > .2 ? 'auto' : 'none'; c.style.zIndex = Math.round(k * 100) + 100;
      if (k > best) { best = k; front = c; }
    });
    all.forEach(c => c.classList.toggle('front', c === front));
    if (front && nameEl) { nameEl.textContent = front.querySelector('b').textContent; tagEl.textContent = front.querySelector('.rc-t').textContent + ' · ' + front.querySelector('.rc-g').textContent; goEl.href = front.getAttribute('href'); }
  }
  let last = 0;
  function frame(now) {
    now = now || performance.now(); const dt = last ? Math.min((now - last) / 1000, .05) : 0; last = now;
    if (target !== null) { const d = target - th; th += d * .12; if (Math.abs(d) < .05) { th = target; target = null; } }
    else if (!drag) { th += v; v *= .94; if (!hover && !reduce && Math.abs(v) < .02) th -= 10 * dt; }
    tiltX += (tiltT - tiltX) * .08;
    render(); if (live) requestAnimationFrame(frame);
  }
  const snapTo = dir => { const i = Math.round(-th / step) + dir; target = -i * step; v = 0; };
  stage.addEventListener('pointerdown', e => { root.classList.add('touched'); drag = { x: e.clientX, th }; moved = 0; v = 0; target = null; stage.setPointerCapture(e.pointerId); stage.classList.add('grab'); });
  stage.addEventListener('pointermove', e => {
        if (!drag) return; const dx = e.clientX - drag.x; moved = Math.max(moved, Math.abs(dx)); const nt = drag.th + dx * .22; v = nt - th; th = nt; });
  const up = () => { if (drag) { drag = null; stage.classList.remove('grab'); if (Math.abs(v) < .3) snapTo(0); } };
  stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);
  all.forEach(c => { c.addEventListener('pointerenter', () => hover = true); c.addEventListener('pointerleave', () => hover = false); });
  stage.addEventListener('pointerleave', () => { hover = false; });
  stage.addEventListener('click', e => { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
  stage.addEventListener('wheel', e => { if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); v = 0; target = null; th -= e.deltaX * .15; } }, { passive: false });
  stage.tabIndex = 0;
  stage.addEventListener('keydown', e => { if (e.key === 'ArrowLeft') { snapTo(-1); e.preventDefault(); } if (e.key === 'ArrowRight') { snapTo(1); e.preventDefault(); } });
  root.querySelectorAll('[data-nav]').forEach(b => b.addEventListener('click', () => snapTo(+b.dataset.nav)));
  root.querySelectorAll('.mr-filters button').forEach(b => b.addEventListener('click', () => {
    root.querySelectorAll('.mr-filters button').forEach(x => x.classList.toggle('on', x === b));
    cards = b.dataset.f === 'all' ? all : all.filter(c => c.dataset.t === b.dataset.f);
    layout(); th = 0; target = null; v = 6;
  }));
  addEventListener('resize', layout);
  layout(); render();
  new IntersectionObserver(es => es.forEach(e => { const was = live; live = e.isIntersecting; if (live && !was) { last = 0; frame(); } })).observe(stage);
})();

// Grilles équilibrées : 4 éléments → 2 + 2, 6 → 3 + 3, 5 → 3 + 2…
document.querySelectorAll('.grid.g3, .grid.g4').forEach(g => {
  const n = g.children.length, c = g.classList.contains('g4') ? 4 : 3;
  if (n <= c) return;
  const rows = Math.ceil(n / c), cols = Math.ceil(n / rows);
  if (cols !== c) { g.dataset.cols = cols; g.style.setProperty('--cols', cols); }
});

// En-têtes de section : la ligne se trace quand la section arrive à l'écran
(function () {
  const ss = document.querySelectorAll('section');
  if (!('IntersectionObserver' in window)) { ss.forEach(s => s.classList.add('seen')); return; }
  const o = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('seen'); o.unobserve(e.target); } }), { threshold: .15 });
  ss.forEach(s => o.observe(s));
})();
