// News-image entry (Node 22, standard library only): the front page is drawn
// by render.py into entry.png beside this file, and this program copies it to
// /output/entry.png. The copy is byte for byte, so two runs are identical.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const png = readFileSync(new URL('./entry.png', import.meta.url));
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, png);
// The gate refuses an empty or truncated file, so fail loudly instead of
// silently handing the grader a broken image.
if (statSync(outPath).size !== png.length) {
  throw new Error(`entry.png write mismatch: ${statSync(outPath).size} != ${png.length}`);
}
console.log(`wrote ${outPath} (${png.length} bytes)`);
