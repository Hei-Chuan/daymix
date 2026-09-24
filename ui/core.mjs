import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { McpServer } from '@modelcontextprotocol/server';
import { z } from 'zod';

const repo=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const CARD_URI='ui://daymix/card-v2.2.html';
const MAX_OUTPUT=2_000_000; // A full sourced ledger is larger than the text card.
const ENGINE_TIMEOUT_MS=20_000;
function sourceUrls(value, urls=new Set()){
  if(Array.isArray(value))for(const item of value)sourceUrls(item,urls);
  else if(value&&typeof value==='object')for(const [key,item] of Object.entries(value)){
    if(key==='source_url'&&typeof item==='string'&&item.startsWith('https://'))urls.add(item);
    else sourceUrls(item,urls);
  }
  return [...urls];
}

export function runEngine(args){return new Promise((resolve,reject)=>{
  const python=process.env.DAYMIX_PYTHON||process.env.WANXIANGLI_PYTHON||(process.platform==='win32'?'python':'python3');
  const child=spawn(python,[path.join(repo,'scripts/daymix.py'),'--identity-mode','hosted','--format','json',...args],{
    cwd:repo,stdio:['ignore','pipe','pipe'],env:{...process.env,PYTHONIOENCODING:'utf-8'},shell:false
  });
  const chunks=[];let size=0,failed=false,settled=false;
  const timer=setTimeout(()=>{failed=true;child.kill('SIGKILL')},ENGINE_TIMEOUT_MS);
  child.stdout.on('data',chunk=>{size+=chunk.length;if(size>MAX_OUTPUT){failed=true;child.kill('SIGKILL')}else chunks.push(chunk)});
  // Engine diagnostics can contain input values. Never send them to a client or log them.
  child.stderr.resume();
  const finish=(error,value)=>{if(settled)return;settled=true;clearTimeout(timer);error?reject(error):resolve(value)};
  child.on('error',()=>finish(new Error('Daymix engine could not start')));
  child.on('close',code=>{
    if(failed)return finish(new Error(size>MAX_OUTPUT?'Daymix result exceeds output limit':'Daymix engine timed out'));
    if(code!==0)return finish(new Error('Daymix engine failed'));
    try{finish(null,JSON.parse(Buffer.concat(chunks).toString('utf8')))}catch{finish(new Error('Daymix engine returned invalid JSON'))}
  });
})}

export function createDaymixServer({withUi=false}={}){
  const server=new McpServer({name:'daymix',version:'2.3.0',instructions:'Call get_daily_card for the complete daily ledger. Preserve its rating and original signs. A text card and sources are available without a UI.'});
  server.registerTool('get_daily_card',{
    title:'今天呢？· Daymix',description:'Generate one stable Daymix daily card with four symbolic signs, three reflective lenses, sourced text, and optional expandable UI.',
    inputSchema:z.object({date:z.iso.date().optional(),timezone:z.string().min(1).max(100).default('Asia/Shanghai'),user_id:z.string().max(80).optional(),context:z.enum(['备考']).optional()}),
    outputSchema:z.object({schema:z.literal('daymix/2'),cast_version:z.literal('v2.2'),seed_version:z.string(),data_version:z.string(),date:z.record(z.string(),z.unknown()),rating:z.record(z.string(),z.unknown()),four_signs:z.record(z.string(),z.unknown()),three_lenses:z.record(z.string(),z.unknown()),reality:z.record(z.string(),z.unknown()),summary:z.record(z.string(),z.unknown())}).passthrough(),
    annotations:{readOnlyHint:true,openWorldHint:false,destructiveHint:false},
    ...(withUi?{_meta:{ui:{resourceUri:CARD_URI}}}:{})
  },async({date,timezone,user_id,context})=>{
    const args=['--timezone',timezone];if(date)args.push('--date',date);if(user_id)args.push('--user-id',user_id);if(context)args.push('--context',context);
    try{
      const ledger=await runEngine(args);const y=ledger.four_signs.yijing;const t=ledger.four_signs.tarot;
      const l=ledger.three_lenses,r=ledger.reality;
      const plain=[`Daymix · 今天呢 ${ledger.date.gregorian} · ${ledger.rating.rating}`,
        `宜 ${r.effective_dos.join(' · ')}`,`不太建议 ${r.effective_donts.join(' · ')}`,
        `四象：儒家·易 ${y.primary.name}→${y.changed.name}（动爻 ${y.moving_lines.join('、')||'无'}）`,
        `塔罗 ${t.name} · ${t.orientation}；道教 ${ledger.four_signs.daoism.title} · ${ledger.four_signs.daoism.grade||'未标品第'}`,
        `星象 月亮${ledger.four_signs.astrology.positions.moon.zodiac_sign}，主要相位 ${ledger.four_signs.astrology.aspects.length} 项`,
        `三镜：佛教察「${l.buddhism.focus}」；基督宗教 ${l.christianity.ot.reference} ↔ ${l.christianity.nt.reference}；斯多葛关注可控行动`,
        `现实复核：${r.adjustments.join('；')||'未见需要调整的条件'}`,`今日总结：${ledger.summary.text}`,
        `出处：${sourceUrls(ledger).join(' · ')}；其他来源标识及原文见 structuredContent。`].join('\n');
      return {structuredContent:ledger,content:[{type:'text',text:plain}]};
    }catch{return {isError:true,content:[{type:'text',text:'Daymix could not generate the card. Check the date, timezone and server health, then retry.'}]}}
  });
  return server;
}
