const $ = (id) => document.getElementById(id);
const ids = ['vs','h','rho','xi','rvs','rrho'];

function read() {
  const v = {};
  for (const id of ids) v[id] = parseFloat($(id).value);
  return {
    soil: { H: v.h, Vs: v.vs, rho: v.rho, xi: v.xi / 100 },
    rock: { Vs: v.rvs, rho: v.rrho, xi: 0.01 },
  };
}

function peak(soil, rock) {
  // Sweep finely around the fundamental to find the true damped peak, which
  // sits slightly below f0 = Vs/4H rather than exactly on it.
  const f0 = soil.Vs / (4 * soil.H);
  let best = { f: f0, amp: 0 };
  for (let i = 0; i <= 4000; i++) {
    const f = (f0 * 0.4) + (f0 * 1.2 * i) / 4000;
    const a = amplification(2 * Math.PI * f, soil, rock);
    if (a > best.amp) best = { f, amp: a };
  }
  return best;
}

function draw(soil, rock, pk) {
  const cv = $('plot'), ctx = cv.getContext('2d');
  const cs = getComputedStyle(document.body);
  const fg = cs.color;
  const accent = cs.getPropertyValue('--accent').trim() || '#0E6C77';
  const mut = cs.getPropertyValue('--muted').trim() || '#8a949c';
  const W = cv.width, H = cv.height, L = 52, R = 12, T = 14, B = 38;

  ctx.clearRect(0, 0, W, H);

  const Tmax = 3.0;
  const pts = [];
  let aMax = 1;
  for (let i = 1; i <= 600; i++) {
    const per = (Tmax * i) / 600;
    const a = amplification((2 * Math.PI) / per, soil, rock);
    pts.push([per, a]);
    if (a > aMax) aMax = a;
  }
  const yTop = Math.ceil(Math.max(aMax, 2) * 1.15);
  const X = (p) => L + (p / Tmax) * (W - L - R);
  const Y = (a) => H - B - (a / yTop) * (H - T - B);

  // axes + gridlines
  ctx.strokeStyle = mut; ctx.fillStyle = mut; ctx.lineWidth = 1;
  ctx.font = '12px system-ui, sans-serif';
  ctx.globalAlpha = 0.35;
  for (let a = 0; a <= yTop; a += Math.max(1, Math.round(yTop / 5))) {
    ctx.beginPath(); ctx.moveTo(L, Y(a)); ctx.lineTo(W - R, Y(a)); ctx.stroke();
  }
  ctx.globalAlpha = 1;
  for (let a = 0; a <= yTop; a += Math.max(1, Math.round(yTop / 5))) {
    ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
    ctx.fillText(a + '×', L - 8, Y(a));
  }
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  for (let p = 0; p <= Tmax + 1e-9; p += 0.5) ctx.fillText(p.toFixed(1) + ' s', X(p), H - B + 8);
  ctx.fillText('period of shaking  (long, slow shaking to the right)', (L + W - R) / 2, H - 16);

  // "no amplification" reference
  ctx.setLineDash([4, 4]); ctx.globalAlpha = 0.7;
  ctx.beginPath(); ctx.moveTo(L, Y(1)); ctx.lineTo(W - R, Y(1)); ctx.stroke();
  ctx.setLineDash([]); ctx.globalAlpha = 1;

  // the curve
  ctx.strokeStyle = accent;
  ctx.lineWidth = 2; ctx.beginPath();
  pts.forEach(([p, a], i) => (i ? ctx.lineTo(X(p), Y(a)) : ctx.moveTo(X(p), Y(a))));
  ctx.stroke();

  // mark resonance
  const pT = 1 / pk.f;
  if (pT <= Tmax) {
    ctx.strokeStyle = fg; ctx.globalAlpha = 0.45; ctx.setLineDash([2, 3]);
    ctx.beginPath(); ctx.moveTo(X(pT), Y(0)); ctx.lineTo(X(pT), Y(pk.amp)); ctx.stroke();
    ctx.setLineDash([]); ctx.globalAlpha = 1;
    ctx.fillStyle = fg; ctx.textAlign = X(pT) > W * 0.7 ? 'right' : 'left'; ctx.textBaseline = 'bottom';
    ctx.fillText(`  ${pk.amp.toFixed(1)}× at ${pT.toFixed(2)} s  `, X(pT), Y(pk.amp) - 4);
  }
}

