// Verification against cases that can be worked by hand. If any of these fail,
// nothing downstream is trustworthy.

import assert from 'node:assert/strict';
import { sitePeriod, amplification, amplificationSpectrum } from '../src/transfer.js';

let passed = 0;
const check = (name, fn) => {
  fn();
  passed++;
  console.log(`  PASS  ${name}`);
};

// A representative soft basin profile: 30 m of soft alluvium (Site Class D
// territory) over ordinary bedrock.
const soil = { H: 30, Vs: 180, rho: 1800, xi: 0 };
const rock = { Vs: 760, rho: 2200, xi: 0 };
const rigid = { Vs: Infinity, rho: Infinity, xi: 0 };

console.log('\n1D site response -- analytical verification\n');

check('T_site = 4H/Vs  ->  4(30)/180 = 0.6667 s', () => {
  assert.ok(Math.abs(sitePeriod(30, 180) - 0.66667) < 1e-4);
});

check('omega -> 0 gives amplification of exactly 1', () => {
  // Very long waves do not see the layer. cos->1, sin->0, F->1.
  assert.ok(Math.abs(amplification(1e-9, soil, rock) - 1) < 1e-9);
});

check('rigid rock at resonance -> unbounded amplification', () => {
  // alpha = 0, xi = 0, so F = 1/cos(pi/2) -> infinity. Energy cannot escape
  // downward and nothing dissipates it, so the column rings without limit.
  const w0 = (Math.PI * soil.Vs) / (2 * soil.H); // = 3*pi rad/s
  assert.ok(amplification(w0, soil, rigid) > 1e6);
});

check('elastic halfspace at resonance -> peak = 1/alpha (hand calc 5.161)', () => {
  // alpha = (1800 x 180) / (2200 x 760) = 324000 / 1672000 = 0.19378
  // 1/alpha = 5.1605
  const alpha = (1800 * 180) / (2200 * 760);
  const expected = 1 / alpha;
  const w0 = (Math.PI * soil.Vs) / (2 * soil.H);
  const got = amplification(w0, soil, rock);
  assert.ok(Math.abs(got - expected) < 1e-9, `expected ${expected}, got ${got}`);
  assert.ok(Math.abs(expected - 5.1605) < 1e-3);
});

check('damped peak sits just below f0, and converges to it as xi -> 0', () => {
  // With damping the resonant peak shifts slightly DOWN from f0 = Vs/4H.
  // That is real behaviour, not error -- so the meaningful check is that it
  // converges to the undamped answer (1.5 Hz, amplitude 1/alpha = 5.1605) as
  // damping is removed.
  const peakAt = (xi) => {
    const { f, amp } = amplificationSpectrum({ ...soil, xi }, rock, { fMax: 4, n: 200001 });
    let i = 0;
    for (let k = 1; k < amp.length; k++) if (amp[k] > amp[i]) i = k;
    return { f: f[i], amp: amp[i] };
  };

  const f0 = soil.Vs / (4 * soil.H); // 1.5 Hz
  const limit = 1 / ((1800 * 180) / (2200 * 760)); // 5.1605

  const heavy = peakAt(0.05);
  const light = peakAt(0.001);

  // Peak is below f0, and less so as damping drops.
  assert.ok(heavy.f < f0 && light.f < f0);
  assert.ok(light.f > heavy.f);
  assert.ok(Math.abs(light.f - f0) < 0.001, `light-damping peak ${light.f} should approach ${f0}`);

  // Amplitude approaches the undamped 1/alpha ceiling from below.
  assert.ok(heavy.amp < light.amp && light.amp < limit);
  assert.ok(Math.abs(light.amp - limit) < 0.05, `${light.amp} should approach ${limit}`);
});

check('damping reduces the peak below the undamped 1/alpha limit', () => {
  const w0 = (Math.PI * soil.Vs) / (2 * soil.H);
  const undamped = amplification(w0, soil, rock);
  const damped = amplification(w0, { ...soil, xi: 0.05 }, { ...rock, xi: 0.02 });
  assert.ok(damped < undamped);
  assert.ok(damped > 1);
});

check('stiff soil on similar rock barely amplifies', () => {
  // Vs 700 soil on Vs 760 rock: alpha near 1, so almost nothing is trapped.
  const stiff = { H: 30, Vs: 700, rho: 2100, xi: 0.02 };
  const w0 = (Math.PI * stiff.Vs) / (2 * stiff.H);
  assert.ok(amplification(w0, stiff, rock) < 1.5);
});

console.log(`\n${passed} checks passed\n`);
