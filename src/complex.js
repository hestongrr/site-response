// Minimal complex arithmetic. Complex numbers are plain {re, im} objects.
// Kept explicit rather than clever so the transfer-function code below reads
// like the equations it implements.

export const C = (re, im = 0) => ({ re, im });

export const cAdd = (a, b) => ({ re: a.re + b.re, im: a.im + b.im });

export const cMul = (a, b) => ({
  re: a.re * b.re - a.im * b.im,
  im: a.re * b.im + a.im * b.re,
});

export const cDiv = (a, b) => {
  const d = b.re * b.re + b.im * b.im;
  return { re: (a.re * b.re + a.im * b.im) / d, im: (a.im * b.re - a.re * b.im) / d };
};

export const cAbs = (a) => Math.hypot(a.re, a.im);

// cos(z) and sin(z) for complex z, via the standard identities:
//   cos(x + iy) = cos(x)cosh(y) - i sin(x)sinh(y)
//   sin(x + iy) = sin(x)cosh(y) + i cos(x)sinh(y)
export const cCos = (z) => ({
  re: Math.cos(z.re) * Math.cosh(z.im),
  im: -Math.sin(z.re) * Math.sinh(z.im),
});

export const cSin = (z) => ({
  re: Math.sin(z.re) * Math.cosh(z.im),
  im: Math.cos(z.re) * Math.sinh(z.im),
});
