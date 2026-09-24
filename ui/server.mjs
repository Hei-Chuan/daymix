import { createServer } from 'node:http';
import { Readable } from 'node:stream';
import { spawn } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { McpServer, WebStandardStreamableHTTPServerTransport } from '@modelcontextprotocol/server';
import { registerAppResource, registerAppTool, RESOURCE_MIME_TYPE } from '@modelcontextprotocol/ext-apps/server';
import { z } from 'zod';

const here=path.dirname(fileURLToPath(import.meta.url));
const repo=path.resolve(here,'..');
const uri='ui://daymix/card-v2.2.html';
const server=new McpServer({name:'daymix',version:'2.2.0',instructions:'Call get_daily_card to generate the complete daily ledger. Preserve its rating and original signs. The UI expands sections locally; without UI, use the returned text card.'});
function runPython(args){return new Promise((resolve,reject)=>{
  const python=process.env.DAYMIX_PYTHON||process.env.WANXIANGLI_PYTHON||(process.platform==='win32'?'python':'python3');
  const child=spawn(python,[path.join(repo,'scripts/daymix.py'),'--identity-mode','hosted','--format','json',...args],{cwd:repo,stdio:['ignore','pipe','pipe'],env:{...process.env,PYTHONIOENCODING:'utf-8'}});
  let out='',err='';const timer=setTimeout(()=>child.kill('SIGKILL'),20000);
  child.stdout.on('data',v=>{out+=v;if(out.length>200000)child.kill('SIGKILL')});child.stderr.on('data',v=>err+=v);
  child.on('error',e=>{clearTimeout(timer);reject(e)});child.on('close',code=>{clearTimeout(timer);code===0?resolve(JSON.parse(out)):reject(new Error(err.slice(0,400)||`engine exited ${code}`))});
})}
registerAppTool(server,'get_daily_card',{
 title:'今天呢？· Daymix',description:'Generate one stable Daymix daily card with four symbolic signs, three reflective lenses, sourced text, and an expandable UI.',
 inputSchema:z.object({date:z.iso.date().optional(),timezone:z.string().default('Asia/Shanghai'),user_id:z.string().max(80).optional(),context:z.enum(['备考']).optional()}),
 annotations:{readOnlyHint:true},_meta:{ui:{resourceUri:uri}}
},async({date,timezone,user_id,context})=>{
 const args=['--timezone',timezone];if(date)args.push('--date',date);if(user_id)args.push('--user-id',user_id);if(context)args.push('--context',context);
 const ledger=await runPython(args);const y=ledger.four_signs.yijing;const t=ledger.four_signs.tarot;
 const l=ledger.three_lenses,r=ledger.reality;
 const plain=[`Daymix · 今天呢 ${ledger.date.gregorian} · ${ledger.rating.rating}`,
  `宜 ${r.effective_dos.join(' · ')}`,`不太建议 ${r.effective_donts.join(' · ')}`,
  `四象：儒家·易 ${y.primary.name}→${y.changed.name}（动爻 ${y.moving_lines.join('、')||'无'}）`,
  `塔罗 ${t.name} · ${t.orientation}；道教 ${ledger.four_signs.daoism.title} · ${ledger.four_signs.daoism.grade||'未标品第'}`,
  `星象 月亮${ledger.four_signs.astrology.positions.moon.zodiac_sign}，主要相位 ${ledger.four_signs.astrology.aspects.length} 项`,
  `三镜：佛教察「${l.buddhism.focus}」；基督宗教 ${l.christianity.ot.reference} ↔ ${l.christianity.nt.reference}；斯多葛关注可控行动`,
  `现实复核：${r.adjustments.join('；')||'未见需要调整的条件'}`,`今日总结：${ledger.summary.text}`].join('\n');
 return {structuredContent:ledger,content:[{type:'text',text:plain}]};
});
registerAppResource(server,'daymix-card',uri,{mimeType:RESOURCE_MIME_TYPE},async()=>({contents:[{uri,mimeType:RESOURCE_MIME_TYPE,text:await readFile(path.join(here,'dist/card.html'),'utf8'),_meta:{ui:{prefersBorder:true}}}]}));
const transport=new WebStandardStreamableHTTPServerTransport({sessionIdGenerator:undefined,enableJsonResponse:true});
await server.connect(transport);
const host=process.env.HOST||'127.0.0.1',port=Number(process.env.PORT||3000);
createServer(async(req,res)=>{
 if(!req.url?.startsWith('/mcp')){res.writeHead(404).end();return}
 try{
  const url=`http://${req.headers.host||`${host}:${port}`}${req.url}`;
  const init={method:req.method,headers:req.headers};
  if(req.method!=='GET'&&req.method!=='HEAD'){init.body=Readable.toWeb(req);init.duplex='half'};
  const response=await transport.handleRequest(new Request(url,init));
  res.writeHead(response.status,Object.fromEntries(response.headers));
  if(response.body)Readable.fromWeb(response.body).pipe(res);else res.end();
 }catch(e){res.writeHead(500,{'content-type':'text/plain'}).end(String(e.message))}
}).listen(port,host,()=>console.error(`Daymix MCP: http://${host}:${port}/mcp`));
