import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { build } from 'esbuild';
const result=await build({entryPoints:[fileURLToPath(new URL('./card.js',import.meta.url))],bundle:true,format:'iife',write:false,minify:true,target:'es2020',platform:'browser'});
const html=await fs.readFile(new URL('./card.html',import.meta.url),'utf8');
await fs.mkdir(new URL('./dist/',import.meta.url),{recursive:true});
await fs.writeFile(new URL('./dist/card.html',import.meta.url),html.replace('/* WIDGET_BUNDLE */',() => result.outputFiles[0].text));
