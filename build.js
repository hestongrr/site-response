// Builds two pages from one physics source:
//
//   dist/index.html          standalone, offline, zero dependencies -- for anyone
//   dist/site-response.html  same tool in thebigpicture.tech chrome
//
// No toolchain. The standalone output must work from a USB stick, opened by
// double-click, on a machine that has never seen the internet.
//
// src/ is the single source of truth for the physics. Both outputs are VERIFIED
// against the tested modules before they are written, so neither page can
// silently drift from the code the test suite covers.

import { readFileSync, writeFileSync, existsSync } from 'node:fs';

const read = (p) => readFileSync(p, 'utf8');
const MODULES = ['src/complex.js', 'src/transfer.js'];

// Our modules use only top-level `import ... from` and `export const` /
// `export function`, so flattening them to plain script is mechanical.
const flatten = (src) =>
  src.split('\n').filter((l) => !/^\s*import\s/.test(l)).join('\n')
     .replace(/^export\s+(const|function)\s/gm, '$1 ');

const physics = MODULES.map((m) => `// ===== ${m} =====\n${flatten(read(m))}`).join('\n\n');

const parts = {
  '/*__PHYSICS__*/': physics,
  '/*__APP_JS__*/': read('web/app.js'),
  '/*__APP_CSS__*/': read('web/app.css'),
  '/*__APP_BODY__*/': read('web/app-body.html'),
  '/*__SAFETY__*/': read('web/safety.html'),
}

// The site build depends on Heston's own thebigpicture.tech design, which is
// deliberately NOT part of this repo. Its shell and chrome live outside it, in a
// private directory. When that directory is absent -- which is the case for
// anyone who clones this -- only the standalone page is built.
const PRIVATE_SITE = process.env.SITE_BUILD_DIR
  || `${process.env.HOME}/private/site-response-site-build`;
const hasSiteBuild = existsSync(`${PRIVATE_SITE}/site.html`);
if (hasSiteBuild) {
  parts['/*__CHROME_CSS__*/'] = read(`${PRIVATE_SITE}/site-chrome.css`);
}

const render = (shell) => {
  let out = read(shell);
  for (const [token, value] of Object.entries(parts)) out = out.replace(token, () => value);
  const leftover = out.match(/\/\*__[A-Z_]+__\*\//);
  if (leftover) throw new Error(`unreplaced token ${leftover[0]} in ${shell}`);
  return out;
};

// --- verify the inlined physics reproduces the module physics exactly ---
const mod = await import('./src/transfer.js');
const inlined = new Function(`${physics}\nreturn { sitePeriod, amplification };`)();

let worst = Math.abs(inlined.sitePeriod(22, 240) - mod.sitePeriod(22, 240));
for (const soil of [
  { H: 22, Vs: 240, rho: 1850, xi: 0.04 },
  { H: 90, Vs: 120, rho: 1600, xi: 0.12 },
  { H: 6, Vs: 700, rho: 2100, xi: 0.02 },
]) {
  const rock = { Vs: 800, rho: 2300, xi: 0.01 };
  for (let f = 0.05; f < 25; f += 0.05) {
    const w = 2 * Math.PI * f;
    worst = Math.max(worst, Math.abs(inlined.amplification(w, soil, rock) - mod.amplification(w, soil, rock)));
  }
}
if (!(worst < 1e-12)) {
  console.error(`BUNDLE VERIFICATION FAILED: max deviation ${worst}`);
  process.exit(1);
}

const targets = [['web/standalone.html', 'dist/index.html']];
if (hasSiteBuild) targets.push([`${PRIVATE_SITE}/site.html`, 'dist/site-response.html']);
else console.log('(site build skipped -- private design directory not present)');
for (const [shell, out] of targets) {
  const html = render(shell);
  writeFileSync(out, html);
  console.log(`${out.padEnd(26)} ${(html.length / 1024).toFixed(1)} KB`);
}
console.log(`\nphysics verified against tested modules: max deviation ${worst.toExponential(2)}`);