function update() {
  const { soil, rock } = read();

  $('vsO').textContent   = soil.Vs + ' m/s';
  $('hO').textContent    = soil.H + ' m';
  $('rhoO').textContent  = soil.rho + ' kg/m³';
  $('xiO').textContent   = (soil.xi * 100).toFixed(1) + ' %';
  $('rvsO').textContent  = rock.Vs + ' m/s';
  $('rrhoO').textContent = rock.rho + ' kg/m³';

  const T = sitePeriod(soil.H, soil.Vs);
  const alpha = (soil.rho * soil.Vs) / (rock.rho * rock.Vs);
  const pk = peak(soil, rock);

  $('rT').textContent = T.toFixed(2) + ' s';
  $('rF').textContent = (1 / T).toFixed(2) + ' Hz';
  $('rA').textContent = alpha.toFixed(3);
  $('rAmp').textContent = pk.amp.toFixed(1) + '×';

  const storeys = Math.round(T / 0.1);
  $('rStory').textContent = storeys < 1
    ? 'low, stiff buildings (1 storey)'
    : `roughly ${Math.max(1, storeys - 1)}–${storeys + 1} storeys`;

  $('work').textContent =
`1. How long does one round trip take?
   A shear wave goes up through the soil, reflects off the ground surface,
   comes back down, and reflects again. That round trip is 4 x H of travel.

     T_site = 4H / Vs
            = 4 x ${soil.H} m / ${soil.Vs} m/s
            = ${(4 * soil.H).toFixed(0)} / ${soil.Vs}
            = ${T.toFixed(3)} s          <- the ground rings at this period

2. How hard is it for energy to escape back down into the rock?
   Impedance is density x velocity: how hard a material is to shake.

     alpha = (rho_soil x Vs_soil) / (rho_rock x Vs_rock)
           = (${soil.rho} x ${soil.Vs}) / (${rock.rho} x ${rock.Vs})
           = ${(soil.rho * soil.Vs).toFixed(0)} / ${(rock.rho * rock.Vs).toFixed(0)}
           = ${alpha.toFixed(3)}

   Small alpha means soft soil on stiff rock. Energy that comes up gets
   trapped and rattles around instead of leaving.

3. What is the most it could amplify?
   With no damping at all, the peak would be exactly 1 / alpha:

     1 / ${alpha.toFixed(3)} = ${(1 / alpha).toFixed(1)}x

   Real soil turns some shaking into heat. At ${(soil.xi * 100).toFixed(1)}% damping the
   real peak comes out at ${pk.amp.toFixed(1)}x, at a period of ${(1 / pk.f).toFixed(2)} s.

4. Check: does that answer make sense?
   The damped peak (${pk.amp.toFixed(1)}x) must be below the undamped ceiling
   (${(1 / alpha).toFixed(1)}x), and it is. It must also sit at or just below
   T_site = ${T.toFixed(2)} s, and it does (${(1 / pk.f).toFixed(2)} s).

5. So who is in trouble?
   A building's own period is very roughly 0.1 s per storey, so ${T.toFixed(2)} s
   is about a ${Math.max(1, storeys)}-storey building. That building and this ground
   want to swing at the same rate. The ground pushes it in time with its
   own sway, over and over, and the sway grows.

   This is what happened in Mexico City in 1985. The earthquake was 350 km
   away. Soft lakebed clay rang at about 2 seconds, mid-rise buildings rang
   at about 2 seconds, and those were the buildings that came down --
   while shorter buildings right beside them stayed up.`;

  draw(soil, rock, pk);
}

for (const id of ids) $(id).addEventListener('input', update);
document.querySelectorAll('.presets button').forEach((b) =>
  b.addEventListener('click', () => {
    const [vs, h, rho, xi] = b.dataset.p.split(',');
    $('vs').value = vs; $('h').value = h; $('rho').value = rho; $('xi').value = xi;
    update();
  })
);
update();
