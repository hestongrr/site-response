# site-response

Why soft ground shakes harder than rock — worked out from first principles,
verified against hand calculations, and free to use or fork.

**Status: working. Not usable for design.**

Open `dist/index.html` in any browser. One file, 19 KB, no dependencies, no
internet connection required, no install. Put it on a USB stick and it works on
a machine that has never been online.

## Why this exists

If you are an engineer in the United States, everything here is a ten-minute
lookup. If you are anywhere else — and especially in the poor, seismically
active, hard-to-reach places where earthquakes actually kill people — it is
effectively unavailable. That asymmetry is the entire reason for this repo.

Nevada, where this was written, is the **third most seismically active state in
the United States** — behind only Alaska and California, with a magnitude 6 about
every ten years. Almost nobody who lives here knows that. The recurrence
intervals are longer than an attention span.

Earthquakes do not kill people at any meaningful rate. Collapsing buildings do.
The knowledge that prevents those collapses has been settled for fifty years; it
just never reaches the person laying the block.

## What is here now

Two things, deliberately in one file:

1. **Why some ground shakes harder than other ground** — interactive, with the
   arithmetic worked out line by line.
2. **General earthquake safety** — what to do when it starts, and the cheap
   preparations that prevent most injuries. Sourced to the Nevada Bureau of
   Mines and Geology, FEMA, and the Earthquake Country Alliance, with links out
   to all of them.

For the offline use case the safety half is the more valuable one. If somebody
has exactly one file on a cheap phone, "strap the water heater and know where
the gas shutoff is" saves more people than a transfer function does.


`dist/index.html` — the whole thing, self-contained. Move the sliders, watch what
soft ground does, and read the arithmetic worked out line by line underneath.

`src/transfer.js` — 1D linear-viscoelastic site response for one soil layer over
an elastic halfspace. The derivation is written out in the file, in full, in
plain language.

The two equations that carry the whole subject:

    T_site = 4H / Vs                          natural period of a soil column
    alpha  = (rho_soil x Vs_soil) / (rho_rock x Vs_rock)     impedance ratio

A 30 m soft alluvium column at Vs = 180 m/s rings at 4(30)/180 = 0.67 s. A
six-to-seven storey building rings at roughly the same period. They are tuned to
each other, and the ground hands the building energy at exactly the rhythm it
wants to swing at. That is Mexico City 1985 in two lines of arithmetic.

## Verification

    npm test        # 7 analytical checks
    node build.js   # rebuild dist/, re-verifying it against the tested modules

Seven checks against cases with known closed-form answers: unit amplification at
zero frequency, unbounded response over rigid undamped rock, peak amplification
of exactly 1/alpha at resonance, convergence of the damped peak to the undamped
limit, and near-unity response when soil and rock have similar stiffness.

`build.js` inlines the modules into the single-file page and then asserts the
inlined copy reproduces the module results to within 1e-12 across the frequency
band, so the shipped page can never drift from the tested physics.

## Scope and limits

- Linear elastic only. No strain-dependent stiffness degradation, no
  liquefaction, no nonlinearity.
- Single uniform layer. Real profiles are layered.
- Vertically propagating SH waves only. No surface waves, no basin edge effects,
  no topographic amplification.

Source for the formulation: Kramer, *Geotechnical Earthquake Engineering* (1996),
Ch. 7. This is a teaching reference, not a code or standard.

## This is not engineering advice

Educational simulation. Not a site-specific geotechnical evaluation, not a
design tool, and not a substitute for a licensed engineer in your jurisdiction.

## License

MIT
