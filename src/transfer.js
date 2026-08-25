// 1D linear-viscoelastic site response: one soil layer over an elastic halfspace.
//
// THE PHYSICS, BUILT UP
// ---------------------
// A shear (SH) wave travels straight up through the soil layer, hits the free
// surface, and reflects back down. At the soil/rock boundary part of it
// transmits back into the rock and part reflects up again. The surface motion
// is the sum of every one of those passes. When the arrivals line up in phase,
// they add -- that is resonance, and it is the whole reason soft ground is
// dangerous.
//
// One round trip through a layer of thickness H at shear wave velocity Vs is
// two passes down and two passes up = 4H of travel, so the site rings with a
// natural period of
//
//     T_site = 4H / Vs                                              ... (1)
//
// Two properties control how much amplification you actually get:
//
//   1. IMPEDANCE CONTRAST. Impedance is density x velocity, rho*Vs -- how hard
//      it is to shake a material. The ratio between soil and rock,
//
//          alpha = (rho_soil * Vs_soil) / (rho_rock * Vs_rock)      ... (2)
//
//      is small when soft soil sits on stiff rock (a typical basin might be
//      alpha ~ 0.2). Small alpha means energy that comes up into the soil has
//      trouble getting back out -- it gets trapped and rattles around.
//
//   2. DAMPING. Real soil bleeds energy to heat as it strains. Damping ratio
//      xi (a few percent for small strains) is what keeps the amplification
//      finite instead of infinite.
//
// Damping enters as a COMPLEX shear wave velocity, which is just a compact way
// of saying "the wave loses a little amplitude for every wavelength it
// travels":
//
//     Vs* = Vs * (1 + i*xi)                                         ... (3)
//
// With that, the transfer function between motion at the SOIL SURFACE and
// motion at a ROCK OUTCROP (i.e. what a seismometer sitting on nearby exposed
// rock would record) is
//
//                            1
//     F(w) = --------------------------------------                ... (4)
//             cos(k* H) + i * alpha* * sin(k* H)
//
// where k* = w / Vs* is the complex wavenumber and alpha* is (2) built from
// complex velocities. Reference: Kramer, Geotechnical Earthquake Engineering
// (1996), Ch. 7 -- teaching source, NOT an NCEES-supplied exam reference.
//
// Three checks fall straight out of (4), and the test suite asserts all three:
//   - w -> 0        : cos -> 1, sin -> 0, so F -> 1. Very long waves do not
//                     notice the layer at all. Amplification of exactly 1.
//   - rigid rock    : Vs_rock -> infinity so alpha -> 0, leaving F = 1/cos(wH/Vs),
//                     which blows up at the resonant frequencies. Undamped rock
//                     gives back nothing, so the soil rings forever.
//   - at resonance  : cos(k H) = 0, so F = 1 / (i*alpha), giving a peak
//                     amplification of exactly 1/alpha for the undamped case.

import { C, cAdd, cMul, cDiv, cAbs, cCos, cSin } from './complex.js';

/**
 * Natural period of a uniform soil column -- equation (1) above.
 * @param {number} H thickness of the soil layer, m
 * @param {number} Vs shear wave velocity of the soil, m/s
 * @returns {number} period, seconds
 */
export function sitePeriod(H, Vs) {
  return (4 * H) / Vs;
}

/**
 * Complex transfer function, soil surface / rock outcrop -- equation (4).
 *
 * @param {number} omega circular frequency, rad/s
 * @param {object} soil  {H, Vs, rho, xi}  m, m/s, kg/m^3, ratio (0.05 = 5%)
 * @param {object} rock  {Vs, rho, xi}     Vs may be Infinity for rigid rock
 * @returns {{re:number, im:number}}
 */
export function transferFunction(omega, soil, rock) {
  // Complex velocities -- equation (3). Damping makes them complex.
  const VsSoil = C(soil.Vs, soil.Vs * (soil.xi ?? 0));

  // Complex impedance ratio -- equation (2). Rigid rock is the limiting case
  // rho_rock*Vs_rock -> infinity, which drives alpha to exactly zero.
  let alpha;
  if (!isFinite(rock.Vs) || !isFinite(rock.rho)) {
    alpha = C(0, 0);
  } else {
    const VsRock = C(rock.Vs, rock.Vs * (rock.xi ?? 0));
    alpha = cDiv(cMul(C(soil.rho), VsSoil), cMul(C(rock.rho), VsRock));
  }

  // Complex wavenumber times layer thickness: k* H = omega*H / Vs*
  const kH = cDiv(C(omega * soil.H), VsSoil);

  // Denominator of (4): cos(k*H) + i*alpha*sin(k*H)
  const denom = cAdd(cCos(kH), cMul(cMul(C(0, 1), alpha), cSin(kH)));

  return cDiv(C(1), denom);
}

/**
 * Amplification factor |F(w)| -- the number a non-engineer actually wants.
 * "The surface shakes this many times harder than the rock next door."
 */
export function amplification(omega, soil, rock) {
  return cAbs(transferFunction(omega, soil, rock));
}

/**
 * Sample the amplification spectrum over a frequency band.
 * @returns {{f: number[], amp: number[]}} f in Hz
 */
export function amplificationSpectrum(soil, rock, { fMax = 25, n = 2000 } = {}) {
  const f = [];
  const amp = [];
  for (let i = 0; i < n; i++) {
    const fi = (fMax * i) / (n - 1);
    f.push(fi);
    amp.push(amplification(2 * Math.PI * fi, soil, rock));
  }
  return { f, amp };
}
