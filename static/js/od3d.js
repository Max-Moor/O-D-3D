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

// Nuage de points : une pièce mécanique (bride percée) numérisée en rotation
const cv = document.getElementById('cloud');
if (cv) {
  const ctx = cv.getContext('2d');
  const pts = [];
  const R1 = 1, R0 = .42, H = .34;
  // bride : disque percé + moyeu + 6 trous
  for (let i = 0; i < 2600; i++) {
    const a = Math.random() * Math.PI * 2, r = R0 + Math.random() * (R1 - R0);
    const holes = [...Array(6)].some((_, k) => {
      const ha = k * Math.PI / 3, hx = Math.cos(ha) * .72, hy = Math.sin(ha) * .72;
      return Math.hypot(Math.cos(a) * r - hx, Math.sin(a) * r - hy) < .11;
    });
    if (holes) continue;
    const top = Math.random() < .5;
    pts.push([Math.cos(a) * r, (top ? 1 : -1) * H * .25, Math.sin(a) * r]);
  }
  for (let i = 0; i < 900; i++) { const a = Math.random() * 6.283, y = (Math.random() - .5) * H * .5; pts.push([Math.cos(a) * R1, y, Math.sin(a) * R1]); }
  for (let i = 0; i < 1200; i++) { const a = Math.random() * 6.283, y = Math.random() * H * 1.6; pts.push([Math.cos(a) * R0, -y, Math.sin(a) * R0]); }
  for (let i = 0; i < 500; i++) { const a = Math.random() * 6.283, r = .25 + Math.random() * .17; pts.push([Math.cos(a) * r, -H * 1.6, Math.sin(a) * r]); }
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let t = 0, W, Hh, dpr;
  const size = () => { dpr = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; Hh = cv.clientHeight; cv.width = W * dpr; cv.height = Hh * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  size(); addEventListener('resize', size);
  const angEl = document.getElementById('ang'), ptsEl = document.getElementById('npts');
  if (ptsEl) ptsEl.textContent = pts.length.toLocaleString('fr-BE');
  const draw = () => {
    t += reduce ? 0 : .004;
    ctx.clearRect(0, 0, W, Hh);
    const ry = t * 1.6, rx = -.95 + Math.sin(t * .7) * .1, s = Math.min(W, Hh) * .34, cx = W / 2, cy = Hh / 2;
    const cyr = Math.cos(ry), syr = Math.sin(ry), cxr = Math.cos(rx), sxr = Math.sin(rx);
    const scanY = Math.sin(t * 2.2) * .7;
    for (const p of pts) {
      let x = p[0] * cyr - p[2] * syr, z = p[0] * syr + p[2] * cyr, y = p[1];
      const y2 = y * cxr - z * sxr; z = y * sxr + z * cxr;
      const f = 2.6 / (2.6 + z), X = cx + x * s * f, Y = cy + y2 * s * f;
      const near = Math.abs(y2 - scanY) < .03;
      const a = .25 + (1 - (z + 1) / 2) * .6;
      ctx.fillStyle = near ? 'rgba(255,255,255,.95)' : `rgba(0,193,234,${a.toFixed(2)})`;
      const r = near ? 1.6 : 1.1 * f;
      ctx.fillRect(X, Y, r, r);
    }
    // ligne de scan
    const sy = cy + scanY * s;
    const g = ctx.createLinearGradient(0, sy - 18, 0, sy + 18);
    g.addColorStop(0, 'rgba(0,193,234,0)'); g.addColorStop(.5, 'rgba(0,193,234,.18)'); g.addColorStop(1, 'rgba(0,193,234,0)');
    ctx.fillStyle = g; ctx.fillRect(cx - s * 1.25, sy - 18, s * 2.5, 36);
    ctx.fillStyle = 'rgba(125,235,255,.8)'; ctx.fillRect(cx - s * 1.25, sy, s * 2.5, 1);
    if (angEl) angEl.textContent = ((ry * 57.3) % 360).toFixed(1).padStart(5, '0') + '°';
    if (!reduce) requestAnimationFrame(draw);
  };
  draw();
}

// Ruche : zoom sur le logo survolé
const hexes = [...document.querySelectorAll('.hex')];
hexes.forEach(h => {
  h.addEventListener('mouseenter', () => { h.classList.add('on'); hexes.forEach(o => o !== h && o.classList.add('dim')); });
  h.addEventListener('mouseleave', () => hexes.forEach(o => o.classList.remove('on', 'dim')));
});
